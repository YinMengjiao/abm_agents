"""
实验3运行脚本: AI进化机制
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import SimulationConfig
from experiments.exp2_mechanism.simulation_evolution import EvolutionSimulation
from experiments.exp2_mechanism.visualization_evolution import visualize_evolution_results
from config import RESULTS


def run_experiment3():
    """运行实验3: AI进化机制"""
    print("="*70)
    print("【实验3】AI代理进化机制")
    print("研究问题: AI能否从消费者反馈中学习改进？")
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
    print(f"  - AI代理数量: {config.n_ai_agents}")
    print(f"  - 仿真步数: {config.n_steps}")
    print(f"  - AI进化速率: 0.02")
    
    # 创建并运行仿真
    sim = EvolutionSimulation(config, evolution_rate=0.02)
    sim.run()
    
    # 获取结果
    summary = sim.get_summary_statistics()
    
    print("\n" + "="*70)
    print("仿真结果汇总")
    print("="*70)
    
    # AI进化指标
    if 'evolution_summary' in summary:
        evo = summary['evolution_summary']
        print("\n【AI进化效果】")
        print(f"  错误率变化: {evo['initial_error_rate']:.3f} -> {evo['final_error_rate']:.3f} "
              f"(降低 {evo['error_rate_reduction']:.3f})")
        print(f"  进化进度: {evo['initial_evolution_progress']:.3f} -> {evo['final_evolution_progress']:.3f}")
        print(f"  消费者信任恢复: {evo['trust_recovery']:.3f}")
        print(f"  总学习事件数: {evo['total_learning_events']}")
    
    # AI群体指标
    if 'ai_population_metrics' in summary:
        pop = summary['ai_population_metrics']
        print("\n【AI群体表现】")
        print(f"  平均进化进度: {pop['avg_evolution_progress']:.3f}")
        print(f"  平均错误率: {pop['avg_error_rate']:.3f}")
        print(f"  平均准确度: {pop['avg_accuracy']:.3f}")
        print(f"  最佳AI代理ID: {pop['best_agent_id']}")
    
    # 依赖等级分布
    print("\n【依赖等级分布】")
    final_dist = summary['final_level_distribution']
    for level in range(1, 6):
        count = final_dist.get(level, 0)
        pct = count / config.n_consumers * 100
        print(f"  L{level}: {count} ({pct:.1f}%)")
    
    # 生成可视化
    print("\n" + "="*70)
    print("生成可视化...")
    visualize_evolution_results(sim, output_dir=RESULTS["exp2"])
    
    print("\n" + "="*70)
    print("实验3完成!")
    print("="*70)
    
    return sim, summary


if __name__ == "__main__":
    sim, summary = run_experiment3()
