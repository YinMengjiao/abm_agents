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
from config import RESULTS


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
        enable_ai_learning=False,  # 基准实验禁用AI学习,保持静态
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
    
    # J扫描实验结果
    print(f"\n  [注意] 平均场近似 J_c^MF ≈ 0.1667,但修改版模型的实测 J_c ≈ 0.453")
    print(f"  基准实验 J 演化范围: 0.20 -> 0.35 (全程处于无序相 J < J_c)")
    print(f"  磁化强度-0.475为瞬态漂移,非稳态有序相")
    
    print("\n【消费者行为】")
    print(f"  平均满意度: {summary['satisfaction']['mean']:.3f}")
    print(f"  AI使用率: {summary['ai_usage']:.3f}")
    print(f"  错误率: {summary['error_rate']:.3f}")
    
    print("\n【网络拓扑】")
    net_metrics = summary['network_metrics']
    print(f"  平均聚类系数: {net_metrics.get('avg_clustering', 0):.3f}")
    print(f"  平均路径长度: {net_metrics.get('avg_path_length', 0):.2f}")
    
    # 生成综合图（唯一输出，3×3 子图汇总）
    print("\n" + "="*70)
    print("生成基线实验综合图...")
    print("="*70)
    from experiments.exp1_baseline.create_baseline_summary import create_baseline_summary
    create_baseline_summary(sim, summary, output_dir=RESULTS["exp1"])
    
    print("\n" + "="*70)
    print("基线实验完成!")
    print("="*70)
    
    return sim, summary


if __name__ == "__main__":
    sim, summary = run_baseline()
