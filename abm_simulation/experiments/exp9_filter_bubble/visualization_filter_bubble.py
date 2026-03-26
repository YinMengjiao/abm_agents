"""
实验 9 可视化：过滤气泡
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


def visualize_filter_bubble_results(analyzer, results, output_dir: str):
    """可视化过滤气泡结果"""
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. 各依赖等级多样性对比
    ax1 = plt.subplot(2, 3, 1)
    _plot_diversity_by_level(ax1, results)
    
    # 2. 多样性分布直方图
    ax2 = plt.subplot(2, 3, 2)
    _plot_diversity_distribution(ax2, results)
    
    # 3. 探索率对比
    ax3 = plt.subplot(2, 3, 3)
    _plot_exploration_rate(ax3, results)
    
    # 4. 类别覆盖热力图
    ax4 = plt.subplot(2, 3, 4)
    _plot_category_coverage(ax4, analyzer, results)
    
    # 5. 过滤气泡强度
    ax5 = plt.subplot(2, 3, 5)
    _plot_filter_bubble_strength(ax5, results)
    
    # 6. 个体多样性散点图
    ax6 = plt.subplot(2, 3, 6)
    _plot_individual_diversity(ax6, results)
    
    plt.suptitle('实验 9: 过滤气泡与选择多样性分析', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 为 suptitle 留出空间
    plt.savefig(f'{output_dir}/filter_bubble_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 过滤气泡分析图已保存：{output_dir}/filter_bubble_analysis.png")


def _plot_diversity_by_level(ax, results):
    """绘制各依赖等级多样性对比"""
    diversity_by_level = results['population_metrics']['diversity_by_level']
    
    levels = list(diversity_by_level.keys())
    diversities = list(diversity_by_level.values())
    
    colors = plt.cm.RdYlGn(np.array(diversities))
    bars = ax.bar([f'L{l}' for l in levels], diversities, color=colors, alpha=0.8)
    
    ax.set_ylabel('多样性得分')
    ax.set_title('各依赖等级选择多样性')
    ax.set_ylim(0, 1)
    
    # 添加数值标签
    for bar, div in zip(bars, diversities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{div:.3f}', ha='center', va='bottom', fontsize=9)


def _plot_diversity_distribution(ax, results):
    """绘制多样性分布直方图"""
    individual_metrics = results['individual_metrics']
    diversity_scores = [m['diversity_score'] for m in individual_metrics if 'diversity_score' in m]
    
    if diversity_scores:
        ax.hist(diversity_scores, bins=20, alpha=0.7, color='steelblue', edgecolor='black')
        ax.axvline(x=np.mean(diversity_scores), color='red', linestyle='--', 
                  linewidth=2, label=f'均值: {np.mean(diversity_scores):.3f}')
    
    ax.set_xlabel('多样性得分')
    ax.set_ylabel('消费者数量')
    ax.set_title('多样性分布')
    ax.legend()


def _plot_exploration_rate(ax, results):
    """绘制探索率对比"""
    individual_metrics = results['individual_metrics']
    
    # 按依赖等级分组
    exploration_by_level = {i: [] for i in range(1, 6)}
    
    for m in individual_metrics:
        if 'exploration_rate' in m and 'dependency_level' in m:
            level = m['dependency_level']
            exploration_by_level[level].append(m['exploration_rate'])
    
    levels = []
    avg_exploration = []
    
    for level in range(1, 6):
        if exploration_by_level[level]:
            levels.append(f'L{level}')
            avg_exploration.append(np.mean(exploration_by_level[level]))
    
    colors = plt.cm.RdYlGn_r(np.array(avg_exploration))
    bars = ax.bar(levels, avg_exploration, color=colors, alpha=0.8)
    
    ax.set_ylabel('平均探索率')
    ax.set_title('各等级探索行为')
    ax.set_ylim(0, 1)
    
    # 添加趋势线
    if len(avg_exploration) > 1:
        z = np.polyfit(range(len(avg_exploration)), avg_exploration, 1)
        p = np.poly1d(z)
        ax.plot(range(len(avg_exploration)), p(range(len(avg_exploration))), 
               'r--', alpha=0.5, label='趋势')
        ax.legend()


def _plot_category_coverage(ax, analyzer, results):
    """绘制类别覆盖热力图"""
    # 创建消费者-类别矩阵
    n_consumers_sample = min(50, len(analyzer.consumer_histories))
    n_categories = analyzer.n_categories
    
    # 随机选择消费者样本
    sample_consumers = np.random.choice(
        list(analyzer.consumer_histories.keys()), 
        n_consumers_sample, 
        replace=False
    )
    
    coverage_matrix = np.zeros((n_consumers_sample, n_categories))
    
    for i, consumer_id in enumerate(sample_consumers):
        history = analyzer.consumer_histories[consumer_id]
        for cat in history.chosen_categories:
            coverage_matrix[i, cat] += 1
    
    # 归一化
    row_sums = coverage_matrix.sum(axis=1, keepdims=True)
    coverage_matrix = np.divide(coverage_matrix, row_sums, 
                               where=row_sums!=0, out=np.zeros_like(coverage_matrix))
    
    im = ax.imshow(coverage_matrix, cmap='YlOrRd', aspect='auto')
    ax.set_xlabel('产品类别')
    ax.set_ylabel('消费者样本')
    ax.set_title('类别选择热力图')
    plt.colorbar(im, ax=ax, label='选择频率')


def _plot_filter_bubble_strength(ax, results):
    """绘制过滤气泡强度"""
    pop_metrics = results['population_metrics']
    
    # 创建气泡强度可视化
    bubble_strength = pop_metrics['filter_bubble_strength']
    high_vs_low = pop_metrics['high_vs_low_diff']
    
    # 绘制仪表盘式图表
    categories = ['过滤气泡\n强度', '高vs低差异']
    values = [bubble_strength, abs(high_vs_low)]
    colors = ['red' if v > 0.1 else 'orange' if v > 0.05 else 'green' for v in values]
    
    bars = ax.bar(categories, values, color=colors, alpha=0.7)
    ax.set_ylabel('强度')
    ax.set_title('过滤气泡指标')
    ax.set_ylim(0, 0.5)
    
    # 添加阈值线
    ax.axhline(y=0.05, color='green', linestyle='--', alpha=0.5, label='低')
    ax.axhline(y=0.1, color='orange', linestyle='--', alpha=0.5, label='中')
    ax.axhline(y=0.2, color='red', linestyle='--', alpha=0.5, label='高')
    ax.legend()
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.3f}', ha='center', va='bottom', fontsize=10)


def _plot_individual_diversity(ax, results):
    """绘制个体多样性散点图"""
    individual_metrics = results['individual_metrics']
    
    levels = []
    diversities = []
    coverages = []
    
    for m in individual_metrics:
        if all(k in m for k in ['dependency_level', 'diversity_score', 'category_coverage']):
            levels.append(m['dependency_level'])
            diversities.append(m['diversity_score'])
            coverages.append(m['category_coverage'])
    
    # 使用颜色表示依赖等级
    scatter = ax.scatter(diversities, coverages, c=levels, cmap='RdYlGn_r', 
                        alpha=0.6, s=30)
    
    ax.set_xlabel('多样性得分')
    ax.set_ylabel('类别覆盖率')
    ax.set_title('个体多样性特征')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.colorbar(scatter, ax=ax, label='依赖等级')
    
    # 添加趋势线
    if len(diversities) > 1:
        z = np.polyfit(diversities, coverages, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(diversities), max(diversities), 100)
        ax.plot(x_line, p(x_line), 'r--', alpha=0.5)
