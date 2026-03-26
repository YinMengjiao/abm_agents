"""
实验 2 综合可视化 - 将所有图表合并到一张图上
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# 添加项目根目录并导入中文字体配置
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from visualization.chinese_font import setup_chinese_font
setup_chinese_font()


def create_experiment2_summary(baseline_sim, memory_sim, baseline_results, memory_results, 
                                output_dir: str = "results/all_figures"):
    """
    创建实验 2 的综合总结图
    
    Args:
        baseline_sim: 基线仿真对象
        memory_sim: 记忆增强仿真对象
        baseline_results: 基线结果统计
        memory_results: 记忆增强结果统计
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建大型画布 (4 行 3 列)
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('实验 2: 消费者记忆机制 - 综合分析', fontsize=20, fontweight='bold', y=0.98)
    
    # ========== 第一行：依赖等级对比 ==========
    # 子图 1: 基线模型等级分布
    ax1 = plt.subplot(4, 3, 1)
    _plot_baseline_level_distribution(ax1, baseline_results)
    
    # 子图 2: 记忆增强模型等级分布
    ax2 = plt.subplot(4, 3, 2)
    _plot_memory_level_distribution(ax2, memory_results)
    
    # 子图 3: 差异对比
    ax3 = plt.subplot(4, 3, 3)
    _plot_level_difference(ax3, baseline_results, memory_results)
    
    # ========== 第二行：关键指标演化 ==========
    # 子图 4: 满意度演化
    ax4 = plt.subplot(4, 3, 4)
    _plot_satisfaction_evolution(ax4, baseline_sim, memory_sim)
    
    # 子图 5: AI 使用率演化
    ax5 = plt.subplot(4, 3, 5)
    _plot_ai_usage_evolution(ax5, baseline_sim, memory_sim)
    
    # 子图 6: 错误率演化
    ax6 = plt.subplot(4, 3, 6)
    _plot_error_rate_evolution(ax6, baseline_sim, memory_sim)
    
    # ========== 第三行：记忆动态 ==========
    # 子图 7: 信任度演化
    ax7 = plt.subplot(4, 3, 7)
    _plot_trust_dynamics(ax7, memory_results)
    
    # 子图 8: 连续错误数
    ax8 = plt.subplot(4, 3, 8)
    _plot_consecutive_errors(ax8, memory_results)
    
    # 子图 9: 记忆容量使用
    ax9 = plt.subplot(4, 3, 9)
    _plot_memory_capacity(ax9, memory_results)
    
    # ========== 第四行：综合分析 ==========
    # 子图 10: 雷达图对比
    ax10 = plt.subplot(4, 3, 10, projection='polar')
    _plot_radar_comparison(ax10, baseline_results, memory_results)
    
    # 子图 11: 磁化强度对比
    ax11 = plt.subplot(4, 3, 11)
    _plot_magnetization_comparison(ax11, baseline_sim, memory_sim)
    
    # 子图 12: 最终状态汇总
    ax12 = plt.subplot(4, 3, 12)
    _plot_final_summary(ax12, baseline_results, memory_results)
    
    # 调整布局
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # 保存图片
    output_path = f'{output_dir}/experiment2_summary.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"[OK] 实验 2 综合图已保存：{output_path}")
    return output_path


def _plot_baseline_level_distribution(ax, results):
    """基线模型等级分布"""
    dist = results['final_level_distribution']
    levels = list(range(1, 6))
    counts = [dist.get(l, 0) for l in levels]
    level_names = ['L1\n自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    bars = ax.bar(level_names, counts, color=colors, edgecolor='black', alpha=0.8)
    ax.set_ylabel('智能体数量', fontsize=11)
    ax.set_title('基线模型 - 最终等级分布', fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
               f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')


def _plot_memory_level_distribution(ax, results):
    """记忆增强模型等级分布"""
    dist = results['final_level_distribution']
    levels = list(range(1, 6))
    counts = [dist.get(l, 0) for l in levels]
    level_names = ['L1\n自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    bars = ax.bar(level_names, counts, color=colors, edgecolor='black', alpha=0.8)
    ax.set_ylabel('智能体数量', fontsize=11)
    ax.set_title('记忆增强模型 - 最终等级分布', fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
               f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')


def _plot_level_difference(ax, baseline, memory):
    """等级差异对比"""
    baseline_dist = baseline['final_level_distribution']
    memory_dist = memory['final_level_distribution']
    
    levels = list(range(1, 6))
    level_names = ['L1\n自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
    
    differences = [memory_dist.get(l, 0) - baseline_dist.get(l, 0) for l in levels]
    colors = ['green' if d > 0 else 'red' if d < 0 else 'gray' for d in differences]
    
    bars = ax.bar(level_names, differences, color=colors, edgecolor='black', alpha=0.8)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_ylabel('数量变化', fontsize=11)
    ax.set_title('记忆效应 (记忆 - 基线)', fontsize=12, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    
    for bar, diff in zip(bars, differences):
        va = 'bottom' if diff >= 0 else 'top'
        offset = 5 if diff >= 0 else -5
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + offset,
               f'{diff:+d}', ha='center', va=va, fontsize=10, fontweight='bold')


def _plot_satisfaction_evolution(ax, baseline_sim, memory_sim):
    """满意度演化"""
    if hasattr(baseline_sim, 'metrics_history') and baseline_sim.metrics_history:
        steps = [m.step for m in baseline_sim.metrics_history[::10]]
        baseline_sat = [m.avg_satisfaction for m in baseline_sim.metrics_history[::10]]
        memory_sat = [m.avg_satisfaction for m in memory_sim.metrics_history[::10]]
        
        ax.plot(steps, baseline_sat, 'b-', label='基线', linewidth=2, alpha=0.7)
        ax.plot(steps, memory_sat, 'r--', label='记忆增强', linewidth=2, alpha=0.7)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('满意度', fontsize=11)
        ax.set_title('满意度演化', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)


def _plot_ai_usage_evolution(ax, baseline_sim, memory_sim):
    """AI 使用率演化"""
    if hasattr(baseline_sim, 'metrics_history') and baseline_sim.metrics_history:
        steps = [m.step for m in baseline_sim.metrics_history[::10]]
        baseline_use = [m.ai_usage_rate for m in baseline_sim.metrics_history[::10]]
        memory_use = [m.ai_usage_rate for m in memory_sim.metrics_history[::10]]
        
        ax.plot(steps, baseline_use, 'b-', label='基线', linewidth=2, alpha=0.7)
        ax.plot(steps, memory_use, 'r--', label='记忆增强', linewidth=2, alpha=0.7)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('AI 使用率', fontsize=11)
        ax.set_title('AI 使用率演化', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)


def _plot_error_rate_evolution(ax, baseline_sim, memory_sim):
    """错误率演化"""
    if hasattr(baseline_sim, 'metrics_history') and baseline_sim.metrics_history:
        steps = [m.step for m in baseline_sim.metrics_history[::10]]
        baseline_err = [m.error_rate for m in baseline_sim.metrics_history[::10]]
        memory_err = [m.error_rate for m in memory_sim.metrics_history[::10]]
        
        ax.plot(steps, baseline_err, 'b-', label='基线', linewidth=2, alpha=0.7)
        ax.plot(steps, memory_err, 'r--', label='记忆增强', linewidth=2, alpha=0.7)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('错误率', fontsize=11)
        ax.set_title('错误率演化', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)


def _plot_trust_dynamics(ax, memory_results):
    """信任动态"""
    if 'memory_dynamics' in memory_results:
        trust_trend = memory_results['memory_dynamics'].get('trust_trend', [])
        if trust_trend:
            steps = list(range(len(trust_trend)))
            ax.plot(steps, trust_trend, 'g-', linewidth=2)
            ax.set_xlabel('仿真步数', fontsize=11)
            ax.set_ylabel('信任度', fontsize=11)
            ax.set_title('动态信任演化', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)


def _plot_consecutive_errors(ax, memory_results):
    """连续错误数"""
    if 'memory_dynamics' in memory_results:
        errors_trend = memory_results['memory_dynamics'].get('consecutive_errors_trend', [])
        if errors_trend:
            steps = list(range(len(errors_trend)))
            ax.plot(steps, errors_trend, 'r-', linewidth=2)
            ax.set_xlabel('仿真步数', fontsize=11)
            ax.set_ylabel('连续错误数', fontsize=11)
            ax.set_title('连续错误趋势', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)


def _plot_memory_capacity(ax, memory_results):
    """记忆容量使用"""
    if 'memory_dynamics' in memory_results:
        capacity = memory_results['memory_dynamics'].get('memory_capacity_usage', [])
        if capacity:
            steps = list(range(len(capacity)))
            ax.fill_between(steps, 0, capacity, alpha=0.7, color='purple')
            ax.set_xlabel('仿真步数', fontsize=11)
            ax.set_ylabel('使用率', fontsize=11)
            ax.set_title('记忆容量使用', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)


def _plot_radar_comparison(ax, baseline, memory):
    """雷达图对比"""
    categories = ['满意度', 'AI 使用率', 'L3 占比', 'L4 占比', '稳定性']
    
    # 计算各项指标
    base_vals = [
        baseline['satisfaction']['mean'],
        baseline['ai_usage'],
        baseline['final_level_distribution'].get(3, 0) / 500,
        baseline['final_level_distribution'].get(4, 0) / 500,
        abs(baseline['magnetization_trend']['final'])
    ]
    
    mem_vals = [
        memory['satisfaction']['mean'],
        memory['ai_usage'],
        memory['final_level_distribution'].get(3, 0) / 500,
        memory['final_level_distribution'].get(4, 0) / 500,
        abs(memory['magnetization_trend']['final'])
    ]
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    base_vals += base_vals[:1]
    mem_vals += mem_vals[:1]
    angles += angles[:1]
    
    ax.plot(angles, base_vals, 'b-', linewidth=2, label='基线', alpha=0.7)
    ax.fill(angles, base_vals, 'b', alpha=0.1)
    
    ax.plot(angles, mem_vals, 'r--', linewidth=2, label='记忆增强', alpha=0.7)
    ax.fill(angles, mem_vals, 'r', alpha=0.1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_title('综合指标雷达图', fontsize=12, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
    ax.grid(True, alpha=0.3)


def _plot_magnetization_comparison(ax, baseline_sim, memory_sim):
    """磁化强度对比"""
    if hasattr(baseline_sim, 'metrics_history') and baseline_sim.metrics_history:
        steps = [m.step for m in baseline_sim.metrics_history[::10]]
        baseline_mag = [m.magnetization for m in baseline_sim.metrics_history[::10]]
        memory_mag = [m.magnetization for m in memory_sim.metrics_history[::10]]
        
        ax.plot(steps, baseline_mag, 'b-', label='基线', linewidth=2, alpha=0.7)
        ax.plot(steps, memory_mag, 'r--', label='记忆增强', linewidth=2, alpha=0.7)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('磁化强度', fontsize=11)
        ax.set_title('Ising 磁化强度', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)


def _plot_final_summary(ax, baseline, memory):
    """最终状态汇总"""
    categories = ['满意度', 'AI 使用率', '错误率']
    
    base_vals = [
        baseline['satisfaction']['mean'],
        baseline['ai_usage'],
        baseline['error_rate']
    ]
    
    mem_vals = [
        memory['satisfaction']['mean'],
        memory['ai_usage'],
        memory['error_rate']
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax.bar(x - width/2, base_vals, width, label='基线', color='blue', alpha=0.7)
    ax.bar(x + width/2, mem_vals, width, label='记忆增强', color='red', alpha=0.7)
    
    ax.set_ylabel('数值', fontsize=11)
    ax.set_title('最终指标对比', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(fontsize=10)
    ax.grid(True, axis='y', alpha=0.3)


if __name__ == "__main__":
    print("提示：此脚本需要从运行实验 2 的脚本中调用")
    print("请在 run_comparison.py 中导入并使用 create_experiment2_summary 函数")
