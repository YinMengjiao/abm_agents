"""
实验 3-b 可视化：系统性风险
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
        'title': '实验 3-b: 系统性风险与级联失效分析',
        'avg_trust': '平均信任',
        'trust_range': '信任范围',
        'failure_event': '故障发生',
        'trust_trajectory': '(a) Trust Level演化轨迹',
        'cascade_size_label': 'Cascade Size（受影响人数）',
        'frequency': '频次',
        'cascade_dist': '(e) Cascade Size分布',
        'initial_trust': '初始信任',
        'min_trust': '最低信任',
        'final_trust': '最终信任',
        'resilience_score': 'Resilience Score',
        'score': '得分',
        'resilience_assess': '(f) 系统韧性评估',
        'high_resilience': '高韧性',
        'medium_resilience': '中等韧性',
        'low_resilience': '低韧性',
        'resilience_level': '韧性等级',
        'impact_scope': '影响范围',
    },
    'en': {
        'title': 'Experiment 3-b: Systemic Risk & Cascade Failures',
        'avg_trust': 'Avg Trust',
        'trust_range': 'Trust Range',
        'failure_event': 'Failure Event',
        'trust_trajectory': '(a) Trust Level Trajectory',
        'cascade_size_label': 'Cascade Size (Affected Agents)',
        'frequency': 'Frequency',
        'cascade_dist': '(e) Cascade Size Distribution',
        'initial_trust': 'Initial Trust',
        'min_trust': 'Min Trust',
        'final_trust': 'Final Trust',
        'resilience_score': 'Resilience Score',
        'score': 'Score',
        'resilience_assess': '(f) System Resilience Assessment',
        'high_resilience': 'High Resilience',
        'medium_resilience': 'Medium Resilience',
        'low_resilience': 'Low Resilience',
        'resilience_level': 'Resilience Level',
        'impact_scope': 'Impact Scope',
    }
}


def visualize_systemic_risk_results(main_result, stress_results, risk_model, output_dir: str = None, en: bool = False):
    """
    可视化系统性风险结果
    
    Args:
        main_result: 主要结果
        stress_results: 压力测试结果
        risk_model: 风险模型
        output_dir: 输出目录
        en: True=英文, False=中文 (默认)
    """
    if output_dir is None:
        output_dir = RESULTS["exp3_risk"]
    os.makedirs(output_dir, exist_ok=True)
    
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    
    # 设置字体
    if en:
        setup_english_font()
    else:
        setup_chinese_font()
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. Trust Level演化轨迹
    ax1 = plt.subplot(2, 3, 1)
    _plot_trust_trajectory(ax1, main_result, text)
    
    # 2. 依赖等级演化
    ax2 = plt.subplot(2, 3, 2)
    _plot_dependency_trajectory(ax2, main_result)
    
    # 3. 故障传播过程
    ax3 = plt.subplot(2, 3, 3)
    _plot_failure_propagation(ax3, main_result)
    
    # 4. 压力测试对比
    ax4 = plt.subplot(2, 3, 4)
    _plot_stress_test_comparison(ax4, stress_results, text)
    
    # 5. Cascade Size分布
    ax5 = plt.subplot(2, 3, 5)
    _plot_cascade_size_distribution(ax5, stress_results, text)
    
    # 6. 系统韧性评估
    ax6 = plt.subplot(2, 3, 6)
    _plot_resilience_assessment(ax6, main_result, risk_model, text)
    
    plt.suptitle(text['title'], fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95], pad=2.0, h_pad=3.0, w_pad=3.0)  # 增加子图间距
    plt.savefig(f'{output_dir}/systemic_risk_analysis.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  [OK] 系统性风险分析图已保存：{output_dir}/systemic_risk_analysis.png")


def _plot_trust_trajectory(ax, result, text):
    """Plot Trust Level trajectory"""
    trajectory = result.get('trust_trajectory', [])
    
    if not trajectory:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
        return
    
    steps = range(len(trajectory))
    avg_trust = [np.mean(t) for t in trajectory]
    min_trust = [np.min(t) for t in trajectory]
    max_trust = [np.max(t) for t in trajectory]
    
    # 绘制平均Trust Level
    ax.plot(steps, avg_trust, color='#4C72B0', linewidth=2.5, label=text['avg_trust'])
    ax.fill_between(steps, min_trust, max_trust, alpha=0.25, color='#4C72B0', label=text['trust_range'])
    
    # 标注故障点
    ax.axvline(x=50, color='#C44E52', linestyle='--', linewidth=2.5, label=text['failure_event'])
    
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('Trust Level')
    ax.set_title(text['trust_trajectory'])
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_dependency_trajectory(ax, result):
    """绘制依赖等级演化"""
    trajectory = result.get('dependency_trajectory', [])
    
    if not trajectory:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
        return
    
    steps = range(len(trajectory))
    avg_dep = [np.mean(t) for t in trajectory]
    
    ax.plot(steps, avg_dep, color='#55A868', linewidth=2.5)
    ax.fill_between(steps, avg_dep, alpha=0.25, color='#55A868')
    
    # 标注故障点
    ax.axvline(x=50, color='#C44E52', linestyle='--', linewidth=2.5)
    
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('Average Dependency Level')
    ax.set_title('(b) Dependency Level Evolution')
    ax.set_ylim(1, 5)
    ax.grid(True, alpha=0.3)


def _plot_failure_propagation(ax, result):
    """绘制故障传播过程"""
    trajectory = result.get('trust_trajectory', [])
    
    if not trajectory or len(trajectory) < 50:
        ax.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center')
        return
    
    # 计算每步的Trust Level下降速度（近似传播）
    propagation_speed = []
    for i in range(1, len(trajectory)):
        if i >= 50 and i <= 70:  # 故障传播期
            speed = abs(np.mean(trajectory[i]) - np.mean(trajectory[i-1]))
            propagation_speed.append(speed)
        else:
            propagation_speed.append(0)
    
    # 累积受影响人数（模拟）
    steps = range(len(propagation_speed))
    ax.fill_between(steps, propagation_speed, alpha=0.5, color='#C44E52')
    ax.plot(steps, propagation_speed, color='#C44E52', linewidth=2.5)
    
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('Propagation Speed')
    ax.set_title('(c) Failure Propagation Process')
    ax.axvline(x=50, color='#C44E52', linestyle='--', alpha=0.5)
    ax.grid(True, alpha=0.3)


def _plot_stress_test_comparison(ax, stress_results, text):
    """Plot stress test comparison"""
    scenarios = list(stress_results.keys())
    trust_drops = [stress_results[s]['trust_drop'] for s in scenarios]
    max_affected = [stress_results[s]['max_affected'] for s in scenarios]
    
    x = np.arange(len(scenarios))
    width = 0.35
    
    # 归一化Max Impact人数
    max_aff_normalized = [m / 500 for m in max_affected]
    
    ax.bar(x - width/2, trust_drops, width, label='Trust Drop', alpha=0.8, color='#C44E52', edgecolor='white', linewidth=0.5)
    ax.bar(x + width/2, max_aff_normalized, width, label=text['impact_scope'], alpha=0.8, color='#DD8452', edgecolor='white', linewidth=0.5)
    
    ax.set_ylabel('Impact Severity')
    ax.set_title('(d) Stress Test Scenario Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels([s.replace('_', '\n') for s in scenarios], rotation=0, fontsize=8)
    ax.legend()


def _plot_cascade_size_distribution(ax, stress_results, text):
    """Plot Cascade Size distribution"""
    cascade_sizes = [stress_results[s]['max_affected'] for s in stress_results.keys()]
    
    if not cascade_sizes:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
        return
    
    ax.hist(cascade_sizes, bins=10, alpha=0.75, color='#4C72B0', edgecolor='white', linewidth=0.8)
    mean_val = np.mean(cascade_sizes)
    ax.axvline(x=mean_val, color='#C44E52', linestyle='--', 
              linewidth=2.5, label=f'Mean: {mean_val:.0f}')
    
    ax.set_xlabel(text['cascade_size_label'])
    ax.set_ylabel(text['frequency'])
    ax.set_title(text['cascade_dist'])
    ax.legend()


def _plot_resilience_assessment(ax, result, risk_model, text):
    """Plot system resilience assessment"""
    trajectory = result.get('trust_trajectory', [])
    
    if not trajectory:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
        return
    
    # 计算韧性指标
    initial_trust = np.mean(trajectory[0]) if trajectory else 0.5
    min_trust = min(np.mean(t) for t in trajectory) if trajectory else 0.3
    final_trust = np.mean(trajectory[-1]) if trajectory else 0.5
    
    # 韧性 = 恢复程度 / 冲击程度
    shock = initial_trust - min_trust
    recovery = final_trust - min_trust
    resilience = recovery / (shock + 0.001)
    
    # 绘制韧性仪表盘
    categories = [text['initial_trust'], text['min_trust'], text['final_trust'], text['resilience_score']]
    values = [initial_trust, min_trust, final_trust, resilience]
    colors = ['#55A868', '#C44E52', '#4C72B0', '#8172B3']  # 顶刊柔和配色
    
    bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=0.8)
    ax.set_ylabel(text['score'])
    ax.set_title(text['resilience_assess'])
    
    # 先调整 y 轴上限，为标签留出空间
    max_val = max(values)
    ax.set_ylim(0, max_val * 1.2)  # 预留 20% 的空间给标签
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    
    # 添加韧性等级标注
    if resilience > 0.8:
        resilience_level = text['high_resilience']
    elif resilience > 0.5:
        resilience_level = text['medium_resilience']
    else:
        resilience_level = text['low_resilience']
    
    ax.text(0.5, 0.9, f"{text['resilience_level']}: {resilience_level}", 
           transform=ax.transAxes, ha='center', fontsize=12, 
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
