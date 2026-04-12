"""
对比实验可视化：调查数据驱动 vs 理论假设初始化
生成学术论文级别的对比图表
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.gridspec import GridSpec
from matplotlib.sankey import Sankey
import json
import os
import sys

# 添加项目根目录（abm_simulation/）到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from visualization.chinese_font import setup_chinese_font, setup_english_font
from config import RESULTS

# 顶刊柔和配色
COLORS = {
    'survey': '#2E86AB',      # 蓝色 - 调查数据
    'theoretical': '#A23B72', # 紫色 - 理论假设
    'survey_fill': 'rgba(46, 134, 171, 0.2)',
    'theoretical_fill': 'rgba(162, 59, 114, 0.2)',
    'levels': ['#4C72B0', '#5B9BD5', '#55A868', '#DD8452', '#C44E52']
}

# 语言配置
TEXT_CONFIG = {
    'zh': {
        'title': '初始化方式对比：调查数据驱动 vs 理论假设',
        'subtitle_survey': '调查数据初始化流向',
        'subtitle_theoretical': '理论假设初始化流向',
        'initial': '初始',
        'final': '最终',
        'evolution': '等级分布演化对比',
        'magnetization': '磁化强度演化对比',
        'satisfaction': '满意度演化对比',
        'metrics': '关键指标对比 (箱线图)',
        'sim_steps': '仿真步数',
        'agent_count': '智能体数量',
        'magnetization_label': '磁化强度 M',
        'avg_satisfaction': '平均满意度',
        'normalized': '归一化值',
        'survey_data': '调查数据',
        'theoretical': '理论假设',
        'final_mag': '最终磁化强度',
        'avg_sat': '平均满意度',
        'ai_usage': 'AI使用率',
        'error_rate': '错误率',
        'level_survey': '调查',
        'level_theoretical': '理论',
        'initial_to_final': '初始→最终'
    },
    'en': {
        'title': 'Initialization Comparison: Survey-Driven vs Theoretical',
        'subtitle_survey': 'Survey Data Initialization Flow',
        'subtitle_theoretical': 'Theoretical Initialization Flow',
        'initial': 'Initial',
        'final': 'Final',
        'evolution': 'Level Distribution Evolution',
        'magnetization': 'Magnetization Evolution',
        'satisfaction': 'Satisfaction Evolution',
        'metrics': 'Key Metrics Comparison (Boxplot)',
        'sim_steps': 'Simulation Steps',
        'agent_count': 'Agent Count',
        'magnetization_label': 'Magnetization M',
        'avg_satisfaction': 'Avg Satisfaction',
        'normalized': 'Normalized Value',
        'survey_data': 'Survey Data',
        'theoretical': 'Theoretical',
        'final_mag': 'Final Magnetization',
        'avg_sat': 'Avg Satisfaction',
        'ai_usage': 'AI Usage Rate',
        'error_rate': 'Error Rate',
        'level_survey': 'Survey',
        'level_theoretical': 'Theory',
        'initial_to_final': 'Initial→Final'
    }
}

# 等级标签
LEVEL_LABELS = {
    'zh': ['L1\n完全自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理'],
    'en': ['L1\nFully Autonomous', 'L2\nInfo-Assisted', 'L3\nSemi-Delegated', 'L4\nHighly Dependent', 'L5\nFully Delegated']
}

LEVEL_LABELS_SHORT = {
    'zh': ['L1', 'L2', 'L3', 'L4', 'L5'],
    'en': ['L1', 'L2', 'L3', 'L4', 'L5']
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


def plot_initial_to_final_sankey(ax, results, group_name, dist_key, color_main, en=False):
    """绘制横向桑基图 - 上方初始，下方最终"""
    levels = [1, 2, 3, 4, 5]
    lang = 'en' if en else 'zh'
    level_labels_short = LEVEL_LABELS_SHORT[lang]
    text = TEXT_CONFIG[lang]
    
    # 获取初始分布
    if dist_key == 'survey':
        initial_dist = results['parameters']['survey_distribution']
        final_results = results['results_survey']
    else:
        initial_dist = results['parameters']['theoretical_distribution']
        final_results = results['results_theoretical']
    
    # 计算最终分布的平均值
    final_counts = []
    for level in levels:
        counts = [r['final_distribution'].get(str(level), 0) for r in final_results]
        final_counts.append(np.mean(counts))
    
    # 转换为百分比
    initial_values = np.array([initial_dist[str(l)] * 100 for l in levels])
    total_final = sum(final_counts)
    final_values = np.array([(c / total_final) * 100 if total_final > 0 else 0 for c in final_counts])
    
    # 桑基图布局参数
    n_levels = len(levels)
    top_y = 0.75  # 上方（初始）
    bottom_y = 0.25  # 下方（最终）
    
    # 计算每个等级的横向位置（按照比例累积排列）
    # 上方节点：按照初始分布比例排列
    initial_total = sum(initial_values)
    initial_cumulative = np.cumsum([0] + list(initial_values)) / initial_total
    top_x_positions = []
    top_widths = []
    margin = 0.05  # 左右边距
    available_width = 1.0 - 2 * margin
    
    for i in range(n_levels):
        # 中心位置
        center_x = margin + available_width * (initial_cumulative[i] + initial_cumulative[i+1]) / 2
        # 宽度（与比例成正比）
        width = available_width * (initial_values[i] / initial_total)
        top_x_positions.append(center_x)
        top_widths.append(width)
    
    # 下方节点：按照最终分布比例排列
    final_total = sum(final_values)
    final_cumulative = np.cumsum([0] + list(final_values)) / final_total
    bottom_x_positions = []
    bottom_widths = []
    
    for i in range(n_levels):
        # 中心位置
        center_x = margin + available_width * (final_cumulative[i] + final_cumulative[i+1]) / 2
        # 宽度（与比例成正比）
        width = available_width * (final_values[i] / final_total)
        bottom_x_positions.append(center_x)
        bottom_widths.append(width)
    
    # 绘制水流带（从上到下），宽度从上方节点平滑过渡到下方节点
    for i in range(n_levels):
        for j in range(n_levels):
            if abs(i - j) <= 1:  # 只显示自身和相邻等级的流动
                # 计算流向强度
                if i == j:
                    flow_strength = 0.7
                else:
                    flow_strength = 0.15
                
                # 上方和下方的水流带宽度分别匹配对应节点宽度
                band_width_top = top_widths[i] * flow_strength
                band_width_bottom = bottom_widths[j] * flow_strength
                
                # 使用贝塞尔曲线创建平滑的水流效果
                n_points = 50
                y = np.linspace(top_y, bottom_y, n_points)
                t = (y - top_y) / (bottom_y - top_y)  # 0→1 插值因子
                
                # 沿路径插值宽度
                band_width = band_width_top + (band_width_bottom - band_width_top) * t
                
                # 计算中心线（带正弦曲线）
                x_center = top_x_positions[i] + (bottom_x_positions[j] - top_x_positions[i]) * t
                avg_bw = (band_width_top + band_width_bottom) / 2
                x_center += avg_bw * 0.3 * np.sin(np.pi * t) * (1 if i < j else -1 if i > j else 0)
                
                # 左边界和右边界
                x_left = x_center - band_width / 2
                x_right = x_center + band_width / 2
                
                # 填充水流带
                ax.fill_betweenx(y, x_left, x_right, 
                                color=COLORS['levels'][i], 
                                alpha=0.35 if i != j else 0.5, edgecolor='none')
    
    # 绘制上方初始分布节点（矩形条）
    for i, level in enumerate(levels):
        x_left = top_x_positions[i] - top_widths[i] / 2
        x_right = top_x_positions[i] + top_widths[i] / 2
        
        # 矩形条（宽度与比例成正比）
        rect = plt.Rectangle((x_left, top_y - 0.02), top_widths[i], 0.04,
                           facecolor=COLORS['levels'][i], alpha=0.8, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        
        # 标签（上方）
        ax.text(top_x_positions[i], top_y + 0.06, level_labels_short[i], 
               ha='center', va='center', fontsize=10, fontweight='bold')
        ax.text(top_x_positions[i], top_y + 0.11, f'{initial_values[i]:.2f}%', 
               ha='center', va='center', fontsize=9)
    
    # 绘制下方最终分布节点（矩形条）
    for i, level in enumerate(levels):
        x_left = bottom_x_positions[i] - bottom_widths[i] / 2
        x_right = bottom_x_positions[i] + bottom_widths[i] / 2
        
        # 矩形条（宽度与比例成正比）
        rect = plt.Rectangle((x_left, bottom_y - 0.02), bottom_widths[i], 0.04,
                           facecolor=COLORS['levels'][i], alpha=0.8, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        
        # 标签（下方）
        ax.text(bottom_x_positions[i], bottom_y - 0.06, level_labels_short[i], 
               ha='center', va='center', fontsize=10, fontweight='bold')
        ax.text(bottom_x_positions[i], bottom_y - 0.11, f'{final_values[i]:.2f}%', 
               ha='center', va='center', fontsize=9)
    
    # 添加标签
    ax.text(0.5, top_y + 0.18, text['initial'], ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(0.5, bottom_y - 0.18, text['final'], ha='center', va='center', fontsize=11, fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')


def plot_initial_distribution_comparison(ax, results, en=False):
    """绘制初始分布对比 - 弦图"""
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    plot_initial_to_final_sankey(ax, results, 'survey', 'survey', COLORS['survey'], en=en)
    ax.set_title(f'(a) {text["subtitle_survey"]}', fontsize=12, fontweight='bold', pad=20)


def plot_final_distribution_comparison(ax, results, en=False):
    """绘制最终分布对比 - 弦图"""
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    plot_initial_to_final_sankey(ax, results, 'theoretical', 'theoretical', COLORS['theoretical'], en=en)
    ax.set_title(f'(b) {text["subtitle_theoretical"]}', fontsize=12, fontweight='bold', pad=20)


def plot_evolution_comparison(ax, results, en=False):
    """绘制等级演化对比"""
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    # 获取第一个运行的演化数据作为示例
    survey_result = results['results_survey'][0]
    theoretical_result = results['results_theoretical'][0]
    
    n_steps = len(survey_result['level_evolution']['1'])
    steps = np.arange(n_steps) * 10  # 每10步采样
    
    # 绘制调查数据
    for level in range(1, 6):
        values = survey_result['level_evolution'][str(level)]
        ax.plot(steps, values, color=COLORS['levels'][level-1], 
               linewidth=2, alpha=0.8, linestyle='-', label=f'L{level} {text["level_survey"]}')
    
    # 绘制理论假设（虚线）
    for level in range(1, 6):
        values = theoretical_result['level_evolution'][str(level)]
        ax.plot(steps, values, color=COLORS['levels'][level-1], 
               linewidth=2, alpha=0.5, linestyle='--', label=f'L{level} {text["level_theoretical"]}')
    
    ax.set_xlabel(text['sim_steps'], fontsize=11)
    ax.set_ylabel(text['agent_count'], fontsize=11)
    ax.set_title(f'(c) {text["evolution"]}', fontsize=12, fontweight='bold')
    # 图例移到左上角，避免遮挡数据
    ax.legend(fontsize=8, loc='upper left', ncol=2)
    ax.grid(True, alpha=0.3)


def plot_magnetization_comparison(ax, results, en=False):
    """绘制磁化强度演化对比"""
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    survey_result = results['results_survey'][0]
    theoretical_result = results['results_theoretical'][0]
    
    n_steps = len(survey_result['magnetization_evolution'])
    steps = np.arange(n_steps) * 10
    
    survey_mag = survey_result['magnetization_evolution']
    theoretical_mag = theoretical_result['magnetization_evolution']
    
    ax.plot(steps, survey_mag, color=COLORS['survey'], linewidth=2.5, 
           label=text['survey_data'], alpha=0.8)
    ax.plot(steps, theoretical_mag, color=COLORS['theoretical'], linewidth=2.5, 
           label=text['theoretical'], alpha=0.8, linestyle='--')
    
    ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax.set_xlabel(text['sim_steps'], fontsize=11)
    ax.set_ylabel(text['magnetization_label'], fontsize=11)
    ax.set_title(f'(d) {text["magnetization"]}', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)


def plot_satisfaction_comparison(ax, results, en=False):
    """绘制满意度演化对比"""
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    survey_result = results['results_survey'][0]
    theoretical_result = results['results_theoretical'][0]
    
    n_steps = len(survey_result['satisfaction_evolution'])
    steps = np.arange(n_steps) * 10
    
    survey_sat = survey_result['satisfaction_evolution']
    theoretical_sat = theoretical_result['satisfaction_evolution']
    
    ax.plot(steps, survey_sat, color=COLORS['survey'], linewidth=2.5, 
           label=text['survey_data'], alpha=0.8)
    ax.plot(steps, theoretical_sat, color=COLORS['theoretical'], linewidth=2.5, 
           label=text['theoretical'], alpha=0.8, linestyle='--')
    
    ax.set_xlabel(text['sim_steps'], fontsize=11)
    ax.set_ylabel(text['avg_satisfaction'], fontsize=11)
    ax.set_title(f'(e) {text["satisfaction"]}', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)


def plot_metrics_boxplot(ax, results, en=False):
    """绘制关键指标箱线图对比"""
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    metrics = ['magnetization_final', 'avg_satisfaction', 'ai_usage_rate', 'error_rate']
    metric_labels = [text['final_mag'], text['avg_sat'], text['ai_usage'], text['error_rate']]
    
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
                     patch_artist=True)
    bp2 = ax.boxplot(theoretical_data_norm, positions=positions + width/2, widths=width,
                     patch_artist=True)
    
    for patch in bp1['boxes']:
        patch.set_facecolor(COLORS['survey'])
        patch.set_alpha(0.6)
    for patch in bp2['boxes']:
        patch.set_facecolor(COLORS['theoretical'])
        patch.set_alpha(0.6)
    
    ax.set_xticks(positions)
    ax.set_xticklabels(metric_labels, fontsize=9)
    ax.set_ylabel(text['normalized'], fontsize=11)
    ax.set_title(f'(f) {text["metrics"]}', fontsize=12, fontweight='bold')
    
    # 手动创建图例
    from matplotlib.patches import Patch
    survey_label = 'Survey Data' if en else '调查数据'
    theory_label = 'Theoretical' if en else '理论假设'
    legend_handles = [
        Patch(facecolor=COLORS['survey'], alpha=0.6, label=survey_label),
        Patch(facecolor=COLORS['theoretical'], alpha=0.6, label=theory_label)
    ]
    ax.legend(handles=legend_handles, fontsize=10, loc='lower right')
    ax.grid(True, axis='y', alpha=0.3)
    
    # 添加数据标签（中位数）
    for i in range(len(metrics)):
        # 调查数据中位数
        median_survey = np.median(survey_data_norm[i])
        ax.text(positions[i] - width/2, median_survey + 0.03, 
               f'{median_survey:.2f}', ha='center', va='bottom', 
               fontsize=8, fontweight='bold', color=COLORS['survey'])
        
        # 理论假设中位数
        median_theoretical = np.median(theoretical_data_norm[i])
        ax.text(positions[i] + width/2, median_theoretical + 0.03, 
               f'{median_theoretical:.2f}', ha='center', va='bottom', 
               fontsize=8, fontweight='bold', color=COLORS['theoretical'])


def create_comparison_visualization(results, output_dir: str = None, en: bool = False):
    """创建完整的对比可视化
    
    Args:
        results: 实验结果数据
        output_dir: 输出目录
        en: True=英文, False=中文 (默认)
    """
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    if output_dir is None:
        output_dir = RESULTS["exp_comparison"]
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 设置字体
    if en:
        setup_english_font()
    else:
        setup_chinese_font()
    
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
    plot_initial_distribution_comparison(ax1, results, en=en)
    plot_final_distribution_comparison(ax2, results, en=en)
    plot_evolution_comparison(ax3, results, en=en)
    plot_magnetization_comparison(ax4, results, en=en)
    plot_satisfaction_comparison(ax5, results, en=en)
    plot_metrics_boxplot(ax6, results, en=en)
    
    # 总标题
    plt.suptitle(text['title'], 
                fontsize=16, fontweight='bold', y=0.98)
    
    # 保存
    output_path = os.path.join(output_dir, 'initialization_comparison.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\n✓ 对比图已保存: {output_path}")
    
    plt.close()
    return output_path


def main(en: bool = False):
    """主函数
    
    Args:
        en: True=生成英文图表, False=生成中文图表 (默认)
    """
    # 加载结果
    results = load_results()
    
    # 生成可视化
    output_path = create_comparison_visualization(results, en=en)
    
    lang_str = '英文' if en else '中文'
    print(f"\n{'='*70}")
    print(f"可视化完成！（{lang_str}）")
    print(f"{'='*70}")
    print(f"输出文件: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='生成对比实验可视化图表')
    parser.add_argument('--en', action='store_true', help='生成英文版本的图表')
    args = parser.parse_args()
    
    main(en=args.en)
