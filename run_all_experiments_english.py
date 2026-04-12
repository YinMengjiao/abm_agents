"""
运行所有实验并生成英文版本图片
使用带人口统计信息的ACDDS数据 (acdds_with_demographics.csv)
"""

import sys
import os
from pathlib import Path
import io

# 设置标准输出编码为UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加路径
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abm_simulation')
sys.path.insert(0, project_root)

from simulation import SimulationConfig


def run_all_experiments_english():
    """运行所有实验并生成英文图片"""
    
    print("\n" + "="*70)
    print("🚀 Running All Experiments with Demographics Data (ENGLISH)")
    print("="*70)
    
    # 加载带人口统计信息的数据
    print("\n📊 Loading ACDDS data with demographics...")
    survey_dist = SimulationConfig.load_survey_distribution(with_demographics=True)
    
    print("\n" + "="*70)
    print("Experiment Configuration")
    print("="*70)
    print(f"  - Consumers: 500")
    print(f"  - Merchants: 20")
    print(f"  - AI Agents: 3")
    print(f"  - Simulation Steps: 300")
    print(f"  - Network Type: small_world")
    print(f"  - Language: English")
    print("="*70)
    
    success_exps = []
    failed_exps = []
    
    # ========== 实验 1: 基准动态 ==========
    print("\n" + "="*70)
    print("▶️  Experiment 1: Baseline Dynamics")
    print("="*70)
    try:
        from experiments.exp1_baseline.run_baseline import run_baseline
        sim, summary = run_baseline()
        print("\n✅ Experiment 1 completed!\n")
        success_exps.append(1)
    except Exception as e:
        print(f"\n❌ Experiment 1 failed: {e}\n")
        import traceback
        traceback.print_exc()
        failed_exps.append(1)
    
    # ========== 实验 2: AI进化机制 ==========
    print("\n" + "="*70)
    print("▶️  Experiment 2: AI Agent Evolution")
    print("="*70)
    try:
        from experiments.exp2_mechanism.run_evolution import run_experiment2
        sim, summary = run_experiment2(en=True)
        print("\n✅ Experiment 2 completed!\n")
        success_exps.append(2)
    except Exception as e:
        print(f"\n❌ Experiment 2 failed: {e}\n")
        import traceback
        traceback.print_exc()
        failed_exps.append(2)
    
    # ========== 实验 3-a: 过滤气泡 ==========
    print("\n" + "="*70)
    print("▶️  Experiment 3-a: Filter Bubble")
    print("="*70)
    try:
        from experiments.exp3_consequences.filter_bubble.run_filter_bubble import run_experiment9
        analyzer, bubble_results = run_experiment9(en=True)
        print("\n✅ Experiment 3-a completed!\n")
        success_exps.append(3)
    except Exception as e:
        print(f"\n❌ Experiment 3-a failed: {e}\n")
        import traceback
        traceback.print_exc()
        failed_exps.append(3)
    
    # ========== 实验 3-b: 系统性风险 ==========
    print("\n" + "="*70)
    print("▶️  Experiment 3-b: Systemic Risk")
    print("="*70)
    try:
        from experiments.exp3_consequences.systemic_risk.run_systemic_risk import run_experiment10
        risk_model, main_result, stress_results = run_experiment10(en=True)
        print("\n✅ Experiment 3-b completed!\n")
        success_exps.append(3)
    except Exception as e:
        print(f"\n❌ Experiment 3-b failed: {e}\n")
        import traceback
        traceback.print_exc()
        failed_exps.append(3)
    
    # ========== 实验 4: 信息干预 ==========
    print("\n" + "="*70)
    print("▶️  Experiment 4: Information Intervention")
    print("="*70)
    try:
        from experiments.exp4_intervention.run_intervention import run_experiment4
        results = run_experiment4(en=True)
        print("\n✅ Experiment 4 completed!\n")
        success_exps.append(4)
    except Exception as e:
        print(f"\n❌ Experiment 4 failed: {e}\n")
        import traceback
        traceback.print_exc()
        failed_exps.append(4)
    
    # ========== 对比实验: 初始化方式对比 ==========
    print("\n" + "="*70)
    print("▶️  Comparison Experiment: Survey vs Theoretical Initialization")
    print("="*70)
    try:
        from experiments.exp_comparison_init.run_comparison import InitializationComparisonExperiment
        from experiments.exp_comparison_init.visualization_comparison import create_comparison_visualization
        
        # 运行对比实验
        exp = InitializationComparisonExperiment(
            n_runs=10,
            n_steps=200,
            n_consumers=500
        )
        exp.run_comparison()
        output_dir = exp.save_results()
        
        # 加载结果并生成英文可视化
        import json
        json_path = os.path.join(output_dir, 'comparison_results.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            comparison_results = json.load(f)
        
        create_comparison_visualization(comparison_results, en=True)
        print("\n✅ Comparison Experiment completed!\n")
        success_exps.append('comparison')
    except Exception as e:
        print(f"\n❌ Comparison Experiment failed: {e}\n")
        import traceback
        traceback.print_exc()
        failed_exps.append('comparison')
    
    # ========== 总结 ==========
    print("\n" + "="*70)
    print("🎉 All Experiments Completed!")
    print("="*70)
    print(f"\n✅ Successful: {len(success_exps)} experiments")
    if failed_exps:
        print(f"❌ Failed: {len(failed_exps)} experiments")
    
    print(f"\n📂 Results Location:")
    print(f"   {Path.cwd() / 'abm_simulation' / 'results'}")
    print("\n" + "="*70)


if __name__ == "__main__":
    run_all_experiments_english()
