"""
实验2可视化对比模块
对比基线模型和记忆增强模型的结果
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from typing import Dict, List, Tuple
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class Experiment2Visualizer:
    """实验2可视化器"""
    
    def __init__(self, output_dir: str = "experiments/experiment2_memory/results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_level_distribution_comparison(self, 
                                          baseline_dist: Dict[int, int],
                                          memory_dist: Dict[int, int],
                                          save: bool = True):
        """对比依赖等级分布"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
        
        levels = list(range(1, 6))
        level_names = ['L1\n自主', 'L2\n信息辅助', 'L3\n半委托', 'L4\n高度依赖', 'L5\n完全代理']
        
        base_counts = [baseline_dist.get(l, 0) for l in levels]
        memory_counts = [memory_dist.get(l, 0) for l in levels]
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        # 基线分布
        bars1 = ax1.bar(level_names, base_counts, color=colors, edgecolor='black', alpha=0.8)
        ax1.set_ylabel('智能体数量', fontsize=12)
        ax1.set_title('基线模型', fontsize=13, fontweight='bold')
        ax1.grid(True, axis='y', alpha=0.3)
        for bar, count in zip(bars1, base_counts):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                    f'{count}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 记忆增强分布
        bars2 = ax2.bar(level_names, memory_counts, color=colors, edgecolor='black', alpha=0.8)
        ax2.set_ylabel('智能体数量', fontsize=12)
        ax2.set_title('记忆增强模型', fontsize=13, fontweight='bold')
        ax2.grid(True, axis='y', alpha=0.3)
        for bar, count in zip(bars2, memory_counts):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                    f'{count}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 差异对比
        differences = [m - b for m, b in zip(memory_counts, base_counts)]
        colors_diff = ['green' if d > 0 else 'red' for d in differences]
        bars3 = ax3.bar(level_names, differences, color=colors_diff, edgecolor='black', alpha=0.7)
        ax3.set_ylabel('数量差异（记忆-基线）', fontsize=12)
        ax3.set_title('分布差异', fontsize=13, fontweight='bold')
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax3.grid(True, axis='y', alpha=0.3)
        for bar, diff in zip(bars3, differences):
            y_pos = bar.get_height() + 3 if diff > 0 else bar.get_height() - 8
            ax3.text(bar.get_x() + bar.get_width()/2., y_pos,
                    f'{diff:+d}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.suptitle('依赖等级分布对比：基线 vs 记忆增强', fontsize=15, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save:
            plt.savefig(f"{self.output_dir}/level_distribution_comparison.png", 
                       dpi=150, bbox_inches='tight')
            print(f"  保存: level_distribution_comparison.png")
        plt.close()
    
    def plot_metrics_comparison(self,
                               baseline_metrics: List,
                               memory_metrics: List,
                               save: bool = True):
        """对比系统指标演化"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        steps = [m.step for m in baseline_metrics]
        
        # 满意度对比
        ax = axes[0, 0]
        base_sat = [m.avg_satisfaction for m in baseline_metrics]
        mem_sat = [m.avg_satisfaction for m in memory_metrics]
        ax.plot(steps, base_sat, 'b-', label='基线', linewidth=2, alpha=0.8)
        ax.plot(steps, mem_sat, 'r-', label='记忆增强', linewidth=2, alpha=0.8)
        ax.fill_between(steps, base_sat, mem_sat, alpha=0.2, color='gray')
        ax.set_ylabel('平均满意度', fontsize=11)
        ax.set_title('满意度演化对比', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        
        # AI使用率对比
        ax = axes[0, 1]
        base_ai = [m.ai_usage_rate for m in baseline_metrics]
        mem_ai = [m.ai_usage_rate for m in memory_metrics]
        ax.plot(steps, base_ai, 'b-', label='基线', linewidth=2, alpha=0.8)
        ax.plot(steps, mem_ai, 'r-', label='记忆增强', linewidth=2, alpha=0.8)
        ax.fill_between(steps, base_ai, mem_ai, alpha=0.2, color='gray')
        ax.set_ylabel('AI使用率', fontsize=11)
        ax.set_title('AI使用率演化对比', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        
        # 错误率对比
        ax = axes[1, 0]
        base_err = [m.error_rate for m in baseline_metrics]
        mem_err = [m.error_rate for m in memory_metrics]
        ax.plot(steps, base_err, 'b-', label='基线', linewidth=2, alpha=0.8)
        ax.plot(steps, mem_err, 'r-', label='记忆增强', linewidth=2, alpha=0.8)
        ax.fill_between(steps, base_err, mem_err, alpha=0.2, color='gray')
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('错误率', fontsize=11)
        ax.set_title('错误率演化对比', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # 磁化强度对比
        ax = axes[1, 1]
        base_mag = [m.magnetization for m in baseline_metrics]
        mem_mag = [m.magnetization for m in memory_metrics]
        ax.plot(steps, base_mag, 'b-', label='基线', linewidth=2, alpha=0.8)
        ax.plot(steps, mem_mag, 'r-', label='记忆增强', linewidth=2, alpha=0.8)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        ax.fill_between(steps, base_mag, mem_mag, alpha=0.2, color='gray')
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('磁化强度', fontsize=11)
        ax.set_title('系统极化程度对比', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.suptitle('系统指标演化对比', fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        if save:
            plt.savefig(f"{self.output_dir}/metrics_comparison.png", 
                       dpi=150, bbox_inches='tight')
            print(f"  保存: metrics_comparison.png")
        plt.close()
    
    def plot_memory_dynamics(self,
                            memory_stats_history: List[Dict],
                            save: bool = True):
        """绘制记忆模型特有的动态指标"""
        if not memory_stats_history:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        steps = [m['step'] for m in memory_stats_history]
        
        # 动态信任度
        ax = axes[0, 0]
        trust_values = [m['avg_dynamic_trust'] for m in memory_stats_history]
        ax.plot(steps, trust_values, 'g-', linewidth=2)
        ax.set_ylabel('平均动态信任度', fontsize=11)
        ax.set_title('消费者对AI的动态信任演化', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        
        # 连续错误
        ax = axes[0, 1]
        consecutive_errors = [m['avg_consecutive_errors'] for m in memory_stats_history]
        ax.plot(steps, consecutive_errors, 'r-', linewidth=2)
        ax.set_ylabel('平均连续错误次数', fontsize=11)
        ax.set_title('错误累积情况', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 信任度分布（箱线图）
        ax = axes[1, 0]
        # 每50步采样一次信任分布
        sample_indices = list(range(0, len(trust_values), max(1, len(trust_values)//5)))
        sampled_trust = [trust_values[i] for i in sample_indices]
        sampled_labels = [f'{steps[i]}' for i in sample_indices]
        ax.bar(range(len(sampled_trust)), sampled_trust, color='steelblue', edgecolor='black')
        ax.set_xticks(range(len(sampled_trust)))
        ax.set_xticklabels(sampled_labels)
        ax.set_xlabel('仿真步数', fontsize=11)
        ax.set_ylabel('平均信任度', fontsize=11)
        ax.set_title('信任度关键节点', fontsize=12, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        
        # 信任变化率
        ax = axes[1, 1]
        if len(trust_values) > 10:
            trust_change = np.diff(trust_values, prepend=trust_values[0])
            window = 20
            trust_change_smooth = np.convolve(trust_change, np.ones(window)/window, mode='valid')
            ax.plot(steps[window-1:], trust_change_smooth, 'purple', linewidth=2)
            ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
            ax.set_xlabel('仿真步数', fontsize=11)
            ax.set_ylabel('信任度变化率（平滑）', fontsize=11)
            ax.set_title('信任度变化趋势', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        plt.suptitle('记忆模型特有指标：信任动态', fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        if save:
            plt.savefig(f"{self.output_dir}/memory_dynamics.png", 
                       dpi=150, bbox_inches='tight')
            print(f"  保存: memory_dynamics.png")
        plt.close()
    
    def plot_summary_radar(self,
                          baseline_summary: Dict,
                          memory_summary: Dict,
                          save: bool = True):
        """雷达图对比关键指标"""
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # 指标标准化到0-1
        categories = ['满意度', 'AI使用率', '1-错误率', 'L3占比', '系统平衡度']
        
        # 基线数据
        base_values = [
            baseline_summary['satisfaction']['mean'],
            baseline_summary['ai_usage'],
            1 - baseline_summary['error_rate'],
            baseline_summary['final_level_distribution'].get(3, 0) / 500,
            1 - abs(baseline_summary['magnetization_trend']['final'])
        ]
        
        # 记忆增强数据
        memory_values = [
            memory_summary['satisfaction']['mean'],
            memory_summary['ai_usage'],
            1 - memory_summary['error_rate'],
            memory_summary['final_level_distribution'].get(3, 0) / 500,
            1 - abs(memory_summary['magnetization_trend']['final'])
        ]
        
        # 角度
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        base_values += base_values[:1]
        memory_values += memory_values[:1]
        angles += angles[:1]
        
        # 绘制
        ax.plot(angles, base_values, 'o-', linewidth=2, label='基线', color='blue')
        ax.fill(angles, base_values, alpha=0.25, color='blue')
        ax.plot(angles, memory_values, 'o-', linewidth=2, label='记忆增强', color='red')
        ax.fill(angles, memory_values, alpha=0.25, color='red')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)
        ax.set_ylim(0, 1)
        ax.set_title('综合指标雷达图对比', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=11)
        ax.grid(True)
        
        if save:
            plt.savefig(f"{self.output_dir}/summary_radar.png", 
                       dpi=150, bbox_inches='tight')
            print(f"  保存: summary_radar.png")
        plt.close()
    
    def generate_all_comparison_plots(self,
                                     baseline_sim,
                                     memory_sim,
                                     baseline_summary,
                                     memory_summary):
        """生成所有对比图表"""
        print("\n生成实验2对比可视化图表...")
        
        self.plot_level_distribution_comparison(
            baseline_summary['final_level_distribution'],
            memory_summary['final_level_distribution']
        )
        
        self.plot_metrics_comparison(
            baseline_sim.metrics_history,
            memory_sim.metrics_history
        )
        
        if hasattr(memory_sim, 'memory_statistics_history'):
            self.plot_memory_dynamics(memory_sim.memory_statistics_history)
        
        self.plot_summary_radar(baseline_summary, memory_summary)
        
        print(f"\n所有图表已保存到: {self.output_dir}/")


def create_comparison_visualization(baseline_sim, memory_sim, 
                                   baseline_summary, memory_summary):
    """快速创建对比可视化"""
    viz = Experiment2Visualizer()
    viz.generate_all_comparison_plots(baseline_sim, memory_sim, 
                                     baseline_summary, memory_summary)
    return viz


if __name__ == "__main__":
    print("实验2可视化模块已加载")
