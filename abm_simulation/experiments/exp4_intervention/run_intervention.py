"""
实验4运行脚本: 信息干预
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import SimulationConfig
from experiments.exp4_intervention.simulation_intervention import InterventionSimulation
from experiments.exp4_intervention.intervention import InterventionType, InterventionEvent
from experiments.exp4_intervention.visualization_intervention import visualize_all_policy_results
from config import RESULTS


def run_experiment4_policy(policy_type='balanced', en: bool = False):
    """运行指定政策的实验4
    
    Args:
        policy_type: 政策类型
        en: True=英文输出, False=中文输出 (默认)
    """
    print(f"\n{'='*70}")
    print(f"【实验4】信息干预 - 政策类型: {policy_type}")
    print("="*70)
    
    config = SimulationConfig(
        n_consumers=500,
        n_merchants=20,
        n_ai_agents=3,
        network_type='small_world',
        n_steps=300,
        initial_coupling=0.2,
        initial_temperature=2.0,
        enable_adaptive_coupling=True,
    )
    
    print(f"\n仿真配置:")
    print(f"  - 消费者数量: {config.n_consumers}")
    print(f"  - 政策类型: {policy_type}")
    
    # 创建并运行仿真
    sim = InterventionSimulation(config, policy_type=policy_type)
    sim.run()
    
    # 获取结果
    summary = sim.get_summary_statistics()
    
    print("\n【干预效果汇总】")
    if 'intervention_summary' in summary:
        inter = summary['intervention_summary']
        print(f"  总干预次数: {inter.get('total_interventions', 0)}")
        print(f"  受影响消费者总数: {inter.get('total_consumers_affected', 0)}")
        print(f"  高依赖群体平均影响: {summary.get('avg_impact_on_high_dependency', 0):+.1f}人")
        print(f"  总等级变化次数: {summary.get('total_level_changes', 0)}")
    
    print("\n【最终依赖等级分布】")
    final_dist = summary['final_level_distribution']
    for level in range(1, 6):
        count = final_dist.get(level, 0)
        pct = count / config.n_consumers * 100
        print(f"  L{level}: {count} ({pct:.1f}%)")
    
    return sim, summary


def run_experiment4(en: bool = False):
    """运行实验4: 对比不同干预政策
    
    Args:
        en: True=英文输出, False=中文输出 (默认)
    """
    print("="*70)
    print("【实验4】信息干预与政策效果")
    print("研究问题: 外部信息冲击如何改变系统演化？")
    print("="*70)
    
    policies = ['balanced', 'promote_ai', 'protect_consumers']
    results = {}
    
    for policy in policies:
        sim, summary = run_experiment4_policy(policy, en=en)
        results[policy] = (sim, summary)
    
    # 对比分析
    print("\n" + "="*70)
    print("【政策对比分析】")
    print("="*70)
    
    print(f"\n{'政策':<20} {'L5比例':<10} {'L1比例':<10} {'满意度':<10}")
    print("-" * 50)
    
    for policy, (sim, summary) in results.items():
        final_dist = summary['final_level_distribution']
        l5_pct = final_dist.get(5, 0) / 500 * 100
        l1_pct = final_dist.get(1, 0) / 500 * 100
        sat = summary.get('satisfaction', {}).get('mean', 0)
        print(f"{policy:<20} {l5_pct:<10.1f} {l1_pct:<10.1f} {sat:<10.3f}")
    
    # 生成综合图（三种政策合并为一张图）
    print("\n" + "="*70)
    print("生成可视化...")
    lang_str = '英文' if en else '中文'
    print(f"语言: {lang_str}")
    policy_sims = {policy: sim for policy, (sim, _) in results.items()}
    visualize_all_policy_results(policy_sims, output_dir=RESULTS["exp4"], en=en)
    
    print("\n" + "="*70)
    print("实验4完成!")
    print("="*70)
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='运行实验4: 信息干预')
    parser.add_argument('--en', action='store_true', help='生成英文版本的图表')
    args = parser.parse_args()
    
    results = run_experiment4(en=args.en)
