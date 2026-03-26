"""
实验 8 可视化：情境敏感性
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


def visualize_context_results(runner, output_dir: str):
    """可视化情境敏感性结果"""
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. 各情境AI使用率对比
    ax1 = plt.subplot(2, 3, 1)
    _plot_ai_usage_by_context(ax1, runner)
    
    # 2. 各情境满意度对比
    ax2 = plt.subplot(2, 3, 2)
    _plot_satisfaction_by_context(ax2, runner)
    
    # 3. 情境特征雷达图
    ax3 = plt.subplot(2, 3, 3, projection='polar')
    _plot_context_characteristics_radar(ax3, runner)
    
    # 4. 依赖等级调整效果
    ax4 = plt.subplot(2, 3, 4)
    _plot_level_adjustment(ax4, runner)
    
    # 5. 情境-满意度热力图
    ax5 = plt.subplot(2, 3, 5)
    _plot_context_satisfaction_heatmap(ax5, runner)
    
    # 6. 情境适用性分析
    ax6 = plt.subplot(2, 3, 6)
    _plot_context_suitability(ax6, runner)
    
    plt.suptitle('实验 8: 情境敏感性分析', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 为 suptitle 留出空间
    plt.savefig(f'{output_dir}/context_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 情境分析图已保存：{output_dir}/context_analysis.png")


def _plot_ai_usage_by_context(ax, runner):
    """绘制各情境AI使用率"""
    contexts = []
    usage_rates = []
    
    for context_type, results in runner.results_by_context.items():
        if results:
            usage_rate = sum(1 for r in results if r['uses_ai']) / len(results)
            contexts.append(context_type.replace('_', '\n'))
            usage_rates.append(usage_rate * 100)
    
    colors = plt.cm.RdYlGn(np.array(usage_rates) / 100)
    bars = ax.bar(contexts, usage_rates, color=colors, alpha=0.8)
    
    ax.set_ylabel('AI使用率 (%)')
    ax.set_title('各情境AI使用率对比')
    ax.set_ylim(0, 100)
    ax.tick_params(axis='x', rotation=45)
    
    # 添加数值标签
    for bar, rate in zip(bars, usage_rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{rate:.1f}%', ha='center', va='bottom', fontsize=8)


def _plot_satisfaction_by_context(ax, runner):
    """绘制各情境满意度"""
    contexts = []
    satisfactions = []
    
    for context_type, results in runner.results_by_context.items():
        if results:
            avg_sat = np.mean([r['satisfaction'] for r in results])
            contexts.append(context_type.replace('_', '\n'))
            satisfactions.append(avg_sat)
    
    colors = plt.cm.RdYlGn(np.array(satisfactions))
    bars = ax.bar(contexts, satisfactions, color=colors, alpha=0.8)
    
    ax.set_ylabel('平均满意度')
    ax.set_title('各情境满意度对比')
    ax.set_ylim(0, 1)
    ax.tick_params(axis='x', rotation=45)
    
    # 添加数值标签
    for bar, sat in zip(bars, satisfactions):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{sat:.3f}', ha='center', va='bottom', fontsize=8)


def _plot_context_characteristics_radar(ax, runner):
    """绘制情境特征雷达图"""
    # 选择几个代表性情境
    selected_contexts = [
        'high_freq_low_cost',
        'low_freq_high_cost',
        'time_pressure',
        'social_visible'
    ]
    
    characteristics = ['price_level', 'frequency', 'time_pressure', 
                      'social_visibility', 'ai_suitability']
    labels = ['价格', '频率', '时间压力', '社交可见', 'AI适用']
    
    angles = np.linspace(0, 2*np.pi, len(characteristics), endpoint=False).tolist()
    angles += angles[:1]
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(selected_contexts)))
    
    for i, ctx_name in enumerate(selected_contexts):
        ctx_type = None
        for ct in runner.context_manager.contexts.keys():
            if ct.value == ctx_name:
                ctx_type = ct
                break
        
        if ctx_type:
            ctx = runner.context_manager.contexts[ctx_type]
            values = [
                ctx.price_level,
                ctx.frequency,
                ctx.time_pressure,
                ctx.social_visibility,
                ctx.ai_suitability
            ]
            values += values[:1]
            
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=ctx_name.replace('_', ' '), color=colors[i])
            ax.fill(angles, values, alpha=0.1, color=colors[i])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.set_title('情境特征对比')


def _plot_level_adjustment(ax, runner):
    """绘制依赖等级调整效果"""
    contexts = []
    base_levels = []
    adjusted_levels = []
    
    for context_type, results in runner.results_by_context.items():
        if results:
            avg_base = np.mean([r['base_level'] for r in results])
            avg_adjusted = np.mean([r['adjusted_level'] for r in results])
            contexts.append(context_type.replace('_', '\n'))
            base_levels.append(avg_base)
            adjusted_levels.append(avg_adjusted)
    
    x = np.arange(len(contexts))
    width = 0.35
    
    ax.bar(x - width/2, base_levels, width, label='基础等级', alpha=0.8)
    ax.bar(x + width/2, adjusted_levels, width, label='调整后等级', alpha=0.8)
    
    ax.set_ylabel('依赖等级')
    ax.set_title('情境对依赖等级的影响')
    ax.set_xticks(x)
    ax.set_xticklabels(contexts, rotation=45, ha='right')
    ax.legend()
    ax.set_ylim(0, 5)


def _plot_context_satisfaction_heatmap(ax, runner):
    """绘制情境-满意度热力图"""
    # 按基础依赖等级分组
    level_groups = {i: [] for i in range(1, 6)}
    
    for context_type, results in runner.results_by_context.items():
        for r in results:
            base_level = r['base_level']
            level_groups[base_level].append((context_type, r['satisfaction']))
    
    # 计算每个情境-等级组合的平均满意度
    contexts = list(runner.results_by_context.keys())
    data = np.zeros((5, len(contexts)))
    
    for i, level in enumerate(range(1, 6)):
        for j, ctx in enumerate(contexts):
            sats = [s for c, s in level_groups[level] if c == ctx]
            if sats:
                data[i, j] = np.mean(sats)
            else:
                data[i, j] = 0.5
    
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    ax.set_xticks(range(len(contexts)))
    ax.set_xticklabels([c.replace('_', '\n') for c in contexts], rotation=45, ha='right')
    ax.set_yticks(range(5))
    ax.set_yticklabels([f'L{i+1}' for i in range(5)])
    ax.set_title('情境-等级满意度热力图')
    
    # 添加数值标注
    for i in range(5):
        for j in range(len(contexts)):
            text = ax.text(j, i, f'{data[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=7)
    
    plt.colorbar(im, ax=ax)


def _plot_context_suitability(ax, runner):
    """绘制AI适用性分析"""
    contexts = []
    suitabilities = []
    actual_usage = []
    
    for ctx_type, ctx in runner.context_manager.contexts.items():
        contexts.append(ctx_type.value.replace('_', '\n'))
        suitabilities.append(ctx.ai_suitability)
        
        # 计算实际使用率
        results = runner.results_by_context.get(ctx_type.value, [])
        if results:
            usage = sum(1 for r in results if r['uses_ai']) / len(results)
            actual_usage.append(usage)
        else:
            actual_usage.append(0)
    
    x = np.arange(len(contexts))
    width = 0.35
    
    ax.bar(x - width/2, suitabilities, width, label='AI适用性', alpha=0.8)
    ax.bar(x + width/2, actual_usage, width, label='实际使用率', alpha=0.8)
    
    ax.set_ylabel('分数')
    ax.set_title('AI适用性 vs 实际使用率')
    ax.set_xticks(x)
    ax.set_xticklabels(contexts, rotation=45, ha='right')
    ax.legend()
    ax.set_ylim(0, 1)
