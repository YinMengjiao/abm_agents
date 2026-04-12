"""
对比实验可视化：调查数据驱动 vs 理论假设初始化
生成学术论文级别的对比图表
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.gridspec import GridSpec
import json
import os
import sys

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Microsoft JhengHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 顶刊柔和配色
COLORS = {
    'survey': '#2E86AB',      # 蓝色 - 调查数据
    'theoretical': '#A23B72', # 紫色 - 理论假设
    'survey_fill': 'rgba(46, 134, 171, 0.2)',
    'theoretical_fill': 'rgba(162, 59, 114, 0.2)',
    'levels': ['#4C72B0', '#5B9BD5', '#55A868', '#DD8452', '#C44E52']
}


def load_results(results_dir: str = None) -> dict:
    """加载实验结果"""
    if results_dir is None:
        results_dir = os.path.join(os.path.dirname(__file__), 'results')
    
    json_path = os.path.join(results_dir, 'comparison_results.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"✓ 已加载实验结果: {json_path}")
    print(f"  实验组: {len(results['results_survey'])} 次运行")
    print(f"  对照组: {len(results['results_theoretical'])} 次运行")
    
    return results


def plot_initial_distribution_comparison(ax, results):
    """绘制初始分布对比"""
    levels = [1, 2, 3, 4, 5]
    level_labels = ['L1\n完全自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
    
    survey_dist = [results['parameters']['survey_distribution'][str(l)] * 100 for l in levels]
    theoretical_dist = [results['parameters']['theoretical_distribution'][str(l)] * 100 for l in levels]
    
    x = np.arange(len(levels))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, theoretical_dist, width, label='理论假设', 
                   color='#A23B72', alpha=0.7, edgecolor='black', linewidth=0.8)
    bars2 = ax.bar(x + width/2, survey_dist, width, label='调查数据', 
                   color='#2E86AB', alpha=0.7, edgecolor='black', linewidth=0.8)
    
    ax.set_ylabel('比例 (%)', fontsize=11)
    ax.set_title('(a) 初始等级分布对比', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(level_labels, fontsize=9)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, axis='y', alpha=0.3)
    ax.set_ylim(0, max(max(survey_dist), max(theoretical_dist)) * 1.2)
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}%', ha='center', va='bottom', fontsize=8)


def plot_final_distribution_comparison(ax, results):
    """绘制最终分布对比"""
    levels = [1, 2, 3, 4, 5]
    level_labels = ['L1\n完全自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
    
    # 计算平均值
    survey_final = []
    theoretical_final = []
    
    for level in levels:
        survey_counts = [r['final_distribution'].get(str(level), 0) for r in results['results_survey']]
        theoretical_counts = [r['final_distribution'].get(str(level), 0) for r in results['results_theoretical']]
        survey_final.append(np.mean(survey_counts))
        theoretical_final.append(np.mean(theoretical_counts))
    
    x = np.arange(len(levels))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, theoretical_final, width, label='理论假设', 
                   color='#A23B72', alpha=0.7, edgecolor='black', linewidth=0.8)
    bars2 = ax.bar(x + width/2, survey_final, width, label='调查数据', 
                   color='#2E86AB', alpha=0.7, edgecolor='black', linewidth=0.8)
    
    ax.set_ylabel('智能体数量', fontsize=11)
    ax.set_title('(b) 最终等级分布对比 (均值)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(level_labels, fontsize=9)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, axis='y', alpha=0.3)


def plot_evolution_comparison(ax, results):
    """绘制等级演化对比"""
    # 获取第一个运行的演化数据作为示例
    survey_result = results['results_survey'][0]
    theoretical_result = results['results_theoretical'][0]
    
    n_steps = len(survey_result['level_evolution']['1'])
    steps = np.arange(n_steps) * 10  # 每10步采样
    
    # 绘制调查数据
    for level in range(1, 6):
        values = survey_result['level_evolution'][str(level)]
        ax.plot(steps, values, color=COLORS['levels'][level-1], 
               linewidth=2, alpha=0.8, linestyle='-', label=f'L{level} 调查')
    
    # 绘制理论假设（虚线）
    for level in range(1, 6):
        values = theoretical_result['level_evolution'][str(level)]
        ax.plot(steps, values, color=COLORS['levels'][level-1], 
               linewidth=2, alpha=0.5, linestyle='--', label=f'L{level} 理论')
    
    ax.set_xlabel('仿真步数', fontsize=11)
    ax.set_ylabel('智能体数量', fontsize=11)
    ax.set_title('(c) 等级分布演化对比', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8, loc='upper right', ncol=2)
    ax.grid(True, alpha=0.3)


def plot_magnetization_comparison(ax, results):
    """绘制磁化强度演化对比"""
    survey_result = results['results_survey'][0]
    theoretical_result = results['results_theoretical'][0]
    
    n_steps = len(survey_result['magnetization_evolution'])
    steps = np.arange(n_steps) * 10
    
    survey_mag = survey_result['magnetization_evolution']
    theoretical_mag = theoretical_result['magnetization_evolution']
    
    ax.plot(steps, survey_mag, color=COLORS['survey'], linewidth=2.5, 
           label='调查数据', alpha=0.8)
    ax.plot(steps, theoretical_mag, color=COLORS['theoretical'], linewidth=2.5, 
           label='理论假设', alpha=0.8, linestyle='--')
    
    ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax.set_xlabel('仿真步数', fontsize=11)
    ax.set_ylabel('磁化强度 M', fontsize=11)
    ax.set_title('(d) 磁化强度演化对比', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)


def plot_satisfaction_comparison(ax, results):
    """绘制满意度演化对比"""
    survey_result = results['results_survey'][0]
    theoretical_result = results['results_theoretical'][0]
    
    n_steps = len(survey_result['satisfaction_evolution'])
    steps = np.arange(n_steps) * 10
    
    survey_sat = survey_result['satisfaction_evolution']
    theoretical_sat = theoretical_result['satisfaction_evolution']
    
    ax.plot(steps, survey_sat, color=COLORS['survey'], linewidth=2.5, 
           label='调查数据', alpha=0.8)
    ax.plot(steps, theoretical_sat, color=COLORS['theoretical'], linewidth=2.5, 
           label='理论假设', alpha=0.8, linestyle='--')
    
    ax.set_xlabel('仿真步数', fontsize=11)
    ax.set_ylabel('平均满意度', fontsize=11)
    ax.set_title('(e) 满意度演化对比', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)


def plot_metrics_boxplot(ax, results):
    """绘制关键指标箱线图对比"""
    metrics = ['magnetization_final', 'avg_satisfaction', 'ai_usage_rate', 'error_rate']
    metric_labels = ['最终磁化强度', '平均满意度', 'AI使用率', '错误率']
    
    survey_data = []
    theoretical_data = []
    
    for metric in metrics:
        survey_vals = [r[metric] for r in results['results_survey']]
        theoretical_vals = [r[metric] for r in results['results_theoretical']]
        survey_data.append(survey_vals)
        theoretical_data.append(theoretical_vals)
    
    # 归一化到[0,1]便于比较
    survey_data_norm = []
    theoretical_data_norm = []
    
    for i in range(len(metrics)):
        all_vals = survey_data[i] + theoretical_data[i]
        min_val = min(all_vals)
        max_val = max(all_vals)
        if max_val > min_val:
            survey_data_norm.append([(x - min_val) / (max_val - min_val) for x in survey_data[i]])
            theoretical_data_norm.append([(x - min_val) / (max_val - min_val) for x in theoretical_data[i]])
        else:
            survey_data_norm.append([0.5] * len(survey_data[i]))
            theoretical_data_norm.append([0.5] * len(theoretical_data[i]))
    
    positions = np.arange(len(metrics)) * 2
    width = 0.35
    
    bp1 = ax.boxplot(survey_data_norm, positions=positions - width/2, widths=width,
                     patch_artist=True, label='调查数据')
    bp2 = ax.boxplot(theoretical_data_norm, positions=positions + width/2, widths=width,
                     patch_artist=True, label='理论假设')
    
    for patch in bp1['boxes']:
        patch.set_facecolor(COLORS['survey'])
        patch.set_alpha(0.6)
    for patch in bp2['boxes']:
        patch.set_facecolor(COLORS['theoretical'])
        patch.set_alpha(0.6)
    
    ax.set_xticks(positions)
    ax.set_xticklabels(metric_labels, fontsize=9)
    ax.set_ylabel('归一化值', fontsize=11)
    ax.set_title('(f) 关键指标对比 (箱线图)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, axis='y', alpha=0.3)


def create_comparison_visualization(results, output_dir: str = None):
    """创建完整的对比可视化"""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'results')
    
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)
    
    # 创建6个子图
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    ax5 = fig.add_subplot(gs[2, 0])
    ax6 = fig.add_subplot(gs[2, 1])
    
    # 绘制各个子图
    plot_initial_distribution_comparison(ax1, results)
    plot_final_distribution_comparison(ax2, results)
    plot_evolution_comparison(ax3, results)
    plot_magnetization_comparison(ax4, results)
    plot_satisfaction_comparison(ax5, results)
    plot_metrics_boxplot(ax6, results)
    
    # 总标题
    plt.suptitle('初始化方式对比：调查数据驱动 vs 理论假设', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # 保存
    output_path = os.path.join(output_dir, 'initialization_comparison.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\n✓ 对比图已保存: {output_path}")
    
    plt.close()
    return output_path


def main():
    """主函数"""
    # 加载结果
    results = load_results()
    
    # 生成可视化
    output_path = create_comparison_visualization(results)
    
    print(f"\n{'='*70}")
    print(f"可视化完成！")
    print(f"{'='*70}")
    print(f"输出文件: {output_path}")


if __name__ == "__main__":
    main()
