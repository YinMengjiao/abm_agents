"""
基线实验综合可视化 - 将所有图表合并到一张图上
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# 添加项目根目录（abm_simulation/）到路径
# __file__ = .../abm_simulation/experiments/exp1_baseline/create_baseline_summary.py
# 需要三层 dirname 才能到达 abm_simulation/
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from visualization.chinese_font import setup_chinese_font
from config import RESULTS
setup_chinese_font()


def create_baseline_summary(sim, results, output_dir: str = None):
    if output_dir is None:
        output_dir = RESULTS["exp1"]
    """
    创建基线实验的综合总结图
    
    Args:
        sim: 基线仿真对象
        results: 结果统计
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建大型画布 (3 行 3 列)
    fig = plt.figure(figsize=(18, 15))
    fig.suptitle('实验 1: 基线模型 (Ising-D-I-B) - 综合分析', fontsize=20, fontweight='bold', y=0.98)
    
    # ========== 第一行：依赖等级分布 ==========
    # 子图 1: 初始等级分布
    ax1 = plt.subplot(3, 3, 1)
    _plot_initial_level_distribution(ax1, sim)
    
    # 子图 2: 最终等级分布
    ax2 = plt.subplot(3, 3, 2)
    _plot_final_level_distribution(ax2, results)
    
    # 子图 3: 等级演化
    ax3 = plt.subplot(3, 3, 3)
    _plot_level_evolution(ax3, sim)
    
    # ========== 第二行：Ising 动力学 ==========
    # 子图 4: 磁化强度演化
    ax4 = plt.subplot(3, 3, 4)
    _plot_magnetization_evolution(ax4, sim)
    
    # 子图 5: 耦合强度演化
    ax5 = plt.subplot(3, 3, 5)
    _plot_coupling_evolution(ax5, sim)
    
    # 子图 6: Ising 相变分析
    ax6 = plt.subplot(3, 3, 6)
    _plot_phase_transition_analysis(ax6, sim)
    
    # ========== 第三行：系统性能 ==========
    # 子图 7: 满意度演化
    ax7 = plt.subplot(3, 3, 7)
    _plot_satisfaction_evolution(ax7, sim)
    
    # 子图 8: AI 使用率与错误率
    ax8 = plt.subplot(3, 3, 8)
    _plot_ai_usage_and_errors(ax8, sim)
    
    # 子图 9: 网络拓扑特征（雷达图需要 polar 投影）
    ax9 = fig.add_subplot(3, 3, 9, projection='polar')
    _plot_network_topology(ax9, sim)
    
    # 调整布局
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # 保存图片
    output_path = f'{output_dir}/baseline_summary.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"[OK] 基线实验综合图已保存：{output_path}")
    return output_path


def _plot_initial_level_distribution(ax, sim):
    """初始等级分布"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        initial_dist = sim.metrics_history[0].level_distribution
        levels = list(range(1, 6))
        counts = [initial_dist.get(l, 0) for l in levels]
        level_names = ['L1\n自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        bars = ax.bar(level_names, counts, color=colors, edgecolor='black', alpha=0.8)
        ax.set_ylabel('智能体数量', fontsize=11)
        ax.set_title('初始等级分布', fontsize=12, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                   f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')


def _plot_final_level_distribution(ax, results):
    """最终等级分布"""
    final_dist = results['final_level_distribution']
    levels = list(range(1, 6))
    counts = [final_dist.get(l, 0) for l in levels]
    level_names = ['L1\n自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    bars = ax.bar(level_names, counts, color=colors, edgecolor='black', alpha=0.8)
    ax.set_ylabel('智能体数量', fontsize=11)
    ax.set_title('最终等级分布', fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
               f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')


def _plot_level_evolution(ax, sim):
    """等级演化"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        
        # 提取各级别数量
        levels_data = {i: [] for i in range(1, 6)}
        for m in sim.metrics_history[::10]:
            for level in range(1, 6):
                levels_data[level].append(m.level_distribution.get(level, 0))
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        labels = ['L1 自主', 'L2 信息辅助', 'L3 半委托', 'L4 高度依赖', 'L5 完全代理']
        
        for level, color, label in zip(range(1, 6), colors, labels):
            ax.plot(steps, levels_data[level], label=label, color=color, linewidth=2, alpha=0.7)
        
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('智能体数量', fontsize=11)
        ax.set_title('依赖等级演化', fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)


def _plot_magnetization_evolution(ax, sim):
    """磁化强度演化"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        magnetization = [m.magnetization for m in sim.metrics_history[::10]]
        
        ax.plot(steps, magnetization, 'b-', linewidth=2)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('磁化强度', fontsize=11)
        ax.set_title('Ising 磁化强度', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 标注最终值
        final_mag = magnetization[-1]
        ax.text(0.95, 0.95, f'最终：{final_mag:.3f}', transform=ax.transAxes,
               fontsize=10, ha='right', va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


def _plot_coupling_evolution(ax, sim):
    """耦合强度演化"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        coupling = [m.coupling_strength for m in sim.metrics_history[::10]]
        
        ax.plot(steps, coupling, 'g-', linewidth=2)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('耦合强度', fontsize=11)
        ax.set_title('社会影响强度演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 标注临界值
        critical_coupling = 0.1667  # 理论临界值
        ax.axhline(y=critical_coupling, color='red', linestyle=':', linewidth=1.5, label=f'临界值：{critical_coupling:.3f}')
        ax.legend(fontsize=9)


def _plot_phase_transition_analysis(ax, sim):
    """相变分析"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        coupling = [m.coupling_strength for m in sim.metrics_history[::10]]
        magnetization = [m.magnetization for m in sim.metrics_history[::10]]
        
        # 创建双 y 轴
        ax1 = ax
        ax2 = ax.twinx()
        
        line1 = ax1.plot(steps, coupling, 'g-', label='耦合强度', linewidth=2, alpha=0.7)
        line2 = ax2.plot(steps, magnetization, 'b--', label='磁化强度', linewidth=2, alpha=0.7)
        
        ax1.set_xlabel('仿真步数', fontsize=11)
        ax1.set_ylabel('耦合强度', fontsize=11, color='green')
        ax2.set_ylabel('磁化强度', fontsize=11, color='blue')
        ax1.set_title('Ising 相变分析', fontsize=12, fontweight='bold')
        
        # 合并图例
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=9)
        
        ax1.grid(True, alpha=0.3)


def _plot_satisfaction_evolution(ax, sim):
    """满意度演化"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        satisfaction = [m.avg_satisfaction for m in sim.metrics_history[::10]]
        
        ax.fill_between(steps, 0, satisfaction, alpha=0.7, color='orange')
        ax.plot(steps, satisfaction, 'orange', linewidth=2)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('满意度', fontsize=11)
        ax.set_title('平均满意度演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 标注统计值
        mean_sat = np.mean(satisfaction)
        ax.text(0.05, 0.95, f'平均：{mean_sat:.3f}', transform=ax.transAxes,
               fontsize=10, ha='left', va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


def _plot_ai_usage_and_errors(ax, sim):
    """AI 使用率与错误率"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        ai_usage = [m.ai_usage_rate for m in sim.metrics_history[::10]]
        error_rate = [m.error_rate for m in sim.metrics_history[::10]]
        
        # 创建双 y 轴
        ax1 = ax
        ax2 = ax.twinx()
        
        line1 = ax1.plot(steps, ai_usage, 'r-', label='AI 使用率', linewidth=2, alpha=0.7)
        line2 = ax2.plot(steps, error_rate, 'purple', label='错误率', linewidth=2, alpha=0.7)
        
        ax1.set_xlabel('仿真步数', fontsize=11)
        ax1.set_ylabel('AI 使用率', fontsize=11, color='red')
        ax2.set_ylabel('错误率', fontsize=11, color='purple')
        ax1.set_title('AI 使用与错误率', fontsize=12, fontweight='bold')
        
        # 合并图例
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right', fontsize=9)
        
        ax1.grid(True, alpha=0.3)


def _plot_network_topology(ax, sim):
    """网络拓扑特征"""
    if hasattr(sim, 'network') and sim.network:
        graph = sim.network.graph
        
        # 计算网络指标
        avg_degree = np.mean([d for n, d in graph.degree()])
        clustering_coef = nx.average_clustering(graph) if hasattr(nx, 'average_clustering') else 0
        avg_path_length = nx.average_shortest_path_length(graph) if nx.is_connected(graph) else float('inf')
        
        # 绘制雷达图
        categories = ['平均度数', '聚类系数', '路径长度 (归一化)']
        values = [avg_degree, clustering_coef, min(avg_path_length / 10, 1.0)]  # 归一化
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        ax.plot(angles, values, 'b-', linewidth=2, marker='o', markersize=8)
        ax.fill(angles, values, 'b', alpha=0.1)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 1)
        ax.set_title('小世界网络特征', fontsize=12, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        
        # 添加数值标签
        for angle, val in zip(angles[:-1], [avg_degree, clustering_coef, min(avg_path_length / 10, 1.0)]):
            ax.text(angle, val + 0.05, f'{val:.3f}', ha='center', fontsize=9)


# 需要导入 networkx
try:
    import networkx as nx
except ImportError:
    nx = None
    print("警告：未安装 networkx，网络拓扑图可能无法显示")
