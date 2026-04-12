"""
ABM仿真运行入口
支持三种初始化模式：
1. 调查数据驱动（默认）- 使用ACDDS问卷的真实L1-L5分布
2. 交互式手动输入 - 用户自行设定比例
3. 理论默认值 - 使用对称分布假设
"""

import sys
import os
import argparse

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation import ABMSimulation, SimulationConfig
from visualization.plots import quick_visualize


def main(mode: str = 'survey'):
    """
    主函数
    
    Args:
        mode: 初始化模式
            - 'survey': 从 ACDDS调查数据加载（默认）
            - 'interactive': 交互式手动输入
            - 'default': 使用理论默认值
    """
    print("=" * 70)
    print("AI消费决策依赖梯度ABM仿真")
    print("模型: Ising-D-I-B (Desire-Intention-Behavior)")
    print("=" * 70)
    
    if mode == 'survey':
        print("\n📊 模式: 数据驱动初始化（ACDDS调查数据）")
        survey_dist = SimulationConfig.load_survey_distribution()
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
            initial_level_distribution=survey_dist
        )
    
    elif mode == 'interactive':
        print("\n👤 模式: 交互式手动输入")
        user_dist = SimulationConfig.get_user_input_distribution()
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
            initial_level_distribution=user_dist
        )
    
    else:
        print("\n⚙ 模式: 理论默认分布")
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
    print(f"  - 初始化方式: {mode}")
    
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
    parser = argparse.ArgumentParser(description='ABM仿真运行入口')
    parser.add_argument('--mode', type=str, default='survey',
                       choices=['survey', 'interactive', 'default'],
                       help='初始化模式: survey=调查数据, interactive=手动输入, default=理论值')
    args = parser.parse_args()
    
    sim, metrics = main(mode=args.mode)
