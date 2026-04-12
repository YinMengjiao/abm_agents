"""
实验6可视化: 代际演化
"""

import matplotlib.pyplot as plt
import numpy as np
import os


def visualize_generational_results(sim, output_dir: str):
    """可视化代际演化结果"""
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. 代际构成演化
    ax1 = plt.subplot(2, 3, 1)
    _plot_generation_composition(ax1, sim)
    
    # 2. 各代依赖等级趋势
    ax2 = plt.subplot(2, 3, 2)
    _plot_dependency_by_generation(ax2, sim)
    
    # 3. 代际更替事件
    ax3 = plt.subplot(2, 3, 3)
    _plot_generation_transitions(ax3, sim)
    
    # 4. 长期依赖等级演化
    ax4 = plt.subplot(2, 3, 4)
    _plot_long_term_evolution(ax4, sim)
    
    # 5. 代际差异对比
    ax5 = plt.subplot(2, 3, 5)
    _plot_generation_differences(ax5, sim)
    
    # 6. 文化传递效果
    ax6 = plt.subplot(2, 3, 6)
    _plot_cultural_transmission(ax6, sim)
    
    plt.suptitle('实验6: 多代际演化分析', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/generational_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ 代际分析图已保存: {output_dir}/generational_analysis.png")


def _plot_generation_composition(ax, sim):
    """绘制代际构成演化"""
    if not sim.generational_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.generational_metrics_history]
    
    # 获取各代类型随时间的变化
    gen_types = ['immigrant', 'native', 'transitional']
    colors = {'immigrant': 'brown', 'native': 'green', 'transitional': 'orange'}
    
    for gen_type in gen_types:
        counts = [m.generation_composition.get(gen_type, 0) for m in sim.generational_metrics_history]
        if any(counts):
            ax.plot(steps, counts, label=gen_type, color=colors.get(gen_type, 'gray'), linewidth=2)
    
    # 标注代际更替点
    for i in range(1, sim.n_generations):
        ax.axvline(x=i * sim.generation_duration, color='red', linestyle='--', alpha=0.5)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('人口数量')
    ax.set_title('代际构成演化')
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_dependency_by_generation(ax, sim):
    """绘制各代依赖等级趋势"""
    if not sim.generational_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.generational_metrics_history]
    
    # 绘制各代的平均依赖等级
    gen_types = ['immigrant', 'transitional', 'native']
    colors = {'immigrant': 'brown', 'transitional': 'orange', 'native': 'green'}
    
    for gen_type in gen_types:
        deps = [m.avg_dependency_by_generation.get(gen_type, 3.0) 
                for m in sim.generational_metrics_history]
        if any(d != 3.0 for d in deps):
            ax.plot(steps, deps, label=gen_type, color=colors.get(gen_type, 'gray'), linewidth=2)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('平均依赖等级')
    ax.set_title('各代依赖等级趋势')
    ax.set_ylim(1, 5)
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_generation_transitions(ax, sim):
    """绘制代际更替事件"""
    history = sim.generational_dynamics.generation_history
    
    if not history:
        ax.text(0.5, 0.5, '无代际更替', ha='center', va='center')
        return
    
    events = []
    steps = []
    
    for event in history:
        steps.append(event['step'])
        events.append({
            'generation': event['generation'],
            'type': event['type'],
            'exits': event['exits'],
            'entries': event['entries']
        })
    
    # 绘制更替事件
    for i, event in enumerate(events):
        ax.bar(i, event['exits'], color='red', alpha=0.6, label='退出' if i == 0 else '')
        ax.bar(i, event['entries'], bottom=event['exits'], color='green', alpha=0.6, label='进入' if i == 0 else '')
    
    ax.set_xlabel('更替事件')
    ax.set_ylabel('人数')
    ax.set_title('代际更替事件')
    ax.set_xticks(range(len(events)))
    ax.set_xticklabels([f'G{e["generation"]}' for e in events])
    ax.legend()


def _plot_long_term_evolution(ax, sim):
    """绘制长期依赖等级演化"""
    if not sim.metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.metrics_history]
    
    # 绘制各等级演化
    for level in range(1, 6):
        counts = [m.level_distribution.get(level, 0) for m in sim.metrics_history]
        ax.plot(steps, counts, linewidth=2, label=f'L{level}')
    
    # 标注代际更替点
    for i in range(1, sim.n_generations):
        ax.axvline(x=i * sim.generation_duration, color='red', linestyle='--', alpha=0.3)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('消费者数量')
    ax.set_title('长期依赖等级演化')
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_generation_differences(ax, sim):
    """绘制代际差异对比"""
    summary = sim.generational_dynamics.get_summary()
    by_gen = summary.get('dependency_by_generation', {})
    
    if not by_gen:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    gen_types = list(by_gen.keys())
    levels = range(1, 6)
    
    x = np.arange(len(gen_types))
    width = 0.15
    
    for level in levels:
        counts = [by_gen.get(gen, {}).get(level, 0) for gen in gen_types]
        ax.bar(x + (level-3) * width, counts, width, label=f'L{level}')
    
    ax.set_xlabel('代际类型')
    ax.set_ylabel('消费者数量')
    ax.set_title('各代依赖等级分布')
    ax.set_xticks(x)
    ax.set_xticklabels(gen_types, rotation=45, ha='right')
    ax.legend()


def _plot_cultural_transmission(ax, sim):
    """绘制文化传递效果"""
    # 分析父母影响的效果
    history = sim.generational_dynamics.generation_history
    
    if len(history) < 2:
        ax.text(0.5, 0.5, '数据不足', ha='center', va='center')
        return
    
    # 计算每代的平均依赖等级
    gen_deps = []
    gen_labels = []
    
    for i, metric in enumerate(sim.generational_metrics_history):
        if i % sim.generation_duration == 0 or i == len(sim.generational_metrics_history) - 1:
            avg_dep = np.mean(list(metric.avg_dependency_by_generation.values()))
            gen_deps.append(avg_dep)
            gen_labels.append(f'Step {metric.step}')
    
    if gen_deps:
        ax.plot(range(len(gen_deps)), gen_deps, 'o-', linewidth=2, markersize=8)
        ax.set_xlabel('观测点')
        ax.set_ylabel('平均依赖等级')
        ax.set_title('文化演化趋势')
        ax.set_xticks(range(len(gen_labels)))
        ax.set_xticklabels(gen_labels, rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
