"""
实验 2 可视化：AI 进化机制
新版布局（2×3）：完整展示 AI 随时间进化的时序证据
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# 添加项目根目录并导入字体配置
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from visualization.chinese_font import setup_chinese_font, setup_english_font
from config import RESULTS

LEVEL_COLORS = ['#4C72B0', '#5B9BD5', '#55A868', '#DD8452', '#C44E52']
AGENT_COLORS = ['#4C72B0', '#DD8452', '#55A868']  # Low / Medium / High — 与 LEVEL_COLORS 同源，低饱和


def visualize_evolution_results(sim, output_dir: str = None, en: bool = False):
    """
    可视化 AI 进化实验结果（2行 × 3列，6个子图）

    叙事逻辑：
      第一行：AI 端证据 — 精度提升、错误率下降、进化进度收敛
      第二行：系统端证据 — 学习事件量、消费者高依赖比例、依赖等级分布

    Args:
        sim: EvolutionSimulation 实例（已运行完毕）
        output_dir: 输出目录（默认 RESULTS["exp2"]）
        en: True=英文标注, False=中文标注
    """
    if output_dir is None:
        output_dir = RESULTS["exp2"]
    os.makedirs(output_dir, exist_ok=True)

    if en:
        setup_english_font()
    else:
        setup_chinese_font()

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle(
        'Experiment 2: AI Agent Evolution' if en else '实验 2：AI 代理进化机制',
        fontsize=16, fontweight='bold', y=0.99
    )

    _plot_per_agent_accuracy(axes[0, 0], sim, en=en)
    _plot_error_rate_decline(axes[0, 1], sim, en=en)
    _plot_evolution_progress(axes[0, 2], sim, en=en)
    _plot_learning_events(axes[1, 0], sim, en=en)
    _plot_trust_recovery(axes[1, 1], sim, en=en)
    _plot_level_distribution_evolution(axes[1, 2], sim, en=en)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    out_path = os.path.join(output_dir, 'evolution_analysis.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 进化分析图已保存：{out_path}")


# ─────────────────────────────────────────────
# 子图函数
# ─────────────────────────────────────────────

def _plot_per_agent_accuracy(ax, sim, en=False):
    """
    (a) 三个 AI 代理的能力初末对比（分组柱状图）
    展示 4 个核心维度在仿真前后的提升幅度。
    精度轨迹因收敛过快（数千次学习事件/步）不适合时序展示，
    改为 Initial vs Final 对比可直接量化"学到了多少"。
    """
    agents = getattr(sim.ai_population, 'agents', [])
    if not agents:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
        return

    # 已知各等级初始值（来自 ai_evolution.py _init_dynamic_capacity）
    INIT_VALS = {
        0: dict(accuracy=0.55, understanding=0.45, reliability=0.70, personalization=0.30),
        1: dict(accuracy=0.75, understanding=0.70, reliability=0.85, personalization=0.55),
        2: dict(accuracy=0.90, understanding=0.90, reliability=0.95, personalization=0.80),
    }

    dims = ['accuracy', 'understanding', 'reliability', 'personalization']
    dim_labels = (
        ['Accuracy', 'Understanding', 'Reliability', 'Personalization']
        if en else ['推荐精度', '理解深度', '执行可靠性', '个性化']
    )
    agent_labels = (
        ['Low-cap', 'Medium-cap', 'High-cap']
        if en else ['低能力', '中能力', '高能力']
    )

    attr_map = dict(
        accuracy='recommendation_accuracy',
        understanding='understanding_depth',
        reliability='execution_reliability',
        personalization='personalization_ability',
    )

    n_dims = len(dims)
    n_agents = len(agents)
    x = np.arange(n_dims)
    bar_w = 0.13
    # 每个维度：n_agents 个 Initial 柱 + n_agents 个 Final 柱
    # 排列：[Low_init, Med_init, High_init, Low_final, Med_final, High_final]

    for i, agent in enumerate(agents):
        init_vals = [INIT_VALS[i][d] for d in dims]
        final_vals = [getattr(agent, attr_map[d], 0) for d in dims]

        offset_init  = (i - (n_agents - 1) / 2) * bar_w - bar_w * n_agents * 0.55
        offset_final = (i - (n_agents - 1) / 2) * bar_w + bar_w * n_agents * 0.55

        ax.bar(x + offset_init,  init_vals,  bar_w,
               color=AGENT_COLORS[i], alpha=0.40, hatch='//',
               label=(f'{agent_labels[i]} Initial' if en else f'{agent_labels[i]} 初始') if i == 0 or True else '')
        ax.bar(x + offset_final, final_vals, bar_w,
               color=AGENT_COLORS[i], alpha=0.90,
               label=f'{agent_labels[i]} Final' if en else f'{agent_labels[i]} 最终')

    # 图例去重
    handles, labels = ax.get_legend_handles_labels()
    # 只保留 Initial（斜线）和 Final（实色）的代表性图例
    unique = {}
    for h, l in zip(handles, labels):
        if l not in unique:
            unique[l] = h
    ax.legend(list(unique.values()), list(unique.keys()), fontsize=8, ncol=2, loc='lower right')

    ax.set_xticks(x)
    ax.set_xticklabels(dim_labels, fontsize=9)
    ax.set_ylabel('Capability Score (0–1)' if en else '能力值 (0–1)', fontsize=10)
    ax.set_ylim(0, 1.10)
    ax.set_title('(a) AI Capability: Initial vs Final' if en else '(a) AI 能力：初末对比', fontsize=11, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)


def _plot_error_rate_decline(ax, sim, en=False):
    """(b) 平均 AI 错误率随时间下降"""
    hist = sim.evolution_metrics_history
    if not hist:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
        return

    steps = [m.step for m in hist]
    error_rates = [m.avg_ai_error_rate for m in hist]

    ax.fill_between(steps, error_rates, alpha=0.25, color='#C44E52')
    ax.plot(steps, error_rates, color='#C44E52', linewidth=2.5,
            label='Avg Error Rate' if en else '平均错误率')

    # 趋势线
    if len(steps) > 10:
        z = np.polyfit(steps, error_rates, 1)
        p = np.poly1d(z)
        ax.plot(steps, p(steps), '--', color='gray', linewidth=1.5, alpha=0.7,
                label='Trend' if en else '趋势线')

    # 标注首末值
    ax.annotate(f'{error_rates[0]:.3f}',
                xy=(steps[0], error_rates[0]), xytext=(10, 8),
                textcoords='offset points', fontsize=9, color='#C44E52', fontweight='bold')
    ax.annotate(f'{error_rates[-1]:.3f}',
                xy=(steps[-1], error_rates[-1]), xytext=(-40, 8),
                textcoords='offset points', fontsize=9, color='#C44E52', fontweight='bold')

    reduction_pct = (error_rates[0] - error_rates[-1]) / max(error_rates[0], 1e-9) * 100
    ax.set_title(f'(b) Error Rate Decline  (↓{reduction_pct:.0f}%)' if en
                 else f'(b) AI错误率下降  (↓{reduction_pct:.0f}%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Simulation Step' if en else '仿真步数', fontsize=10)
    ax.set_ylabel('AI Error Rate' if en else 'AI 错误率', fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)


def _plot_evolution_progress(ax, sim, en=False):
    """(c) 平均进化进度轨迹（0→1）"""
    hist = sim.evolution_metrics_history
    if not hist:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
        return

    steps = [m.step for m in hist]
    progress = [m.avg_evolution_progress for m in hist]

    ax.fill_between(steps, progress, alpha=0.2, color='#2ca02c')
    ax.plot(steps, progress, color='#2ca02c', linewidth=2.5,
            label='Avg Evolution Progress' if en else '平均进化进度')

    # 标注最终进度
    final_val = progress[-1]
    ax.axhline(y=final_val, color='gray', linestyle=':', alpha=0.5)
    ax.annotate(f'Final: {final_val:.3f}',
                xy=(steps[-1], final_val), xytext=(-80, 10),
                textcoords='offset points', fontsize=9, color='#2ca02c', fontweight='bold')

    ax.set_xlabel('Simulation Step' if en else '仿真步数', fontsize=10)
    ax.set_ylabel('Evolution Progress (0–1)' if en else '进化进度 (0–1)', fontsize=10)
    ax.set_title('(c) Evolution Progress Trajectory' if en else '(c) 进化进度轨迹', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)


def _plot_learning_events(ax, sim, en=False):
    """(d) 每步学习事件数（柱状）+ 累积学习事件（折线）"""
    hist = sim.evolution_metrics_history
    if not hist:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
        return

    steps = [m.step for m in hist]
    per_step = [m.learning_events_count for m in hist]
    cumulative = np.cumsum(per_step)

    ax.bar(steps, per_step, alpha=0.55, color='steelblue', width=1.0,
           label='Per-step events' if en else '单步学习事件')

    ax2 = ax.twinx()
    ax2.plot(steps, cumulative, color='#ff7f0e', linewidth=2,
             label='Cumulative' if en else '累积')
    ax2.set_ylabel('Cumulative Events' if en else '累积事件数', fontsize=10, color='#ff7f0e')
    ax2.tick_params(axis='y', labelcolor='#ff7f0e')

    ax.set_xlabel('Simulation Step' if en else '仿真步数', fontsize=10)
    ax.set_ylabel('Events / Step' if en else '事件数/步', fontsize=10)
    ax.set_title('(d) Learning Events' if en else '(d) 学习事件统计', fontsize=11, fontweight='bold')

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.3)


def _plot_trust_recovery(ax, sim, en=False):
    """(e) 高依赖消费者（L4+L5）比例随时间变化"""
    hist = sim.evolution_metrics_history
    if not hist:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
        return

    steps = [m.step for m in hist]
    trust = [m.consumer_trust_recovery for m in hist]

    ax.fill_between(steps, trust, alpha=0.2, color='#9467bd')
    ax.plot(steps, trust, color='#9467bd', linewidth=2.5,
            label='L4+L5 ratio' if en else 'L4+L5 占比')
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5,
               label='50% baseline' if en else '50% 基准')

    ax.set_xlabel('Simulation Step' if en else '仿真步数', fontsize=10)
    ax.set_ylabel('High-dep Ratio' if en else '高依赖比例', fontsize=10)
    ax.set_title('(e) High-Dependency Consumer Ratio' if en else '(e) 高依赖消费者比例', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)


def _plot_level_distribution_evolution(ax, sim, en=False):
    """(f) L1–L5 依赖等级人数随时间演化"""
    if not sim.metrics_history:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
        return

    steps = [m.step for m in sim.metrics_history]
    for level, color in zip(range(1, 6), LEVEL_COLORS):
        counts = [m.level_distribution.get(level, 0) for m in sim.metrics_history]
        ax.plot(steps, counts, color=color, linewidth=2.2,
                label=f'L{level}', alpha=0.85)

    ax.set_xlabel('Simulation Step' if en else '仿真步数', fontsize=10)
    ax.set_ylabel('Agent Count' if en else '智能体数量', fontsize=10)
    ax.set_title('(f) Dependency Level Distribution' if en else '(f) 依赖等级分布演化', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
