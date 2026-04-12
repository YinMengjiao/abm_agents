"""
实验2对比实验：基线 vs 记忆增强版
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import ABMSimulation, SimulationConfig
from experiments.exp2_consumer_memory.simulation_memory import Experiment2Simulation
from config import RESULTS
import numpy as np


def run_baseline():
    """运行基线实验"""
    print("\n" + "="*70)
    print("【实验1】基线模型 (Baseline)")
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
    
    sim = ABMSimulation(config)
    sim.run()
    
    return sim, sim.get_summary_statistics()


def run_experiment2():
    """运行实验2（记忆增强版）"""
    print("\n" + "="*70)
    print("【实验2】记忆增强模型 (Memory-Enhanced)")
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
    
    sim = Experiment2Simulation(config)
    sim.run()
    
    return sim, sim.get_experiment_summary()


def compare_results(baseline, experiment2):
    """对比两个实验结果"""
    print("\n" + "="*70)
    print("【对比分析】基线 vs 记忆增强版")
    print("="*70)
    
    print("\n【依赖等级分布对比】")
    print(f"{'等级':<12} {'基线':<10} {'记忆增强':<10} {'差异'}")
    print("-" * 50)
    
    for level in range(1, 6):
        base = baseline['final_level_distribution'].get(level, 0)
        exp2 = experiment2['final_level_distribution'].get(level, 0)
        diff = exp2 - base
        diff_str = f"+{diff}" if diff > 0 else str(diff)
        level_names = {1: 'L1自主', 2: 'L2信息辅助', 3: 'L3半委托', 4: 'L4高度依赖', 5: 'L5完全代理'}
        print(f"{level_names[level]:<12} {base:<10} {exp2:<10} {diff_str}")
    
    print("\n【系统指标对比】")
    print(f"{'指标':<20} {'基线':<12} {'记忆增强':<12} {'变化'}")
    print("-" * 60)
    
    metrics = [
        ('磁化强度', baseline['magnetization_trend']['final'], 
         experiment2['magnetization_trend']['final']),
        ('平均满意度', baseline['satisfaction']['mean'], 
         experiment2['satisfaction']['mean']),
        ('AI使用率', baseline['ai_usage'], 
         experiment2['ai_usage']),
        ('错误率', baseline['error_rate'], 
         experiment2['error_rate']),
    ]
    
    for name, base_val, exp2_val in metrics:
        change = ((exp2_val - base_val) / base_val * 100) if base_val != 0 else 0
        change_str = f"{change:+.1f}%"
        print(f"{name:<20} {base_val:<12.3f} {exp2_val:<12.3f} {change_str}")
    
    print("\n【记忆模型特有指标】")
    if 'memory_dynamics' in experiment2:
        md = experiment2['memory_dynamics']
        print(f"  动态信任度: {md['final_avg_dynamic_trust']:.3f}")
        print(f"  平均连续错误: {md['final_avg_consecutive_errors']:.2f}")
        
        # 信任变化趋势
        trust_trend = md['trust_trend']
        if len(trust_trend) > 10:
            early_trust = np.mean(trust_trend[:10])
            late_trust = np.mean(trust_trend[-10:])
            print(f"  信任度变化: {early_trust:.3f} -> {late_trust:.3f} ({late_trust-early_trust:+.3f})")
    
    print("\n【研究发现】")
    # 自动分析
    findings = []
    
    base_l3 = baseline['final_level_distribution'].get(3, 0)
    exp2_l3 = experiment2['final_level_distribution'].get(3, 0)
    if exp2_l3 > base_l3:
        findings.append(f"[1] 记忆机制使 L3 半委托型增加{exp2_l3-base_l3}人，表明消费者更倾向于谨慎评估")
    
    if experiment2['error_rate'] < baseline['error_rate']:
        reduction = (baseline['error_rate'] - experiment2['error_rate']) / baseline['error_rate'] * 100
        findings.append(f"[2] 错误率降低{reduction:.1f}%，记忆学习有效避免了重复错误")
    
    if experiment2['satisfaction']['mean'] > baseline['satisfaction']['mean']:
        findings.append("[3] 满意度提升，经验驱动的决策更符合个体偏好")
    
    if not findings:
        findings.append("[4] 两个模型表现相近，记忆机制在当前参数下影响有限")
    
    for finding in findings:
        print(finding)


def main():
    """主函数"""
    print("="*70)
    print("实验2对比实验：基线模型 vs 记忆增强模型")
    print("="*70)
    
    # 运行基线
    baseline_sim, baseline_results = run_baseline()
    
    # 运行实验2
    memory_sim, experiment2_results = run_experiment2()
    
    # 对比分析
    compare_results(baseline_results, experiment2_results)
    
    # 生成综合图（唯一输出，5×2 子图汇总）
    print("\n" + "="*70)
    print("生成实验 2 综合图...")
    print("="*70)
    from experiments.exp2_consumer_memory.create_summary_plot import create_experiment2_summary
    create_experiment2_summary(
        baseline_sim, memory_sim,
        baseline_results, experiment2_results,
        output_dir=RESULTS["exp2"]
    )
    
    print("\n" + "="*70)
    print("实验完成!")
    print("="*70)


if __name__ == "__main__":
    main()
