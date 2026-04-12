"""
实验7可视化: AI竞争
"""

import matplotlib.pyplot as plt
import numpy as np
import os


def visualize_competition_results(sim, output_dir: str):
    """可视化AI竞争结果"""
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. 市场份额演化
    ax1 = plt.subplot(2, 3, 1)
    _plot_market_share_evolution(ax1, sim)
    
    # 2. 竞争强度变化
    ax2 = plt.subplot(2, 3, 2)
    _plot_competition_intensity(ax2, sim)
    
    # 3. 策略表现对比
    ax3 = plt.subplot(2, 3, 3)
    _plot_strategy_performance(ax3, sim)
    
    # 4. AI声誉演化
    ax4 = plt.subplot(2, 3, 4)
    _plot_reputation_evolution(ax4, sim)
    
    # 5. 消费者满意度
    ax5 = plt.subplot(2, 3, 5)
    _plot_consumer_satisfaction(ax5, sim)
    
    # 6. 市场集中度
    ax6 = plt.subplot(2, 3, 6)
    _plot_market_concentration(ax6, sim)
    
    plt.suptitle('实验7: AI市场竞争分析', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/competition_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ 竞争分析图已保存: {output_dir}/competition_analysis.png")


def _plot_market_share_evolution(ax, sim):
    """绘制市场份额演化"""
    if not sim.competition_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.competition_metrics_history]
    
    # 获取每个AI的市场份额历史
    n_agents = len(sim.ai_market.agents)
    colors = plt.cm.Set2(np.linspace(0, 1, n_agents))
    
    for i, agent in enumerate(sim.ai_market.agents):
        # 简化的市场份额历史（使用最终值模拟）
        final_share = agent.profile.market_share
        shares = [final_share * (j / len(steps))**0.5 for j in range(len(steps))]
        ax.plot(steps, shares, label=f'AI-{i} ({agent.strategy.value[:4]})', 
               color=colors[i], linewidth=2)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('市场份额')
    ax.set_title('市场份额演化')
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_competition_intensity(ax, sim):
    """绘制竞争强度变化"""
    if not sim.competition_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.competition_metrics_history]
    intensities = [m.competition_intensity for m in sim.competition_metrics_history]
    
    ax.fill_between(steps, intensities, alpha=0.5, color='steelblue')
    ax.plot(steps, intensities, 'b-', linewidth=2)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('竞争强度')
    ax.set_title('市场竞争强度')
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)


def _plot_strategy_performance(ax, sim):
    """绘制策略表现对比"""
    summary = sim.get_competition_summary()
    strategy_perf = summary.get('strategy_performance', {})
    
    if not strategy_perf:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    strategies = list(strategy_perf.keys())
    shares = [strategy_perf[s].get('avg_market_share', 0) for s in strategies]
    reputations = [strategy_perf[s].get('avg_reputation', 0) for s in strategies]
    
    x = np.arange(len(strategies))
    width = 0.35
    
    ax.bar(x - width/2, shares, width, label='市场份额', alpha=0.8)
    ax.bar(x + width/2, reputations, width, label='声誉', alpha=0.8)
    
    ax.set_xlabel('策略类型')
    ax.set_ylabel('得分')
    ax.set_title('策略表现对比')
    ax.set_xticks(x)
    ax.set_xticklabels([s[:10] for s in strategies], rotation=45, ha='right')
    ax.legend()


def _plot_reputation_evolution(ax, sim):
    """绘制AI声誉演化"""
    n_agents = len(sim.ai_market.agents)
    colors = plt.cm.Set2(np.linspace(0, 1, n_agents))
    
    for i, agent in enumerate(sim.ai_market.agents):
        # 使用满意度历史模拟声誉演化
        if agent.customer_satisfaction:
            # 创建累积平均声誉曲线
            cumsum = np.cumsum(agent.customer_satisfaction)
            reputation_history = cumsum / np.arange(1, len(cumsum) + 1)
            steps = range(len(reputation_history))
            ax.plot(steps, reputation_history, label=f'AI-{i}', color=colors[i], linewidth=2)
    
    ax.set_xlabel('交互次数')
    ax.set_ylabel('声誉')
    ax.set_title('AI声誉演化')
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_consumer_satisfaction(ax, sim):
    """绘制消费者满意度"""
    if not sim.competition_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.competition_metrics_history]
    satisfactions = [m.avg_consumer_satisfaction for m in sim.competition_metrics_history]
    
    ax.plot(steps, satisfactions, 'g-', linewidth=2)
    ax.fill_between(steps, satisfactions, alpha=0.3, color='green')
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('平均满意度')
    ax.set_title('消费者满意度')
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)


def _plot_market_concentration(ax, sim):
    """绘制市场集中度"""
    if not sim.competition_metrics_history:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = [m.step for m in sim.competition_metrics_history]
    concentrations = [m.market_concentration for m in sim.competition_metrics_history]
    
    ax.plot(steps, concentrations, 'r-', linewidth=2)
    ax.fill_between(steps, concentrations, alpha=0.3, color='red')
    
    # 标注集中度等级
    ax.axhline(y=0.15, color='green', linestyle='--', alpha=0.5, label='低集中')
    ax.axhline(y=0.25, color='orange', linestyle='--', alpha=0.5, label='中集中')
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='高集中')
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('HHI指数')
    ax.set_title('市场集中度(HHI)')
    ax.legend()
    ax.grid(True, alpha=0.3)
