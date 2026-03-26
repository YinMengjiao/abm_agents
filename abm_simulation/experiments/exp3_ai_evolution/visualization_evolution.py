"""
实验 3 可视化：AI 进化机制
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


def visualize_evolution_results(sim, output_dir: str = "experiments/exp3_ai_evolution/results"):
    """
    可视化AI进化实验结果
    
    Args:
        sim: EvolutionSimulation实例
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建综合可视化
    fig = plt.figure(figsize=(16, 12))
    
    # 1. AI进化轨迹
    ax1 = plt.subplot(2, 3, 1)
    _plot_ai_evolution_trajectory(ax1, sim)
    
    # 2. 错误率变化
    ax2 = plt.subplot(2, 3, 2)
    _plot_error_rate_evolution(ax2, sim)
    
    # 3. 依赖等级分布对比
    ax3 = plt.subplot(2, 3, 3)
    _plot_level_distribution_evolution(ax3, sim)
    
    # 4. 学习事件统计
    ax4 = plt.subplot(2, 3, 4)
    _plot_learning_events(ax4, sim)
    
    # 5. AI能力进化热力图
    ax5 = plt.subplot(2, 3, 5)
    _plot_capability_heatmap(ax5, sim)
    
    # 6. 信任恢复曲线
    ax6 = plt.subplot(2, 3, 6)
    _plot_trust_recovery(ax6, sim)
    
    plt.suptitle('实验 3: AI 代理进化机制', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 为 suptitle 留出空间
    plt.savefig(f'{output_dir}/evolution_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 进化分析图已保存：{output_dir}/evolution_analysis.png")


def _plot_ai_evolution_trajectory(ax, sim):
    """绘制AI进化轨迹"""
    if not sim.evolution_metrics_history:
        ax.text(0.5, 0.5, '无进化数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.evolution_metrics_history]
    progress = [m.avg_evolution_progress for m in sim.evolution_metrics_history]
    
    ax.plot(steps, progress, 'b-', linewidth=2, label='平均进化进度')
    ax.fill_between(steps, progress, alpha=0.3)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('进化进度')
    ax.set_title('AI进化轨迹')
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.legend()


def _plot_error_rate_evolution(ax, sim):
    """绘制错误率进化"""
    if not sim.evolution_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.evolution_metrics_history]
    error_rates = [m.avg_ai_error_rate for m in sim.evolution_metrics_history]
    
    ax.plot(steps, error_rates, 'r-', linewidth=2, label='平均错误率')
    ax.fill_between(steps, error_rates, alpha=0.3, color='red')
    
    # 添加趋势线
    if len(steps) > 10:
        z = np.polyfit(steps, error_rates, 1)
        p = np.poly1d(z)
        ax.plot(steps, p(steps), 'r--', alpha=0.5, label='趋势线')
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('错误率')
    ax.set_title('AI错误率进化')
    ax.grid(True, alpha=0.3)
    ax.legend()


def _plot_level_distribution_evolution(ax, sim):
    """绘制依赖等级分布演化"""
    if not sim.metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.metrics_history]
    levels = range(1, 6)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for level, color in zip(levels, colors):
        counts = [m.level_distribution.get(level, 0) for m in sim.metrics_history]
        ax.plot(steps, counts, color=color, linewidth=2, label=f'L{level}')
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('消费者数量')
    ax.set_title('依赖等级分布演化')
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_learning_events(ax, sim):
    """绘制学习事件统计"""
    if not sim.evolution_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.evolution_metrics_history]
    learning_counts = [m.learning_events_count for m in sim.evolution_metrics_history]
    
    # 累积学习事件
    cumulative = np.cumsum(learning_counts)
    
    ax.bar(steps, learning_counts, alpha=0.6, label='单步学习事件', color='steelblue')
    ax_twin = ax.twinx()
    ax_twin.plot(steps, cumulative, 'r-', linewidth=2, label='累积学习事件')
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('单步学习事件数', color='steelblue')
    ax_twin.set_ylabel('累积学习事件数', color='red')
    ax.set_title('AI学习事件统计')
    ax.legend(loc='upper left')
    ax_twin.legend(loc='upper right')


def _plot_capability_heatmap(ax, sim):
    """绘制AI能力进化热力图"""
    # 获取AI群体指标
    if not hasattr(sim.ai_population, 'agents'):
        ax.text(0.5, 0.5, '无AI数据', ha='center', va='center')
        return
    
    agents = sim.ai_population.agents
    n_agents = len(agents)
    
    # 构建能力矩阵
    capabilities = ['准确度', '理解深度', '执行可靠性', '个性化']
    capability_matrix = np.zeros((n_agents, len(capabilities)))
    
    for i, agent in enumerate(agents):
        capability_matrix[i, 0] = getattr(agent, 'recommendation_accuracy', 0.5)
        capability_matrix[i, 1] = getattr(agent, 'understanding_depth', 0.5)
        capability_matrix[i, 2] = getattr(agent, 'execution_reliability', 0.5)
        capability_matrix[i, 3] = getattr(agent, 'personalization_ability', 0.5)
    
    im = ax.imshow(capability_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    ax.set_xticks(range(len(capabilities)))
    ax.set_xticklabels(capabilities, rotation=45, ha='right')
    ax.set_yticks(range(n_agents))
    ax.set_yticklabels([f'AI-{i}' for i in range(n_agents)])
    ax.set_title('AI能力进化热力图')
    
    # 添加数值标注
    for i in range(n_agents):
        for j in range(len(capabilities)):
            text = ax.text(j, i, f'{capability_matrix[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    plt.colorbar(im, ax=ax)


def _plot_trust_recovery(ax, sim):
    """绘制信任恢复曲线"""
    if not sim.evolution_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.evolution_metrics_history]
    trust_recovery = [m.consumer_trust_recovery for m in sim.evolution_metrics_history]
    
    ax.plot(steps, trust_recovery, 'g-', linewidth=2, label='高依赖比例(L4-L5)')
    ax.fill_between(steps, trust_recovery, alpha=0.3, color='green')
    
    # 添加基准线
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='50%基准线')
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('高依赖消费者比例')
    ax.set_title('消费者信任恢复曲线')
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.legend()


def _create_comparison_plot(sim, output_dir):
    """创建与基线的对比图"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # AI进化 vs 时间
    if sim.evolution_metrics_history:
        steps = [m.step for m in sim.evolution_metrics_history]
        error_rates = [m.avg_ai_error_rate for m in sim.evolution_metrics_history]
        
        axes[0].plot(steps, error_rates, 'b-', linewidth=2, label='实验3: 进化AI')
        axes[0].set_xlabel('仿真步数')
        axes[0].set_ylabel('AI错误率')
        axes[0].set_title('AI错误率: 进化 vs 基线')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
    
    # 满意度对比
    if sim.metrics_history:
        steps = [m.step for m in sim.metrics_history]
        satisfactions = [np.mean(list(m.satisfaction_distribution.values())) 
                        if m.satisfaction_distribution else 0.5 
                        for m in sim.metrics_history]
        
        axes[1].plot(steps, satisfactions, 'g-', linewidth=2, label='实验3: 进化AI')
        axes[1].set_xlabel('仿真步数')
        axes[1].set_ylabel('平均满意度')
        axes[1].set_title('消费者满意度: 进化 vs 基线')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
    
    plt.suptitle('实验3对比分析', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/evolution_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ 对比分析图已保存: {output_dir}/evolution_comparison.png")
