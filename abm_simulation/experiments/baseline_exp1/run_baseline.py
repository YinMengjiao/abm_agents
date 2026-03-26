"""
基线实验 (Experiment 1)
Ising-D-I-B基础模型
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import ABMSimulation, SimulationConfig
from visualization.plots import quick_visualize


def run_baseline():
    """运行基线实验"""
    print("="*70)
    print("【实验1】基线模型 (Baseline)")
    print("Ising-D-I-B基础模型")
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
        coupling_trend=0.0005,
        shock_probability=0.05,
    )
    
    print(f"\n仿真配置:")
    print(f"  - 消费者数量: {config.n_consumers}")
    print(f"  - 商家数量: {config.n_merchants}")
    print(f"  - AI代理数量: {config.n_ai_agents}")
    print(f"  - 仿真步数: {config.n_steps}")
    print(f"  - 网络类型: {config.network_type}")
    
    # 创建并运行仿真
    sim = ABMSimulation(config)
    sim.run()
    
    # 输出汇总结果
    summary = sim.get_summary_statistics()
    
    print("\n" + "="*70)
    print("仿真结果汇总")
    print("="*70)
    
    print("\n【依赖等级分布演化】")
    init_dist = sim.metrics_history[0].level_distribution if sim.metrics_history else {}
    final_dist = summary['final_level_distribution']
    
    level_names = {1: 'L1自主', 2: 'L2信息辅助', 3: 'L3半委托', 4: 'L4高度依赖', 5: 'L5完全代理'}
    
    print(f"{'等级':<12} {'初始':<10} {'最终':<10} {'变化'}")
    print("-" * 45)
    for level in range(1, 6):
        init = init_dist.get(level, 0)
        final = final_dist.get(level, 0)
        change = final - init
        change_str = f"+{change}" if change > 0 else str(change)
        print(f"{level_names[level]:<12} {init:<10} {final:<10} {change_str}")
    
    print("\n【Ising动力学】")
    mag_trend = summary['magnetization_trend']
    print(f"  磁化强度: {mag_trend['initial']:.3f} -> {mag_trend['final']:.3f} (变化: {mag_trend['change']:+.3f})")
    print(f"  临界耦合强度: {sim.network.get_critical_J():.4f}")
    
    print("\n【消费者行为】")
    print(f"  平均满意度: {summary['satisfaction']['mean']:.3f}")
    print(f"  AI使用率: {summary['ai_usage']:.3f}")
    print(f"  错误率: {summary['error_rate']:.3f}")
    
    print("\n【网络拓扑】")
    net_metrics = summary['network_metrics']
    print(f"  平均聚类系数: {net_metrics.get('avg_clustering', 0):.3f}")
    print(f"  平均路径长度: {net_metrics.get('avg_path_length', 0):.2f}")
    
    # 生成可视化
    print("\n" + "="*70)
    viz = quick_visualize(sim, output_dir="experiments/baseline_exp1/results")
    
    # 生成综合图
    print("\n" + "="*70)
    print("生成基线实验综合图...")
    print("="*70)
    from experiments.baseline_exp1.create_baseline_summary import create_baseline_summary
    create_baseline_summary(sim, summary, output_dir="results/all_figures")
    
    print("\n" + "="*70)
    print("基线实验完成!")
    print("="*70)
    
    return sim, summary


if __name__ == "__main__":
    sim, summary = run_baseline()
