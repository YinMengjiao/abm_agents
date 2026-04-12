"""
实验 4 可视化：信息干预
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

# 语言配置
TEXT_CONFIG = {
    'zh': {
        'title': '实验 4: 信息干预政策对比',
        'balanced': '均衡政策',
        'promote_ai': '促进AI政策',
        'protect_consumers': '保护消费者政策',
        'timeline_balanced': '(a) 均衡政策：干预事件时间分布',
        'timeline_promote': '(b) 促进AI政策：干预事件时间分布',
        'timeline_protect': '(c) 保护消费者政策：干预事件时间分布',
        'evolution_balanced': '(d) 均衡政策：L1-L5依赖等级动态演化',
        'evolution_promote': '(e) 促进AI政策：L1-L5依赖等级动态演化',
        'evolution_protect': '(f) 保护消费者政策：L1-L5依赖等级动态演化',
        'impact_balanced': '(g) 均衡政策：高依赖群体受干预影响轨迹',
        'impact_promote': '(h) 促进AI政策：高依赖群体受干预影响轨迹',
        'impact_protect': '(i) 保护消费者政策：高依赖群体受干预影响轨迹',
        'before_after_title': '干预前后对比',
        'intervention_effects': '干预效果分析',
        'step_label': '仿真步数',
        'count': '数量',
        'intervention_point': '干预点',
        'no_data': '无数据',
        'high_dependency': '高依赖(L4+L5)',
        'timeline_row': '干预时间线',
        'evolution_row': '依赖等级演化',
        'impact_row': '干预前后高依赖变化',
        'consumer_count': '消费者数量',
        'level_evolution_title': '依赖等级演化（红线=干预点）',
        'intervention_label': '干预',
        'high_dep_evolution': '高依赖群体演化轨迹',
        'impact_intensity': '影响强度',
        'affected_consumers': '受影响消费者数',
        'intervention_type_dist': '干预类型分布',
    },
    'en': {
        'title': 'Experiment 4: Information Intervention Policies',
        'balanced': 'Balanced Policy',
        'promote_ai': 'Pro-AI Policy',
        'protect_consumers': 'Consumer Protection Policy',
        'timeline_balanced': '(a) Balanced: Intervention Timeline',
        'timeline_promote': '(b) Pro-AI: Intervention Timeline',
        'timeline_protect': '(c) Consumer Protection: Intervention Timeline',
        'evolution_balanced': '(d) Balanced: L1-L5 Dependency Level Dynamics',
        'evolution_promote': '(e) Pro-AI: L1-L5 Dependency Level Dynamics',
        'evolution_protect': '(f) Consumer Protection: L1-L5 Dependency Level Dynamics',
        'impact_balanced': '(g) Balanced: High Dependency Group Intervention Impact',
        'impact_promote': '(h) Pro-AI: High Dependency Group Intervention Impact',
        'impact_protect': '(i) Consumer Protection: High Dependency Group Intervention Impact',
        'before_after_title': 'Before vs After Intervention',
        'intervention_effects': 'Intervention Effects Analysis',
        'step_label': 'Simulation Step',
        'count': 'Count',
        'intervention_point': 'Intervention',
        'no_data': 'No Data',
        'high_dependency': 'High Dependency (L4+L5)',
        'timeline_row': 'Intervention Timeline',
        'evolution_row': 'Dependency Level Evolution',
        'impact_row': 'High Dependency Impact',
        'consumer_count': 'Consumer Count',
        'level_evolution_title': 'Dependency Level Evolution (Red=Intervention)',
        'intervention_label': 'Intervention',
        'high_dep_evolution': 'High Dependency Group Evolution',
        'impact_intensity': 'Impact Intensity',
        'affected_consumers': 'Affected Consumers',
        'intervention_type_dist': 'Intervention Type Distribution',
    }
}


def visualize_all_policy_results(policy_sims: dict, output_dir: str = None, en: bool = False):
    """
    将三种政策的结果合并为一张图（3列×3行 = 9子图）
    policy_sims: {'balanced': sim, 'promote_ai': sim, 'protect_consumers': sim}
    
    Args:
        policy_sims: 政策仿真实例字典
        output_dir: 输出目录
        en: True=英文, False=中文 (默认)
    """
    if output_dir is None:
        output_dir = RESULTS["exp4"]
    os.makedirs(output_dir, exist_ok=True)

    policies = list(policy_sims.keys())
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    # 设置字体
    if en:
        setup_english_font()
    else:
        setup_chinese_font()
    
    policy_labels = {
        'balanced': text['balanced'],
        'promote_ai': text['promote_ai'],
        'protect_consumers': text['protect_consumers'],
    }
    n_cols = len(policies)

    fig, axes = plt.subplots(3, n_cols, figsize=(7 * n_cols, 18))
    fig.suptitle(text['title'], fontsize=18, fontweight='bold', y=0.99)

    for col, policy in enumerate(policies):
        sim = policy_sims[policy]
        label = policy_labels.get(policy, policy)

        # 行1：干预时间线 - 每个政策独特标题
        policy_timeline_titles = {
            'balanced': text['timeline_balanced'],
            'promote_ai': text['timeline_promote'],
            'protect_consumers': text['timeline_protect']
        }
        axes[0, col].set_title(policy_timeline_titles.get(policy, label), fontsize=13, fontweight='bold', pad=8)
        _plot_intervention_timeline(axes[0, col], sim, policy_label=label, en=en)

        # 行2：依赖等级演化 - 每个政策独特标题
        policy_evolution_titles = {
            'balanced': text['evolution_balanced'],
            'promote_ai': text['evolution_promote'],
            'protect_consumers': text['evolution_protect']
        }
        _plot_level_evolution_with_interventions(axes[1, col], sim, title=policy_evolution_titles.get(policy), text=text)

        # 行3：干预前后对比 - 每个政策独特标题
        policy_impact_titles = {
            'balanced': text['impact_balanced'],
            'promote_ai': text['impact_promote'],
            'protect_consumers': text['impact_protect']
        }
        _plot_before_after_comparison(axes[2, col], sim, title=policy_impact_titles.get(policy), text=text)

    # 统一行标签（左侧第一列的 y 轴标题已在子函数里设好，这里加行说明）
    row_titles = [text['timeline_row'], text['evolution_row'], text['impact_row']]
    for row, title in enumerate(row_titles):
        axes[row, 0].set_ylabel(f'{title}\n{axes[row, 0].get_ylabel()}', fontsize=11)

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    output_path = os.path.join(output_dir, 'intervention_all_policies.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 实验4综合图已保存：{output_path}")
    return output_path


def visualize_intervention_results(sim, output_dir: str = None):
    """可视化单政策干预实验结果（内部用，对外推荐 visualize_all_policy_results）"""
    if output_dir is None:
        output_dir = RESULTS["exp4"]
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建简化版综合可视化（只展示有数据的子图）
    fig = plt.figure(figsize=(16, 7))
    
    # 1. 干预时间线（左上）- 有数据
    ax1 = plt.subplot(2, 2, 1)
    _plot_intervention_timeline(ax1, sim)
    
    # 2. 依赖等级演化（右上）- 有数据
    ax2 = plt.subplot(2, 2, 2)
    _plot_level_evolution_with_interventions(ax2, sim)
    
    # 3. 干预类型分布（左下）- 有数据
    ax3 = plt.subplot(2, 2, 3)
    _plot_policy_effectiveness(ax3, sim)
    
    # 4. 干预前后对比（右下）- 有数据
    ax4 = plt.subplot(2, 2, 4)
    _plot_before_after_comparison(ax4, sim)
    
    policy_type = getattr(sim, 'policy_type', 'unknown')
    plt.suptitle(f'实验 4: 信息干预效果 ({policy_type})', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 为 suptitle 留出空间
    plt.savefig(f'{output_dir}/intervention_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 干预分析图已保存：{output_dir}/intervention_analysis.png")


def _plot_intervention_timeline(ax, sim, policy_label=None, en: bool = False):
    """绘制干预时间线（事件标记图）
    
    Args:
        ax: matplotlib axis
        sim: simulation instance
        policy_label: policy label
        en: True=English, False=Chinese (default)
    """
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    if not sim.intervention_system.intervention_history:
        ax.text(0.5, 0.5, text['no_data'], ha='center', va='center')
        return
    
    colors = {
        'positive_publicity': 'green',
        'negative_exposure': 'red',
        'mandatory_cooldown': 'orange',
        'education_campaign': 'blue',
        'regulation': 'purple'
    }
    
    # 绘制时间轴（水平线）
    ax.axhline(y=0.5, color='gray', linewidth=1, alpha=0.3)
    
    # 为每个事件使用不同的y位置，避免重叠
    n_events = len(sim.intervention_system.intervention_history)
    y_positions = np.linspace(0.3, 0.7, n_events) if n_events > 1 else [0.5]
    
    for i, event in enumerate(sim.intervention_system.intervention_history):
        color = colors.get(event.intervention_type.value, 'gray')
        timing = event.timing
        duration = event.duration
        
        # 绘制垂直线标记干预时间
        ax.axvline(x=timing, color=color, linestyle='-', linewidth=2, alpha=0.7)
        
        # 绘制持续时间范围（半透明区域）
        ax.axvspan(timing, timing + duration, alpha=0.15, color=color)
        
        # 在顶部标记干预类型
        label_text = event.intervention_type.value.replace('_', ' ')
        if en:
            ax.annotate(f'{label_text}\n(Step {timing}, {duration} steps)', 
                       xy=(timing, y_positions[i]),
                       xytext=(0, 10), textcoords='offset points',
                       ha='center', va='bottom', fontsize=13, 
                       fontweight='bold', color=color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                edgecolor=color, alpha=0.8))
        else:
            ax.annotate(f'{label_text}\n(步{timing}, 持续{duration}步)', 
                       xy=(timing, y_positions[i]),
                       xytext=(0, 10), textcoords='offset points',
                       ha='center', va='bottom', fontsize=13, 
                       fontweight='bold', color=color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                edgecolor=color, alpha=0.8))
    
    ax.set_xlim(-5, 305)
    ax.set_ylim(0, 1)
    ax.set_xlabel(text['step_label'], fontsize=10)
    ax.set_ylabel(text['count'], fontsize=10)
    # 标题已在主函数中设置，这里不再设置
    ax.set_yticks([])  # 隐藏y轴刻度
    ax.grid(axis='x', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)


def _plot_level_evolution_with_interventions(ax, sim, title=None, text=None):
    """Plot dependency level evolution with intervention markers"""
    if text is None:
        text = TEXT_CONFIG['zh']
    
    if not sim.metrics_history:
        ax.text(0.5, 0.5, text['no_data'], ha='center', va='center')
        return
    
    steps = [m.step for m in sim.metrics_history]
    
    # 绘制各等级演化
    for level in range(1, 6):
        counts = [m.level_distribution.get(level, 0) for m in sim.metrics_history]
        ax.plot(steps, counts, linewidth=2, label=f'L{level}')
    
    # 标注干预点
    for event in sim.intervention_system.intervention_history:
        ax.axvline(x=event.timing, color='red', linestyle='--', alpha=0.5)
    
    ax.set_xlabel(text['step_label'], fontsize=10)
    ax.set_ylabel(text['consumer_count'], fontsize=10)
    if title:
        ax.set_title(title, fontsize=13, fontweight='bold')
    else:
        ax.set_title(text['level_evolution_title'], fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)


def _plot_intervention_impact(ax, sim, text=None):
    """Plot intervention impact intensity"""
    if text is None:
        text = TEXT_CONFIG['zh']
    
    if not sim.intervention_metrics_history:
        ax.text(0.5, 0.5, text['no_data'], ha='center', va='center')
        return
    
    steps = [m.step for m in sim.intervention_metrics_history]
    impact_scores = [m.intervention_impact_score for m in sim.intervention_metrics_history]
    
    ax.fill_between(steps, impact_scores, alpha=0.5, color='orange')
    ax.plot(steps, impact_scores, 'r-', linewidth=2)
    
    ax.set_xlabel(text['step_label'])
    ax.set_ylabel(text['impact_intensity'])
    ax.set_title(text['intervention_effects'])
    ax.grid(True, alpha=0.3)


def _plot_affected_consumers(ax, sim, text=None):
    """Plot affected consumer count"""
    if text is None:
        text = TEXT_CONFIG['zh']
    
    if not sim.intervention_metrics_history:
        ax.text(0.5, 0.5, text['no_data'], ha='center', va='center')
        return
    
    steps = [m.step for m in sim.intervention_metrics_history]
    affected = [m.consumers_affected for m in sim.intervention_metrics_history]
    
    ax.bar(steps, affected, alpha=0.6, color='steelblue')
    ax.set_xlabel(text['step_label'])
    ax.set_ylabel(text['affected_consumers'])
    ax.set_title(text['affected_consumers'])


def _plot_policy_effectiveness(ax, sim, text=None):
    """Plot policy effectiveness"""
    if text is None:
        text = TEXT_CONFIG['zh']
    
    if not sim.intervention_system.intervention_history:
        ax.text(0.5, 0.5, text['no_data'], ha='center', va='center')
        return
    
    # 统计各类型干预的效果
    intervention_types = {}
    for event in sim.intervention_system.intervention_history:
        itype = event.intervention_type.value
        if itype not in intervention_types:
            intervention_types[itype] = {'count': 0, 'total_intensity': 0}
        intervention_types[itype]['count'] += 1
        intervention_types[itype]['total_intensity'] += event.intensity
    
    types = list(intervention_types.keys())
    counts = [intervention_types[t]['count'] for t in types]
    
    ax.pie(counts, labels=[t[:10] for t in types], autopct='%1.1f%%')
    ax.set_title(text['intervention_type_dist'])


def _plot_before_after_comparison(ax, sim, title=None, text=None):
    """Plot before-after comparison (line + scatter plot)"""
    if text is None:
        text = TEXT_CONFIG['zh']

    if not sim.intervention_system.intervention_history or not sim.metrics_history:
        ax.text(0.5, 0.5, text['no_data'], ha='center', va='center')
        return

    # 获取高依赖消费者（L4+L5）的演化轨迹
    steps = [m.step for m in sim.metrics_history]
    high_dep_counts = []
    for m in sim.metrics_history:
        high_dep = sum(m.level_distribution.get(l, 0) for l in [4, 5])
        high_dep_counts.append(high_dep)

    # 绘制高依赖消费者数量的演化曲线
    ax.plot(steps, high_dep_counts, 'b-', linewidth=2, alpha=0.7, label=text['high_dependency'])
    ax.fill_between(steps, high_dep_counts, alpha=0.2, color='blue')

    # 标注干预点
    for i, event in enumerate(sim.intervention_system.intervention_history):
        timing = event.timing
        if timing < len(high_dep_counts):
            # 用垂直线标注干预时间
            ax.axvline(x=timing, color='red', linestyle='--', alpha=0.5, linewidth=1)
            # 在干预点添加标记
            ax.plot(timing, high_dep_counts[timing], 'ro', markersize=8)
            intervention_lbl = f"{text['intervention_label']}{i+1}"
            ax.annotate(intervention_lbl, (timing, high_dep_counts[timing]),
                       textcoords="offset points", xytext=(5, 10),
                       fontsize=8, fontweight='bold', color='red')

    ax.set_xlabel(text['step_label'], fontsize=10)
    ax.set_ylabel(text['high_dependency'], fontsize=10)
    if title:
        ax.set_title(title, fontsize=13, fontweight='bold')
    else:
        ax.set_title(text['high_dep_evolution'], fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)


# ─────────────────────────────────────────────────────────────────────────────
# 政策对比汇总图（新增）
# ─────────────────────────────────────────────────────────────────────────────

def visualize_policy_summary(policy_sims: dict, output_dir: str = None, en: bool = False):
    """
    生成政策效果汇总对比图（2行×2列，4个子图）。
    与现有的 9-panel 图互补：聚焦"结果对比"而非"过程展示"。

    子图布局：
      (a) 最终依赖等级分布对比  — 分组柱状图（5等级×3政策）
      (b) 高依赖比例轨迹叠加   — 3条折线画在同一坐标系
      (c) 关键指标横向对比     — 水平条形图（满意度/L1%/L4+L5%）
      (d) 干预净效应           — 各政策高依赖人数初末变化量

    Args:
        policy_sims: {'balanced': sim, 'promote_ai': sim, 'protect_consumers': sim}
        output_dir: 输出目录
        en: True=英文, False=中文
    """
    if output_dir is None:
        output_dir = RESULTS["exp4"]
    os.makedirs(output_dir, exist_ok=True)

    if en:
        setup_english_font()
    else:
        setup_chinese_font()

    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]

    policy_labels = {
        'balanced': text['balanced'],
        'promote_ai': text['promote_ai'],
        'protect_consumers': text['protect_consumers'],
    }
    policies = list(policy_sims.keys())
    POLICY_COLORS = ['#4C72B0', '#DD8452', '#55A868']
    LEVEL_COLORS = ['#4C72B0', '#5B9BD5', '#55A868', '#DD8452', '#C44E52']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        'Experiment 4: Policy Comparison Summary' if en else '实验 4：政策效果汇总对比',
        fontsize=15, fontweight='bold', y=0.99
    )

    # ── (a) 最终依赖等级分布 ─────────────────────────────────────────────────
    ax = axes[0, 0]
    n_policies = len(policies)
    x = np.arange(5)  # L1–L5
    bar_width = 0.25
    offsets = np.linspace(-(n_policies - 1) / 2, (n_policies - 1) / 2, n_policies) * bar_width

    for idx, policy in enumerate(policies):
        sim = policy_sims[policy]
        final_dist = sim.metrics_history[-1].level_distribution if sim.metrics_history else {}
        total = sum(final_dist.values()) or 1
        pcts = [final_dist.get(lv, 0) / total * 100 for lv in range(1, 6)]
        ax.bar(x + offsets[idx], pcts, bar_width,
               label=policy_labels.get(policy, policy),
               color=POLICY_COLORS[idx % len(POLICY_COLORS)], alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels([f'L{i}' for i in range(1, 6)], fontsize=11)
    ax.set_xlabel('Dependency Level' if en else '依赖等级', fontsize=10)
    ax.set_ylabel('Percentage (%)' if en else '占比 (%)', fontsize=10)
    ax.set_title('(a) Final Distribution Comparison' if en else '(a) 最终依赖等级分布对比',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    # ── (b) 高依赖比例轨迹叠加 ──────────────────────────────────────────────
    ax = axes[0, 1]
    for idx, policy in enumerate(policies):
        sim = policy_sims[policy]
        if not sim.metrics_history:
            continue
        steps = [m.step for m in sim.metrics_history]
        high_dep = [
            (m.level_distribution.get(4, 0) + m.level_distribution.get(5, 0))
            / (sum(m.level_distribution.values()) or 1) * 100
            for m in sim.metrics_history
        ]
        ax.plot(steps, high_dep, color=POLICY_COLORS[idx % len(POLICY_COLORS)],
                linewidth=2.2, label=policy_labels.get(policy, policy), alpha=0.85)

        # 标注干预点
        for event in sim.intervention_system.intervention_history:
            ax.axvline(x=event.timing, color=POLICY_COLORS[idx % len(POLICY_COLORS)],
                       linestyle=':', linewidth=1, alpha=0.5)

    ax.set_xlabel('Simulation Step' if en else '仿真步数', fontsize=10)
    ax.set_ylabel('High-dep Ratio (%)' if en else '高依赖比例 (%)', fontsize=10)
    ax.set_title('(b) High-Dependency Trajectory (Overlay)' if en else '(b) 高依赖比例轨迹叠加',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── (c) 关键指标横向对比 ─────────────────────────────────────────────────
    ax = axes[1, 0]
    metric_labels = (
        ['Avg Satisfaction', 'L1 Ratio (%)', 'High-dep L4+L5 (%)']
        if en else ['平均满意度', 'L1 占比 (%)', '高依赖 L4+L5 (%)']
    )
    metric_values = {p: [] for p in policies}

    for policy in policies:
        sim = policy_sims[policy]
        if not sim.metrics_history:
            metric_values[policy] = [0, 0, 0]
            continue
        final = sim.metrics_history[-1]
        total = sum(final.level_distribution.values()) or 1
        sat = getattr(final, 'avg_satisfaction', 0)
        l1_pct = final.level_distribution.get(1, 0) / total * 100
        high_pct = (final.level_distribution.get(4, 0) + final.level_distribution.get(5, 0)) / total * 100
        metric_values[policy] = [sat, l1_pct, high_pct]

    y = np.arange(len(metric_labels))
    bar_h = 0.25
    offsets_h = np.linspace(-(n_policies - 1) / 2, (n_policies - 1) / 2, n_policies) * bar_h

    for idx, policy in enumerate(policies):
        vals = metric_values[policy]
        # 对满意度归一化到0-100%便于同图展示
        display_vals = [vals[0] * 100, vals[1], vals[2]]
        bars = ax.barh(y + offsets_h[idx], display_vals, bar_h,
                       label=policy_labels.get(policy, policy),
                       color=POLICY_COLORS[idx % len(POLICY_COLORS)], alpha=0.85)
        for bar, val in zip(bars, display_vals):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f'{val:.1f}', va='center', fontsize=8)

    ax.set_yticks(y)
    ax.set_yticklabels(metric_labels, fontsize=10)
    ax.set_xlabel('Value (Satisfaction ×100 / %)' if en else '数值（满意度×100 / %）', fontsize=9)
    ax.set_title('(c) Key Metrics Comparison' if en else '(c) 关键指标对比',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='x', alpha=0.3)

    # ── (d) 干预净效应（高依赖人数初末变化）────────────────────────────────
    ax = axes[1, 1]
    deltas = []
    init_vals = []
    final_vals = []

    for policy in policies:
        sim = policy_sims[policy]
        if not sim.metrics_history:
            deltas.append(0); init_vals.append(0); final_vals.append(0)
            continue
        init_m = sim.metrics_history[0]
        final_m = sim.metrics_history[-1]
        init_hd = init_m.level_distribution.get(4, 0) + init_m.level_distribution.get(5, 0)
        final_hd = final_m.level_distribution.get(4, 0) + final_m.level_distribution.get(5, 0)
        init_vals.append(init_hd)
        final_vals.append(final_hd)
        deltas.append(final_hd - init_hd)

    p_labels = [policy_labels.get(p, p) for p in policies]
    x_pos = np.arange(n_policies)
    colors_delta = ['#C44E52' if d > 0 else '#55A868' for d in deltas]

    ax.bar(x_pos, init_vals, color='lightgray', alpha=0.6, label='Initial' if en else '初始值', zorder=2)
    ax.bar(x_pos, deltas, bottom=init_vals, color=colors_delta, alpha=0.85,
           label='Change' if en else '变化量', zorder=3)

    for i, (init, delta) in enumerate(zip(init_vals, deltas)):
        sign = '+' if delta >= 0 else ''
        ax.text(i, init + delta + 2, f'{sign}{delta:.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                color=colors_delta[i])

    ax.set_xticks(x_pos)
    ax.set_xticklabels(p_labels, fontsize=10)
    ax.set_ylabel('High-dep Count (L4+L5)' if en else '高依赖人数 (L4+L5)', fontsize=10)
    ax.set_title('(d) Net Intervention Effect on High-Dep' if en else '(d) 干预对高依赖人数的净效应',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    out_path = os.path.join(output_dir, 'intervention_policy_summary.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] 政策汇总对比图已保存：{out_path}")
    return out_path
