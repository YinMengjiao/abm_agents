"""
实验 10 可视化：系统性风险
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# 添加项目根目录并导入中文字体配置
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from visualization.chinese_font import setup_chinese_font
from config import RESULTS
setup_chinese_font()


def visualize_systemic_risk_results(main_result, stress_results, risk_model, output_dir: str = None):
    """可视化系统性风险结果"""
    if output_dir is None:
        output_dir = RESULTS["exp3_risk"]
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. 信任度演化轨迹
    ax1 = plt.subplot(2, 3, 1)
    _plot_trust_trajectory(ax1, main_result)
    
    # 2. 依赖等级演化
    ax2 = plt.subplot(2, 3, 2)
    _plot_dependency_trajectory(ax2, main_result)
    
    # 3. 故障传播过程
    ax3 = plt.subplot(2, 3, 3)
    _plot_failure_propagation(ax3, main_result)
    
    # 4. 压力测试对比
    ax4 = plt.subplot(2, 3, 4)
    _plot_stress_test_comparison(ax4, stress_results)
    
    # 5. 级联规模分布
    ax5 = plt.subplot(2, 3, 5)
    _plot_cascade_size_distribution(ax5, stress_results)
    
    # 6. 系统韧性评估
    ax6 = plt.subplot(2, 3, 6)
    _plot_resilience_assessment(ax6, main_result, risk_model)
    
    plt.suptitle('实验 3-b: 系统性风险与级联失效分析', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95], pad=2.0, h_pad=3.0, w_pad=3.0)  # 增加子图间距
    plt.savefig(f'{output_dir}/systemic_risk_analysis.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"  [OK] 系统性风险分析图已保存：{output_dir}/systemic_risk_analysis.png")


def _plot_trust_trajectory(ax, result):
    """绘制信任度演化轨迹"""
    trajectory = result.get('trust_trajectory', [])
    
    if not trajectory:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = range(len(trajectory))
    avg_trust = [np.mean(t) for t in trajectory]
    min_trust = [np.min(t) for t in trajectory]
    max_trust = [np.max(t) for t in trajectory]
    
    # 绘制平均信任度
    ax.plot(steps, avg_trust, color='#4C72B0', linewidth=2.5, label='平均信任')
    ax.fill_between(steps, min_trust, max_trust, alpha=0.25, color='#4C72B0', label='信任范围')
    
    # 标注故障点
    ax.axvline(x=50, color='#C44E52', linestyle='--', linewidth=2.5, label='故障发生')
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('信任度')
    ax.set_title('(a) 信任度演化轨迹')
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_dependency_trajectory(ax, result):
    """绘制依赖等级演化"""
    trajectory = result.get('dependency_trajectory', [])
    
    if not trajectory:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    steps = range(len(trajectory))
    avg_dep = [np.mean(t) for t in trajectory]
    
    ax.plot(steps, avg_dep, color='#55A868', linewidth=2.5)
    ax.fill_between(steps, avg_dep, alpha=0.25, color='#55A868')
    
    # 标注故障点
    ax.axvline(x=50, color='#C44E52', linestyle='--', linewidth=2.5)
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('平均依赖等级')
    ax.set_title('(b) 依赖等级演化')
    ax.set_ylim(1, 5)
    ax.grid(True, alpha=0.3)


def _plot_failure_propagation(ax, result):
    """绘制故障传播过程"""
    trajectory = result.get('trust_trajectory', [])
    
    if not trajectory or len(trajectory) < 50:
        ax.text(0.5, 0.5, '数据不足', ha='center', va='center')
        return
    
    # 计算每步的信任度下降速度（近似传播）
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
    
    ax.set_xlabel('仿真步数')
    ax.set_ylabel('传播速度')
    ax.set_title('(c) 故障传播过程')
    ax.axvline(x=50, color='#C44E52', linestyle='--', alpha=0.5)
    ax.grid(True, alpha=0.3)


def _plot_stress_test_comparison(ax, stress_results):
    """绘制压力测试对比"""
    scenarios = list(stress_results.keys())
    trust_drops = [stress_results[s]['trust_drop'] for s in scenarios]
    max_affected = [stress_results[s]['max_affected'] for s in scenarios]
    
    x = np.arange(len(scenarios))
    width = 0.35
    
    # 归一化最大影响人数
    max_aff_normalized = [m / 500 for m in max_affected]
    
    ax.bar(x - width/2, trust_drops, width, label='信任下降', alpha=0.8, color='#C44E52', edgecolor='white', linewidth=0.5)
    ax.bar(x + width/2, max_aff_normalized, width, label='影响范围', alpha=0.8, color='#DD8452', edgecolor='white', linewidth=0.5)
    
    ax.set_ylabel('影响程度')
    ax.set_title('(d) 压力测试场景对比')
    ax.set_xticks(x)
    ax.set_xticklabels([s.replace('_', '\n') for s in scenarios], rotation=0, fontsize=8)
    ax.legend()


def _plot_cascade_size_distribution(ax, stress_results):
    """绘制级联规模分布"""
    cascade_sizes = [stress_results[s]['max_affected'] for s in stress_results.keys()]
    
    if not cascade_sizes:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        return
    
    ax.hist(cascade_sizes, bins=10, alpha=0.75, color='#4C72B0', edgecolor='white', linewidth=0.8)
    ax.axvline(x=np.mean(cascade_sizes), color='#C44E52', linestyle='--', 
              linewidth=2.5, label=f'均值: {np.mean(cascade_sizes):.0f}')
    
    ax.set_xlabel('级联规模（受影响人数）')
    ax.set_ylabel('频次')
    ax.set_title('(e) 级联规模分布')
    ax.legend()


def _plot_resilience_assessment(ax, result, risk_model):
    """绘制系统韧性评估"""
    trajectory = result.get('trust_trajectory', [])
    
    if not trajectory:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center')
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
    categories = ['初始信任', '最低信任', '最终信任', '韧性得分']
    values = [initial_trust, min_trust, final_trust, resilience]
    colors = ['#55A868', '#C44E52', '#4C72B0', '#8172B3']  # 顶刊柔和配色
    
    bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=0.8)
    ax.set_ylabel('得分')
    ax.set_title('(f) 系统韧性评估')
    
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
        resilience_level = '高韧性'
    elif resilience > 0.5:
        resilience_level = '中等韧性'
    else:
        resilience_level = '低韧性'
    
    ax.text(0.5, 0.9, f'韧性等级: {resilience_level}', 
           transform=ax.transAxes, ha='center', fontsize=12, 
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
