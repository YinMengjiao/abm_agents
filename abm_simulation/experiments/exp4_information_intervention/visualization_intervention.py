"""
实验 4 可视化：信息干预
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# 添加项目根目录并导入中文字体配置
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from visualization.chinese_font import setup_chinese_font
setup_chinese_font()


def visualize_intervention_results(sim, output_dir: str):
    """可视化干预实验结果"""
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


def _plot_intervention_timeline(ax, sim):
    """绘制干预时间线"""
    if not sim.intervention_system.intervention_history:
        ax.text(0.5, 0.5, '无干预事件', ha='center', va='center')
        return
    
    colors = {
        'positive_publicity': 'green',
        'negative_exposure': 'red',
        'mandatory_cooldown': 'orange',
        'education_campaign': 'blue',
        'regulation': 'purple'
    }
    
    for i, event in enumerate(sim.intervention_system.intervention_history):
        color = colors.get(event.intervention_type.value, 'gray')
        ax.barh(i, event.duration, left=event.timing, color=color, alpha=0.6)
        ax.text(event.timing + event.duration/2, i, 
               event.intervention_type.value[:10], 
               ha='center', va='center', fontsize=8)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('干预事件')
    ax.set_title('干预时间线')
    ax.set_yticks(range(len(sim.intervention_system.intervention_history)))


def _plot_level_evolution_with_interventions(ax, sim):
    """绘制依赖等级演化（标注干预点）"""
    if not sim.metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.metrics_history]
    
    # 绘制各等级演化
    for level in range(1, 6):
        counts = [m.level_distribution.get(level, 0) for m in sim.metrics_history]
        ax.plot(steps, counts, linewidth=2, label=f'L{level}')
    
    # 标注干预点
    for event in sim.intervention_system.intervention_history:
        ax.axvline(x=event.timing, color='red', linestyle='--', alpha=0.5)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('消费者数量')
    ax.set_title('依赖等级演化（红线=干预点）')
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_intervention_impact(ax, sim):
    """绘制干预影响强度"""
    if not sim.intervention_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.intervention_metrics_history]
    impact_scores = [m.intervention_impact_score for m in sim.intervention_metrics_history]
    
    ax.fill_between(steps, impact_scores, alpha=0.5, color='orange')
    ax.plot(steps, impact_scores, 'r-', linewidth=2)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('影响强度')
    ax.set_title('干预影响强度')
    ax.grid(True, alpha=0.3)


def _plot_affected_consumers(ax, sim):
    """绘制受影响消费者数量"""
    if not sim.intervention_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.intervention_metrics_history]
    affected = [m.consumers_affected for m in sim.intervention_metrics_history]
    
    ax.bar(steps, affected, alpha=0.6, color='steelblue')
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('受影响消费者数')
    ax.set_title('每步受影响消费者')


def _plot_policy_effectiveness(ax, sim):
    """绘制政策效果评估"""
    if not sim.intervention_system.intervention_history:
        ax.text(0.5, 0.5, '无干预数据', ha='center', va='center')
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
    ax.set_title('干预类型分布')


def _plot_before_after_comparison(ax, sim):
    """绘制干预前后对比"""
    if not sim.intervention_system.intervention_history or not sim.metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    # 计算每次干预前后的高依赖比例变化
    changes = []
    labels = []
    
    for i, event in enumerate(sim.intervention_system.intervention_history):
        pre_step = max(0, event.timing - 1)
        post_step = min(len(sim.metrics_history) - 1, event.timing + 10)
        
        if pre_step < len(sim.metrics_history) and post_step < len(sim.metrics_history):
            pre_dist = sim.metrics_history[pre_step].level_distribution
            post_dist = sim.metrics_history[post_step].level_distribution
            
            pre_high = sum(pre_dist.get(l, 0) for l in [4, 5])
            post_high = sum(post_dist.get(l, 0) for l in [4, 5])
            
            changes.append(post_high - pre_high)
            labels.append(f'干预{i+1}')
    
    if changes:
        colors = ['green' if c > 0 else 'red' for c in changes]
        ax.bar(labels, changes, color=colors, alpha=0.6)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.set_ylabel('高依赖消费者变化')
        ax.set_title('干预前后对比')
        ax.tick_params(axis='x', rotation=45)
