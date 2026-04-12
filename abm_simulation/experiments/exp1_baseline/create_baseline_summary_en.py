"""
基线实验综合可视化 - 将所有图表合并到一张图上（完整英文版）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# 添加项目根目录（abm_simulation/）到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from visualization.chinese_font import setup_chinese_font
from config import RESULTS
setup_chinese_font()


# 语言配置
TEXT_CONFIG = {
    'zh': {
        'title': '实验 1: 基线模型 (Ising-D-I-B) - 综合分析',
        'initial_dist': '(a) 初始等级分布',
        'final_dist': '(b) 最终等级分布',
        'level_evolution': '(c) 依赖等级演化',
        'magnetization': '(d) Ising 磁化强度',
        'coupling': '(e) 社会影响强度演化',
        'phase_transition': 'Ising 相变分析',
        'satisfaction': '(f) 平均满意度演化',
        'ai_usage': 'AI 使用与错误率',
        'network': '(g) 小世界网络特征',
        'agent_count': '智能体数量',
        'step': '仿真步数',
        'coupling_strength': '耦合强度',
        'magnetization_label': '磁化强度',
        'satisfaction_label': '满意度',
        'ai_usage_rate': 'AI 使用率',
        'error_rate': '错误率',
        'final': '最终',
        'mean': '平均',
        'critical': '临界值',
        'avg_degree': '平均度数',
        'clustering_coef': '聚类系数',
        'path_length': '路径长度',
    },
    'en': {
        'title': 'Experiment 1: Baseline Model (Ising-D-I-B) - Comprehensive Analysis',
        'initial_dist': '(a) Initial Level Distribution',
        'final_dist': '(b) Final Level Distribution',
        'level_evolution': '(c) Dependency Level Evolution',
        'magnetization': '(d) Ising Magnetization',
        'coupling': '(e) Social Influence Strength Evolution',
        'phase_transition': 'Ising Phase Transition Analysis',
        'satisfaction': '(f) Average Satisfaction Evolution',
        'ai_usage': 'AI Usage & Error Rate',
        'network': '(g) Small-World Network Features',
        'agent_count': 'Agent Count',
        'step': 'Simulation Step',
        'coupling_strength': 'Coupling Strength',
        'magnetization_label': 'Magnetization',
        'satisfaction_label': 'Satisfaction',
        'ai_usage_rate': 'AI Usage Rate',
        'error_rate': 'Error Rate',
        'final': 'Final',
        'mean': 'Mean',
        'critical': 'Critical',
        'avg_degree': 'Avg Degree',
        'clustering_coef': 'Clustering Coef',
        'path_length': 'Path Length',
    }
}


def create_baseline_summary(sim, results, output_dir: str = None, en: bool = False):
    """
    创建基线实验的综合总结图
    
    Args:
        sim: 基线仿真对象
        results: 结果统计
        output_dir: 输出目录
        en: True=英文, False=中文 (默认)
    """
    if output_dir is None:
        output_dir = RESULTS["exp1"]
    os.makedirs(output_dir, exist_ok=True)
    
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    # 等级名称
    if en:
        level_names_short = ['L1\nAutonomous', 'L2\nInfo Assist', 'L3\nSemi-delegate', 'L4\nHigh Depend', 'L5\nFull Agency']
        level_names_line = ['L1 Autonomous', 'L2 Info Assist', 'L3 Semi-delegate', 'L4 High Depend', 'L5 Full Agency']
    else:
        level_names_short = ['L1\n自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
        level_names_line = ['L1 自主', 'L2 信息辅助', 'L3 半委托', 'L4 高度依赖', 'L5 完全代理']
    
    # 创建大型画布 (3 行 3 列)
    fig = plt.figure(figsize=(18, 15))
    fig.suptitle(text['title'], fontsize=20, fontweight='bold', y=0.98)
    
    # ========== 第一行：依赖等级分布 ==========
    ax1 = plt.subplot(3, 3, 1)
    _plot_initial_level_distribution(ax1, sim, level_names_short, text)
    
    ax2 = plt.subplot(3, 3, 2)
    _plot_final_level_distribution(ax2, results, level_names_short, text)
    
    ax3 = plt.subplot(3, 3, 3)
    _plot_level_evolution(ax3, sim, level_names_line, text)
    
    # ========== 第二行：Ising 动力学 ==========
    ax4 = plt.subplot(3, 3, 4)
    _plot_magnetization_evolution(ax4, sim, text)
    
    ax5 = plt.subplot(3, 3, 5)
    _plot_coupling_evolution(ax5, sim, text)
    
    ax6 = plt.subplot(3, 3, 6)
    _plot_phase_transition_analysis(ax6, sim, text)
    
    # ========== 第三行：系统性能 ==========
    ax7 = plt.subplot(3, 3, 7)
    _plot_satisfaction_evolution(ax7, sim, text)
    
    ax8 = plt.subplot(3, 3, 8)
    _plot_ai_usage_and_errors(ax8, sim, text)
    
    ax9 = fig.add_subplot(3, 3, 9, projection='polar')
    _plot_network_topology(ax9, sim, text)
    
    # 调整布局
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # 保存图片
    output_path = f'{output_dir}/baseline_summary.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"[OK] Baseline summary saved: {output_path}")
    return output_path


def _plot_initial_level_distribution(ax, sim, level_names, text):
    """Initial level distribution"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        initial_dist = sim.metrics_history[0].level_distribution
        levels = list(range(1, 6))
        counts = [initial_dist.get(l, 0) for l in levels]
        colors = ['#4C72B0', '#5B9BD5', '#55A868', '#DD8452', '#C44E52']
        
        bars = ax.bar(level_names, counts, color=colors, edgecolor='black', alpha=0.8, linewidth=0.5)
        ax.set_ylabel(text['agent_count'], fontsize=11)
        ax.set_title(text['initial_dist'], fontsize=12, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                   f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')


def _plot_final_level_distribution(ax, results, level_names, text):
    """Final level distribution"""
    final_dist = results['final_level_distribution']
    levels = list(range(1, 6))
    counts = [final_dist.get(l, 0) for l in levels]
    colors = ['#4C72B0', '#5B9BD5', '#55A868', '#DD8452', '#C44E52']
            
    bars = ax.bar(level_names, counts, color=colors, edgecolor='black', alpha=0.8, linewidth=0.5)
    ax.set_ylabel(text['agent_count'], fontsize=11)
    ax.set_title(text['final_dist'], fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
               f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')


def _plot_level_evolution(ax, sim, level_names, text):
    """Level evolution"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        
        levels_data = {i: [] for i in range(1, 6)}
        for m in sim.metrics_history[::10]:
            for level in range(1, 6):
                levels_data[level].append(m.level_distribution.get(level, 0))
        
        colors = ['#4C72B0', '#5B9BD5', '#55A868', '#DD8452', '#C44E52']
            
        for level, color, label in zip(range(1, 6), colors, level_names):
            ax.plot(steps, levels_data[level], label=label, color=color, linewidth=2, alpha=0.7)
        
        ax.set_xlabel(text['step'], fontsize=11)
        ax.set_ylabel(text['agent_count'], fontsize=11)
        ax.set_title(text['level_evolution'], fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)


def _plot_magnetization_evolution(ax, sim, text):
    """Magnetization evolution"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        magnetization = [m.magnetization for m in sim.metrics_history[::10]]
        
        ax.plot(steps, magnetization, color='#4C72B0', linewidth=2)
        ax.axhline(y=0, color='#95A5A6', linestyle='--', linewidth=0.5)
        ax.set_xlabel(text['step'], fontsize=11)
        ax.set_ylabel(text['magnetization_label'], fontsize=11)
        ax.set_title(text['magnetization'], fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        final_mag = magnetization[-1]
        ax.text(0.95, 0.95, f'{text["final"]}: {final_mag:.3f}', transform=ax.transAxes,
               fontsize=10, ha='right', va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


def _plot_coupling_evolution(ax, sim, text):
    """Coupling strength evolution"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        coupling = [m.coupling_strength for m in sim.metrics_history[::10]]
        
        ax.plot(steps, coupling, color='#55A868', linewidth=2)
        ax.set_xlabel(text['step'], fontsize=11)
        ax.set_ylabel(text['coupling_strength'], fontsize=11)
        ax.set_title(text['coupling'], fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        critical_coupling = 0.1667
        ax.axhline(y=critical_coupling, color='red', linestyle=':', linewidth=1.5, label=f'{text["critical"]}: {critical_coupling:.3f}')
        ax.legend(fontsize=9)


def _plot_phase_transition_analysis(ax, sim, text):
    """Phase transition analysis"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        coupling = [m.coupling_strength for m in sim.metrics_history[::10]]
        magnetization = [m.magnetization for m in sim.metrics_history[::10]]
        
        ax1 = ax
        ax2 = ax.twinx()
        
        line1 = ax1.plot(steps, coupling, color='#55A868', label=text['coupling_strength'], linewidth=2, alpha=0.8)
        line2 = ax2.plot(steps, magnetization, color='#4C72B0', label=text['magnetization_label'], linewidth=2, alpha=0.8, linestyle='--')
        
        ax1.set_xlabel(text['step'], fontsize=11)
        ax1.set_ylabel(text['coupling_strength'], fontsize=11, color='green')
        ax2.set_ylabel(text['magnetization_label'], fontsize=11, color='blue')
        ax1.set_title(text['phase_transition'], fontsize=12, fontweight='bold')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=9)
        
        ax1.grid(True, alpha=0.3)


def _plot_satisfaction_evolution(ax, sim, text):
    """Satisfaction evolution"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        satisfaction = [m.avg_satisfaction for m in sim.metrics_history[::10]]
        
        ax.fill_between(steps, 0, satisfaction, alpha=0.6, color='#DD8452')
        ax.plot(steps, satisfaction, color='#DD8452', linewidth=2)
        ax.set_xlabel(text['step'], fontsize=11)
        ax.set_ylabel(text['satisfaction_label'], fontsize=11)
        ax.set_title(text['satisfaction'], fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        mean_sat = np.mean(satisfaction)
        ax.text(0.05, 0.95, f'{text["mean"]}: {mean_sat:.3f}', transform=ax.transAxes,
               fontsize=10, ha='left', va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


def _plot_ai_usage_and_errors(ax, sim, text):
    """AI usage and error rate"""
    if hasattr(sim, 'metrics_history') and sim.metrics_history:
        steps = [m.step for m in sim.metrics_history[::10]]
        ai_usage = [m.ai_usage_rate for m in sim.metrics_history[::10]]
        error_rate = [m.error_rate for m in sim.metrics_history[::10]]
        
        ax1 = ax
        ax2 = ax.twinx()
        
        line1 = ax1.plot(steps, ai_usage, 'r-', label=text['ai_usage_rate'], linewidth=2, alpha=0.7)
        line2 = ax2.plot(steps, error_rate, 'purple', label=text['error_rate'], linewidth=2, alpha=0.7)
        
        ax1.set_xlabel(text['step'], fontsize=11)
        ax1.set_ylabel(text['ai_usage_rate'], fontsize=11, color='red')
        ax2.set_ylabel(text['error_rate'], fontsize=11, color='purple')
        ax1.set_title(text['ai_usage'], fontsize=12, fontweight='bold')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right', fontsize=9)
        
        ax1.grid(True, alpha=0.3)


def _plot_network_topology(ax, sim, text):
    """Network topology features"""
    if hasattr(sim, 'network') and sim.network:
        import networkx as nx
        graph = sim.network.graph
        
        avg_degree = np.mean([d for n, d in graph.degree()])
        clustering_coef = nx.average_clustering(graph) if hasattr(nx, 'average_clustering') else 0
        avg_path_length = nx.average_shortest_path_length(graph) if nx.is_connected(graph) else float('inf')
        
        degree_normalized = min(avg_degree / 20.0, 1.0)
        clustering_normalized = clustering_coef
        path_normalized = max(0, min(1.0 - (avg_path_length - 3.0) / 5.0, 1.0))
        
        categories = [text['avg_degree'], text['clustering_coef'], text['path_length']]
        values = [degree_normalized, clustering_normalized, path_normalized]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        ax.plot(angles, values, color='#4C72B0', linewidth=2, marker='o', markersize=8)
        ax.fill(angles, values, color='#4C72B0', alpha=0.15)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 1.15)
        ax.set_title(text['network'], fontsize=12, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        
        raw_values = [avg_degree, clustering_coef, avg_path_length]
        for angle, val_norm, val_raw in zip(angles[:-1], values[:-1], raw_values):
            ax.text(angle, val_norm + 0.08, f'{val_raw:.2f}', 
                   ha='center', fontsize=9, fontweight='bold', color='#2C3E50')
