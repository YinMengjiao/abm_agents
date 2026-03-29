"""
ABM仿真运行入口
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation import ABMSimulation, SimulationConfig
from visualization.plots import quick_visualize


def main():
    """主函数"""
    print("=" * 60)
    print("AI消费决策依赖梯度ABM仿真")
    print("模型: Ising-D-I-B (Desire-Intention-Behavior)")
    print("=" * 60)
    
    # 配置参数 - 保持在临界附近以维持多样性
    config = SimulationConfig(
        n_consumers=500,           # 消费者数量
        n_merchants=20,            # 商家数量
        n_ai_agents=3,             # AI代理数量
        network_type='small_world', # 社交网络类型
        n_steps=300,               # 仿真步数
        initial_coupling=0.2,      # 降低耦合，避免强极化
        initial_temperature=2.0,   # 提高温度，增加随机性
        enable_adaptive_coupling=True,
        coupling_trend=0.0005,     # 极缓慢增长
        shock_probability=0.05,    # 增加冲击以维持动态
    )
    
    print(f"\n仿真配置:")
    print(f"  - 消费者数量: {config.n_consumers}")
    print(f"  - 商家数量: {config.n_merchants}")
    print(f"  - AI代理数量: {config.n_ai_agents}")
    print(f"  - 仿真步数: {config.n_steps}")
    print(f"  - 网络类型: {config.network_type}")
    
    # 创建并运行仿真
    sim = ABMSimulation(config)
    metrics = sim.run()
    
    # 输出汇总结果
    summary = sim.get_summary_statistics()
    
    print("\n" + "=" * 60)
    print("仿真结果汇总")
    print("=" * 60)
    
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
    print(f"  磁化强度: {mag_trend['initial']:.3f} → {mag_trend['final']:.3f} (变化: {mag_trend['change']:+.3f})")
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
    print("\n" + "=" * 60)
    viz = quick_visualize(sim, output_dir="results")
    
    print("\n仿真完成!")
    print("=" * 60)
    
    return sim, metrics


if __name__ == "__main__":
    sim, metrics = main()
