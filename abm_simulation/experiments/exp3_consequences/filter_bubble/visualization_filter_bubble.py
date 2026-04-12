"""
实验 3-a 可视化：过滤气泡
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
        'title': '实验 3-a: 过滤气泡与选择多样性分析',
    },
    'en': {
        'title': 'Experiment 3-a: Filter Bubbles & Choice Diversity',
    }
}


def visualize_filter_bubble_results(analyzer, results, output_dir: str = None, en: bool = False):
    """
    可视化过滤气泡结果
    
    Args:
        analyzer: 分析器实例
        results: 结果数据
        output_dir: 输出目录
        en: True=英文, False=中文 (默认)
    """
    if output_dir is None:
        output_dir = RESULTS["exp3_bubble"]
    os.makedirs(output_dir, exist_ok=True)
    
    # 设置字体
    if en:
        setup_english_font()
    else:
        setup_chinese_font()
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. 各Dependency Level多样性对比
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
    
    plt.suptitle(TEXT_CONFIG['en' if en else 'zh']['title'], fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95], pad=2.0, h_pad=3.0, w_pad=3.0)  # 增加子图间距
    plt.savefig(f'{output_dir}/filter_bubble_analysis.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  [OK] 过滤气泡分析图已保存：{output_dir}/filter_bubble_analysis.png")


def _plot_diversity_by_level(ax, results):
    """绘制各Dependency Level多样性对比"""
    diversity_by_level = results['population_metrics']['diversity_by_level']
    
    levels = list(diversity_by_level.keys())
    diversities = list(diversity_by_level.values())
    
    colors = plt.cm.RdYlGn(np.array(diversities))
    bars = ax.bar([f'L{l}' for l in levels], diversities, color=colors, alpha=0.8, width=0.5)
    
    ax.set_ylabel('Diversity Score')
    ax.set_title('(a) Choice Diversity by Dependency Level')
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
        ax.hist(diversity_scores, bins=20, alpha=0.75, color='#4C72B0', edgecolor='white', linewidth=0.8)
        ax.axvline(x=np.mean(diversity_scores), color='#C44E52', linestyle='--', 
                  linewidth=2.5, label=f'Mean: {np.mean(diversity_scores):.3f}')
    
    ax.set_xlabel('Diversity Score')
    ax.set_ylabel('Consumer Count')
    ax.set_title('(b) Diversity Distribution')
    ax.legend()


def _plot_exploration_rate(ax, results):
    """绘制探索率对比"""
    individual_metrics = results['individual_metrics']
    
    # 按Dependency Level分组
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
    bars = ax.bar(levels, avg_exploration, color=colors, alpha=0.8, width=0.5)
    
    ax.set_ylabel('Average Exploration Rate')
    ax.set_title('(c) Exploration Behavior by Level')
    ax.set_ylim(0, 1)
    
    # 添加趋势线
    if len(avg_exploration) > 1:
        z = np.polyfit(range(len(avg_exploration)), avg_exploration, 1)
        p = np.poly1d(z)
        ax.plot(range(len(avg_exploration)), p(range(len(avg_exploration))), 
               'r--', alpha=0.5, label='Trend')
        ax.legend()


def _plot_category_coverage(ax, analyzer, results):
    """绘制类别覆盖热力图"""
    # 创建消费者-类别矩阵
    n_consumers_sample = min(50, len(analyzer.consumer_histories))
    n_categories = analyzer.n_categories
    
    # 随机选择Consumer Sample
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
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Consumer Sample')
    ax.set_title('(d) Category Selection Heatmap')
    plt.colorbar(im, ax=ax, label='Selection Frequency')


def _plot_filter_bubble_strength(ax, results):
    """绘制过滤气泡强度 - 改为箱线图展示分布"""
    pop_metrics = results['population_metrics']
    individual_metrics = results['individual_metrics']
    
    # 按高/低依赖分组
    high_dep_scores = [m['diversity_score'] for m in individual_metrics 
                      if m.get('dependency_level', 0) >= 4 and 'diversity_score' in m]
    low_dep_scores = [m['diversity_score'] for m in individual_metrics 
                     if m.get('dependency_level', 0) <= 2 and 'diversity_score' in m]
    
    # 绘制箱线图
    data_to_plot = [low_dep_scores, high_dep_scores]
    bp = ax.boxplot(data_to_plot, labels=['Low Dep.\n(L1-L2)', 'High Dep.\n(L4-L5)'], 
                    patch_artist=True, widths=0.5)
    
    # 设置颜色 - 顶刊柔和配色
    colors = ['#55A868', '#C44E52']  # 绿色和红色
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
        patch.set_edgecolor('#2C3E50')
        patch.set_linewidth(1.2)
    
    # 设置中须和异常值颜色
    for element in ['whiskers', 'caps', 'fliers']:
        for item in bp[element]:
            if element == 'fliers':
                item.set_markeredgecolor('#7F8C8D')
                item.set_markeredgewidth(0.8)
                item.set_markerfacecolor('none')
            else:
                item.set_color('#7F8C8D')
                item.set_linewidth(1.2)
    
    ax.set_ylabel('Diversity Score')
    ax.set_title('(e) Filter Bubble Effect', pad=12)  # 增加标题与图表的间距
    ax.set_ylim(0.4, 1.05)  # 根据实际数据调整Y轴范围
    ax.grid(True, alpha=0.3, axis='y')
    
    # 添加统计检验标注 - 放在子图内部左上角，避免影响布局
    if len(high_dep_scores) > 0 and len(low_dep_scores) > 0:
        from scipy import stats
        t_stat, p_value = stats.ttest_ind(low_dep_scores, high_dep_scores)
        significance = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
        ax.text(0.05, 0.95, f'p={p_value:.4f} {significance}', 
               ha='left', va='top', fontsize=9, fontweight='bold', 
               transform=ax.transAxes, color='#2C3E50',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))


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
    
    # 使用颜色表示Dependency Level
    scatter = ax.scatter(diversities, coverages, c=levels, cmap='RdYlGn_r', 
                        alpha=0.6, s=50, edgecolors='gray', linewidth=0.5)
    
    ax.set_xlabel('Diversity Score')
    ax.set_ylabel('Category Coverage')
    ax.set_title('(f) Individual Diversity Profile')
    
    # 根据数据范围动态设置坐标轴，留出 10% 的边距
    if len(diversities) > 1:
        x_margin = (max(diversities) - min(diversities)) * 0.1
        y_margin = (max(coverages) - min(coverages)) * 0.1
        
        # 避免边距过小导致点贴在边界上
        x_margin = max(x_margin, 0.05)
        y_margin = max(y_margin, 0.05)
        
        ax.set_xlim(min(diversities) - x_margin, max(diversities) + x_margin)
        ax.set_ylim(min(coverages) - y_margin, max(coverages) + y_margin)
    else:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    
    plt.colorbar(scatter, ax=ax, label='Dependency Level')
    
    # 添加趋势线
    if len(diversities) > 1:
        z = np.polyfit(diversities, coverages, 1)
        p = np.poly1d(z)
        x_line = np.linspace(min(diversities), max(diversities), 100)
        ax.plot(x_line, p(x_line), 'r--', alpha=0.5)
