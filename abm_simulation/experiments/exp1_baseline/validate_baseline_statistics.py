"""
基线实验统计验证:20次独立运行,报告⟨M⟩和std
验证无序相涨落是否符合理论预期σ_M ≈ 1/√N
"""

import sys
import os
import numpy as np

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import ABMSimulation, SimulationConfig


def run_baseline_statistics():
    """
    运行20次独立基线实验,统计磁化强度
    
    验证:
    1. ⟨|M|⟩应该接近0 (无序相)
    2. std(|M|)应该接近1/√N ≈ 0.045 (有限尺寸涨落)
    3. -0.475这样的极端值是否合理
    """
    print("="*70)
    print("基线实验统计验证:20次独立运行")
    print("="*70)
    
    n_runs = 20
    n_consumers = 500
    n_steps = 300
    
    print(f"\n配置:")
    print(f"  运行次数: {n_runs}")
    print(f"  消费者数量: {n_consumers}")
    print(f"  仿真步数: {n_steps}")
    print(f"  J演化: 0.20 -> 0.35 (全程无序相)")
    print(f"  理论预期: σ_M ≈ 1/√N = {1/np.sqrt(n_consumers):.4f}")
    print("="*70)
    
    final_M_values = []
    final_level_distributions = []
    
    for run in range(n_runs):
        # 设置随机种子
        seed = run * 12345
        np.random.seed(seed)
        
        config = SimulationConfig(
            n_consumers=n_consumers,
            n_merchants=20,
            n_ai_agents=3,
            network_type='small_world',
            n_steps=n_steps,
            initial_coupling=0.2,
            initial_temperature=2.0,
            enable_adaptive_coupling=True,
            coupling_trend=0.0005,
            shock_probability=0.05,
            enable_ai_learning=False,
        )
        
        sim = ABMSimulation(config)
        sim.run()
        
        # 记录最终磁化强度
        final_M = sim.metrics_history[-1].magnetization
        final_M_values.append(final_M)
        
        # 记录最终等级分布
        final_dist = sim.metrics_history[-1].level_distribution
        final_level_distributions.append(final_dist)
        
        # 进度
        if (run + 1) % 5 == 0:
            avg_dist = {level: 0 for level in range(1, 6)}
            for dist in final_level_distributions:
                for level, count in dist.items():
                    avg_dist[level] += count
            for level in avg_dist:
                avg_dist[level] /= len(final_level_distributions)
            
            print(f"\n运行 {run+1}/{n_runs}: M = {final_M:.4f}")
            print(f"  当前平均分布: L1={avg_dist[1]:.0f}, L2={avg_dist[2]:.0f}, "
                  f"L3={avg_dist[3]:.0f}, L4={avg_dist[4]:.0f}, L5={avg_dist[5]:.0f}")
    
    # 统计分析
    M_array = np.array(final_M_values)
    abs_M_array = np.abs(M_array)
    
    print("\n" + "="*70)
    print("统计结果")
    print("="*70)
    
    print(f"\n磁化强度 M:")
    print(f"  均值 ⟨M⟩ = {np.mean(M_array):.4f}")
    print(f"  标准差 σ_M = {np.std(M_array):.4f}")
    print(f"  最小值 = {np.min(M_array):.4f}")
    print(f"  最大值 = {np.max(M_array):.4f}")
    print(f"  理论预期 σ_M ≈ 1/√N = {1/np.sqrt(n_consumers):.4f}")
    print(f"  比值 (实测/理论) = {np.std(M_array) / (1/np.sqrt(n_consumers)):.2f}")
    
    print(f"\n平均磁化强度 |M|:")
    print(f"  均值 ⟨|M|⟩ = {np.mean(abs_M_array):.4f}")
    print(f"  标准差 = {np.std(abs_M_array):.4f}")
    
    print(f"\n极端值检验:")
    print(f"  最大|M| = {np.max(abs_M_array):.4f}")
    print(f"  最大|M|/σ_M = {np.max(abs_M_array) / np.std(M_array):.2f}σ")
    print(f"  出现-0.475这样的值的概率: < 10^(-{int(np.log10(1/np.max(abs_M_array)))})")
    
    # 平均等级分布
    avg_dist = {level: 0 for level in range(1, 6)}
    for dist in final_level_distributions:
        for level, count in dist.items():
            avg_dist[level] += count
    for level in avg_dist:
        avg_dist[level] /= n_runs
    
    print(f"\n平均依赖等级分布 (20次运行):")
    level_names = {1: 'L1自主', 2: 'L2信息辅助', 3: 'L3半委托', 
                   4: 'L4高度依赖', 5: 'L5完全代理'}
    for level in range(1, 6):
        print(f"  {level_names[level]:<12}: {avg_dist[level]:<6.1f} ({avg_dist[level]/n_consumers*100:.1f}%)")
    
    # 结论
    print("\n" + "="*70)
    print("结论")
    print("="*70)
    
    if np.mean(M_array) < 0.1 and np.std(M_array) < 0.1:
        print("\n✓ 基线实验确认处于无序相:⟨M⟩接近零,涨落符合有限尺寸预期")
    else:
        print("\n✗ 警告:基线可能接近临界区或有序相")
    
    if np.max(abs_M_array) > 0.3:
        print(f"✗ 警告:出现极端涨落|M|={np.max(abs_M_array):.3f},需检查随机种子或代码差异")
    else:
        print(f"✓ 最大涨落在合理范围内:|M|_max = {np.max(abs_M_array):.3f}")
    
    print("\n" + "="*70)
    print("统计验证完成!")
    print("="*70)
    
    return {
        'M_values': M_array,
        'avg_M': np.mean(M_array),
        'std_M': np.std(M_array),
        'avg_abs_M': np.mean(abs_M_array),
        'max_abs_M': np.max(abs_M_array),
        'avg_level_distribution': avg_dist,
        'n_runs': n_runs
    }


if __name__ == "__main__":
    stats = run_baseline_statistics()
