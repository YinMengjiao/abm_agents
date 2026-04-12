"""
稳健性分析：全部实验各运行 N 次，展示关键指标的均值 ± SD
输出：results/robustness/robustness_analysis.png
"""

import sys
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from simulation import ABMSimulation, SimulationConfig
from experiments.exp2_mechanism.simulation_evolution import EvolutionSimulation
from experiments.exp3_consequences.filter_bubble.filter_bubble import (
    FilterBubbleAnalyzer,
)
from experiments.exp3_consequences.systemic_risk.systemic_risk import (
    SystemicRiskModel, FailureType, FailureSeverity,
)
from experiments.exp4_intervention.simulation_intervention import InterventionSimulation
from visualization.chinese_font import setup_english_font
from config import RESULTS, RESULTS_ROOT


# ─────────────────────────────────────────────────────────────────────────────
# 公共仿真配置
# ─────────────────────────────────────────────────────────────────────────────
def _base_config():
    return SimulationConfig(
        n_consumers=500,
        n_merchants=20,
        n_ai_agents=3,
        network_type='small_world',
        n_steps=300,
        initial_coupling=0.2,
        initial_temperature=2.0,
        enable_adaptive_coupling=True,
        coupling_trend=0.0005,
        shock_probability=0.05,
    )


def _silent(fn, *args, **kwargs):
    """运行 fn，将 stdout/stderr 重定向到 /dev/null，避免刷屏"""
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = io.StringIO()
    try:
        return fn(*args, **kwargs)
    finally:
        sys.stdout, sys.stderr = old_out, old_err


# ─────────────────────────────────────────────────────────────────────────────
# 各实验单次运行函数
# ─────────────────────────────────────────────────────────────────────────────

def _run_exp1():
    """返回 dict: step→ {l4_pct, magnetization, satisfaction}"""
    sim = ABMSimulation(_base_config())
    _silent(sim.run)
    steps = [m.step for m in sim.metrics_history]
    total = _base_config().n_consumers
    l4_pct = [
        (m.level_distribution.get(4, 0) + m.level_distribution.get(5, 0)) / total * 100
        for m in sim.metrics_history
    ]
    mag = [m.magnetization for m in sim.metrics_history]
    sat = [m.avg_satisfaction for m in sim.metrics_history]
    final_dist = {lv: sim.metrics_history[-1].level_distribution.get(lv, 0) / total * 100
                  for lv in range(1, 6)}
    return dict(steps=steps, l4_pct=l4_pct, magnetization=mag,
                satisfaction=sat, final_dist=final_dist)


def _run_exp2():
    """返回 dict: step→ error_rate, evolution_progress"""
    sim = EvolutionSimulation(_base_config(), evolution_rate=0.02)
    _silent(sim.run)
    steps = [m.step for m in sim.evolution_metrics_history]
    error_rate = [m.avg_ai_error_rate for m in sim.evolution_metrics_history]
    progress = [m.avg_evolution_progress for m in sim.evolution_metrics_history]
    final_error = error_rate[-1] if error_rate else np.nan
    reduction_pct = (error_rate[0] - error_rate[-1]) / max(error_rate[0], 1e-9) * 100 if error_rate else np.nan
    return dict(steps=steps, error_rate=error_rate, progress=progress,
                final_error=final_error, reduction_pct=reduction_pct)


def _run_exp3a():
    """返回 dict: diversity_by_level (L1-L5), bubble_strength, overall_diversity"""
    analyzer = FilterBubbleAnalyzer(n_categories=20)
    results = _silent(analyzer.run_filter_bubble_experiment, n_consumers=500, n_rounds=50)
    pm = results['population_metrics']
    div_by_level = [pm['diversity_by_level'].get(lv, np.nan) for lv in range(1, 6)]
    return dict(
        div_by_level=div_by_level,
        bubble_strength=pm['filter_bubble_strength'],
        overall_diversity=pm['overall_diversity'],
    )


def _run_exp3b():
    """返回 dict: trust_trajectory (200步均值), trust_drop, max_affected, recovery_time, resilience"""
    risk_model = SystemicRiskModel(n_consumers=500)
    main_result = _silent(
        risk_model.run_crisis_simulation,
        failure_type=FailureType.TECHNICAL_OUTAGE,
        severity=FailureSeverity.MAJOR,
        n_steps=200,
    )
    risk_metrics = risk_model.calculate_systemic_risk_metrics() or {}
    # 信任轨迹：trust_trajectory 是 List[np.ndarray]，取每步均值
    trust_traj = [float(np.mean(t)) for t in risk_model.trust_trajectory]
    return dict(
        trust_trajectory=trust_traj,
        trust_drop=main_result.get('trust_drop', np.nan),
        max_affected=main_result.get('max_affected', np.nan),
        recovery_time=main_result.get('recovery_time', np.nan),
        resilience=risk_metrics.get('system_resilience', np.nan),
    )


def _run_exp4_policy(policy: str):
    """返回 dict: final level dist (L1-L5 %) + high_dep_pct"""
    config = SimulationConfig(
        n_consumers=500, n_merchants=20, n_ai_agents=3,
        network_type='small_world', n_steps=300,
        initial_coupling=0.2, initial_temperature=2.0,
        enable_adaptive_coupling=True,
    )
    sim = InterventionSimulation(config, policy_type=policy)
    _silent(sim.run)
    total = config.n_consumers
    final = sim.metrics_history[-1].level_distribution if sim.metrics_history else {}
    dist = {lv: final.get(lv, 0) / total * 100 for lv in range(1, 6)}
    high_dep = dist[4] + dist[5]
    return dict(dist=dist, high_dep_pct=high_dep)


# ─────────────────────────────────────────────────────────────────────────────
# 主收集函数
# ─────────────────────────────────────────────────────────────────────────────

def run_all_robustness(n_runs: int = 10, seed_base: int = 42):
    """
    运行全部实验各 n_runs 次，返回汇总数据字典。
    总运行量：Exp1×n + Exp2×n + Exp3a×n + Exp3b×n + Exp4×3×n
    """
    rng = np.random.default_rng(seed_base)

    def _set_seed(i):
        np.random.seed(int(rng.integers(0, 99999)))

    results = {
        'exp1': [], 'exp2': [],
        'exp3a': [], 'exp3b': [],
        'exp4': {p: [] for p in ['balanced', 'promote_ai', 'protect_consumers']},
        'n_runs': n_runs,
    }

    total_jobs = n_runs * (1 + 1 + 1 + 1 + 3)
    done = 0

    def _progress(label):
        nonlocal done
        done += 1
        print(f"  [{done:>3}/{total_jobs}] {label}", flush=True)

    print(f"\n{'='*60}")
    print(f"稳健性分析：每个实验运行 {n_runs} 次")
    print(f"{'='*60}\n")

    # Exp1
    print("【实验1】基线模型...")
    for i in range(n_runs):
        _set_seed(i)
        results['exp1'].append(_run_exp1())
        _progress(f"Exp1 run {i+1}/{n_runs}")

    # Exp2
    print("\n【实验2】AI进化...")
    for i in range(n_runs):
        _set_seed(i)
        results['exp2'].append(_run_exp2())
        _progress(f"Exp2 run {i+1}/{n_runs}")

    # Exp3a
    print("\n【实验3a】过滤气泡...")
    for i in range(n_runs):
        _set_seed(i)
        results['exp3a'].append(_run_exp3a())
        _progress(f"Exp3a run {i+1}/{n_runs}")

    # Exp3b
    print("\n【实验3b】系统性风险...")
    for i in range(n_runs):
        _set_seed(i)
        results['exp3b'].append(_run_exp3b())
        _progress(f"Exp3b run {i+1}/{n_runs}")

    # Exp4
    for policy in ['balanced', 'promote_ai', 'protect_consumers']:
        print(f"\n【实验4】{policy}...")
        for i in range(n_runs):
            _set_seed(i)
            results['exp4'][policy].append(_run_exp4_policy(policy))
            _progress(f"Exp4({policy}) run {i+1}/{n_runs}")

    print(f"\n{'='*60}")
    print("所有运行完成！")
    print(f"{'='*60}\n")
    return results


# ─────────────────────────────────────────────────────────────────────────────
# 可视化
# ─────────────────────────────────────────────────────────────────────────────

MUTED = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#9467bd']
POLICY_COLORS = {'balanced': '#4C72B0', 'promote_ai': '#DD8452', 'protect_consumers': '#55A868'}
POLICY_LABELS = {'balanced': 'Balanced', 'promote_ai': 'Pro-AI', 'protect_consumers': 'Consumer Prot.'}


def _shade_band(ax, steps, runs_data, color, label, alpha_band=0.20, alpha_line=0.12):
    """绘制 mean 粗线 + ±1SD 阴影带 + 10 条细透明线"""
    arr = np.array(runs_data)          # shape (n_runs, n_steps)
    mean = arr.mean(axis=0)
    sd = arr.std(axis=0)
    for row in arr:
        ax.plot(steps, row, color=color, linewidth=0.8, alpha=alpha_line)
    ax.fill_between(steps, mean - sd, mean + sd, color=color, alpha=alpha_band)
    ax.plot(steps, mean, color=color, linewidth=2.2, label=label)


def visualize_robustness(results: dict, output_dir: str = None):
    setup_english_font()

    if output_dir is None:
        output_dir = os.path.join(RESULTS_ROOT, 'robustness')
    os.makedirs(output_dir, exist_ok=True)

    n_runs = results['n_runs']
    n_steps = 300

    # ── 对齐各运行的步数序列（截取最短公共长度）──────────────────────────
    def _align(runs, key):
        min_len = min(len(r[key]) for r in runs)
        return np.array([r[key][:min_len] for r in runs]), list(range(min_len))

    exp1_l4, steps1   = _align(results['exp1'], 'l4_pct')
    exp1_mag, _       = _align(results['exp1'], 'magnetization')
    exp2_err, steps2  = _align(results['exp2'], 'error_rate')

    # Exp3b trust trajectory
    min_t = min(len(r['trust_trajectory']) for r in results['exp3b'])
    exp3b_trust = np.array([r['trust_trajectory'][:min_t] for r in results['exp3b']])
    steps3b = list(range(min_t))

    # ── 创建图 ─────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 13))
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])
    ax_d = fig.add_subplot(gs[1, 0])
    ax_e = fig.add_subplot(gs[1, 1])
    ax_f = fig.add_subplot(gs[1, 2])
    ax_g = fig.add_subplot(gs[2, :])   # 底部跨三列

    fig.suptitle(f'Robustness Analysis  (N = {n_runs} runs per experiment)',
                 fontsize=15, fontweight='bold', y=0.98)

    # ── (a) Exp1: L4+L5 proportion trajectory ─────────────────────────────
    _shade_band(ax_a, steps1, exp1_l4, MUTED[0], 'L4+L5%')
    ax_a.set_title('(a)  Exp1 — High-dep (L4+L5) Trajectory', fontsize=10, fontweight='bold')
    ax_a.set_xlabel('Simulation Step', fontsize=9)
    ax_a.set_ylabel('High-dep Proportion (%)', fontsize=9)
    ax_a.legend(fontsize=9)
    ax_a.grid(True, alpha=0.3)

    # ── (b) Exp2: Error rate trajectory ───────────────────────────────────
    _shade_band(ax_b, steps2, exp2_err, MUTED[3], 'Avg Error Rate')
    # 标注首末均值
    init_mean = exp2_err[:, 0].mean()
    final_mean = exp2_err[:, -1].mean()
    reduction = (init_mean - final_mean) / max(init_mean, 1e-9) * 100
    ax_b.set_title(f'(b)  Exp2 — AI Error Rate  (mean ↓{reduction:.0f}%)', fontsize=10, fontweight='bold')
    ax_b.set_xlabel('Simulation Step', fontsize=9)
    ax_b.set_ylabel('AI Error Rate', fontsize=9)
    ax_b.legend(fontsize=9)
    ax_b.grid(True, alpha=0.3)

    # ── (c) Exp3b: Trust trajectory ────────────────────────────────────────
    _shade_band(ax_c, steps3b, exp3b_trust, MUTED[4], 'Avg Trust')
    # 标注故障发生步
    ax_c.axvline(x=50, color='red', linestyle='--', linewidth=1.2, alpha=0.7, label='Failure @ step 50')
    ax_c.set_title('(c)  Exp3b — Trust Trajectory (Failure @ step 50)', fontsize=10, fontweight='bold')
    ax_c.set_xlabel('Simulation Step', fontsize=9)
    ax_c.set_ylabel('Avg Trust Level', fontsize=9)
    ax_c.legend(fontsize=9)
    ax_c.grid(True, alpha=0.3)

    # ── (d) Exp1: Final level distribution boxplot ─────────────────────────
    final_dists = np.array([[r['final_dist'][lv] for lv in range(1, 6)]
                             for r in results['exp1']])  # (n_runs, 5)
    bp = ax_d.boxplot(
        [final_dists[:, i] for i in range(5)],
        tick_labels=[f'L{i}' for i in range(1, 6)],
        patch_artist=True,
        medianprops=dict(color='black', linewidth=1.5),
    )
    for patch, color in zip(bp['boxes'], MUTED):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax_d.set_title('(d)  Exp1 — Final Level Distribution', fontsize=10, fontweight='bold')
    ax_d.set_xlabel('Dependency Level', fontsize=9)
    ax_d.set_ylabel('Proportion (%)', fontsize=9)
    ax_d.grid(axis='y', alpha=0.3)

    # ── (e) Exp3a: Diversity by level + bubble strength ────────────────────
    div_by_level = np.array([r['div_by_level'] for r in results['exp3a']])  # (n_runs, 5)
    bubble_str = np.array([r['bubble_strength'] for r in results['exp3a']])

    bp2 = ax_e.boxplot(
        [div_by_level[:, i] for i in range(5)],
        tick_labels=[f'L{i}' for i in range(1, 6)],
        patch_artist=True,
        medianprops=dict(color='black', linewidth=1.5),
    )
    for patch, color in zip(bp2['boxes'], MUTED):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    # 右轴：bubble strength scatter
    ax_e2 = ax_e.twinx()
    ax_e2.scatter(np.ones(n_runs) * 5.6, bubble_str,
                  color='red', s=30, alpha=0.6, zorder=5)
    ax_e2.errorbar(5.6, bubble_str.mean(), yerr=bubble_str.std(),
                   fmt='D', color='red', markersize=7, capsize=4, zorder=6,
                   label=f'Bubble strength\nμ={bubble_str.mean():.3f}±{bubble_str.std():.3f}')
    ax_e2.set_ylabel('Filter Bubble Strength', fontsize=9, color='red')
    ax_e2.tick_params(axis='y', labelcolor='red')
    ax_e2.legend(fontsize=8, loc='upper right')
    ax_e.set_title('(e)  Exp3a — Choice Diversity by Level', fontsize=10, fontweight='bold')
    ax_e.set_xlabel('Dependency Level', fontsize=9)
    ax_e.set_ylabel('Diversity Score', fontsize=9)
    ax_e.grid(axis='y', alpha=0.3)

    # ── (f) Exp3b: Scalar metrics boxplot ──────────────────────────────────
    trust_drop  = np.array([r['trust_drop']    for r in results['exp3b']])
    cascade_sz  = np.array([r['max_affected']  for r in results['exp3b']])
    rec_time    = np.array([r['recovery_time'] for r in results['exp3b']])
    resilience  = np.array([r['resilience']    for r in results['exp3b']])

    # 归一化到同一量纲（0-1）以便同图展示
    def _norm(x):
        r = np.nanmax(x) - np.nanmin(x)
        return (x - np.nanmin(x)) / r if r > 0 else np.zeros_like(x)

    box_data = [_norm(trust_drop), _norm(cascade_sz), _norm(rec_time), _norm(resilience)]
    metric_labels = ['Trust Drop', 'Max Affected', 'Recovery Time', 'Resilience']
    bp3 = ax_f.boxplot(
        box_data, tick_labels=metric_labels, patch_artist=True,
        medianprops=dict(color='black', linewidth=1.5),
    )
    for patch, color in zip(bp3['boxes'], MUTED):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax_f.set_title('(f)  Exp3b — Risk Metrics (normalized)', fontsize=10, fontweight='bold')
    ax_f.set_ylabel('Normalized Value', fontsize=9)
    ax_f.tick_params(axis='x', labelsize=8)
    ax_f.grid(axis='y', alpha=0.3)

    # 右轴：实际均值标注
    for i, (data, lbl) in enumerate(zip([trust_drop, cascade_sz, rec_time, resilience], metric_labels), 1):
        ax_f.text(i, 1.05, f'{np.nanmean(data):.2f}', ha='center', fontsize=7.5, color='gray')

    # ── (g) Exp4: Final high-dep% per policy (跨三列) ──────────────────────
    policies = ['balanced', 'promote_ai', 'protect_consumers']
    n_policies = len(policies)
    x_pos = np.arange(n_policies)
    width = 0.55

    high_dep_runs = np.array([
        [r['high_dep_pct'] for r in results['exp4'][p]] for p in policies
    ])  # shape (3, n_runs)

    means = high_dep_runs.mean(axis=1)
    sds   = high_dep_runs.std(axis=1)

    bars = ax_g.bar(x_pos, means, width, yerr=sds, capsize=6,
                    color=[POLICY_COLORS[p] for p in policies], alpha=0.80,
                    error_kw=dict(elinewidth=1.5, ecolor='gray'))

    # 在每个柱子上方叠加散点（10个运行点）
    for i, policy in enumerate(policies):
        jitter = np.random.uniform(-0.15, 0.15, n_runs)
        ax_g.scatter(x_pos[i] + jitter, high_dep_runs[i],
                     color=POLICY_COLORS[policy], s=18, alpha=0.55, zorder=5)
        ax_g.text(x_pos[i], means[i] + sds[i] + 1.5,
                  f'{means[i]:.1f}±{sds[i]:.1f}%',
                  ha='center', fontsize=9.5, fontweight='bold',
                  color=POLICY_COLORS[policy])

    ax_g.set_xticks(x_pos)
    ax_g.set_xticklabels([POLICY_LABELS[p] for p in policies], fontsize=11)
    ax_g.set_ylabel('High-dep Proportion L4+L5 (%)', fontsize=10)
    ax_g.set_title('(g)  Exp4 — Final High-Dependency (L4+L5) per Policy  '
                   '(bars = mean ± SD;  dots = individual runs)',
                   fontsize=10, fontweight='bold')
    ax_g.grid(axis='y', alpha=0.3)
    ax_g.set_ylim(0, max(means + sds) * 1.25 + 5)

    # ── 保存 ───────────────────────────────────────────────────────────────
    out_path = os.path.join(output_dir, 'robustness_analysis.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 稳健性分析图已保存：{out_path}")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='稳健性分析：全实验多次运行')
    parser.add_argument('--n', type=int, default=10, help='每个实验的运行次数（默认10）')
    parser.add_argument('--seed', type=int, default=42, help='随机种子基值')
    args = parser.parse_args()

    all_results = run_all_robustness(n_runs=args.n, seed_base=args.seed)

    out_dir = os.path.join(RESULTS_ROOT, 'robustness')
    visualize_robustness(all_results, output_dir=out_dir)
