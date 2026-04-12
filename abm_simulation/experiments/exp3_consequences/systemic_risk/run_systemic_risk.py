"""
实验10运行脚本: 系统性风险
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

import numpy as np

from experiments.exp3_consequences.systemic_risk.systemic_risk import SystemicRiskModel, StressTestScenarios, FailureType, FailureSeverity
from experiments.exp3_consequences.systemic_risk.visualization_systemic_risk import visualize_systemic_risk_results
from config import RESULTS


def run_experiment10(en: bool = False):
    """
    运行实验10: 系统性风险
    
    Args:
        en: True=英文输出, False=中文输出 (默认)
    """
    print("="*70)
    print("【实验10】系统性风险与级联失效")
    print("研究问题: AI系统故障的社会传染效应？")
    print("="*70)
    
    print(f"\n仿真配置:")
    print(f"  - 消费者数量: 500")
    print(f"  - 仿真步数: 200")
    print(f"  - 故障触发时间: 第50步")
    
    # 创建风险模型
    risk_model = SystemicRiskModel(n_consumers=500)
    
    # 运行主要故障场景
    print("\n【主要故障场景】")
    print("  运行严重技术故障场景...")
    
    main_result = risk_model.run_crisis_simulation(
        failure_type=FailureType.TECHNICAL_OUTAGE,
        severity=FailureSeverity.MAJOR,
        n_steps=200
    )
    
    print(f"\n  故障影响:")
    print(f"    最大受影响人数: {main_result['max_affected']}")
    print(f"    信任度下降: {main_result['trust_drop']:.3f}")
    print(f"    初始信任: {main_result['initial_avg_trust']:.3f}")
    print(f"    最终信任: {main_result['final_avg_trust']:.3f}")
    print(f"    恢复时间: {main_result['recovery_time']}步")
    
    # 压力测试
    print("\n【压力测试场景】")
    stress_test = StressTestScenarios(risk_model)
    stress_results = stress_test.run_all_scenarios()
    
    print(f"\n  各场景对比:")
    print(f"{'场景':<20} {'信任下降':<12} {'最大影响':<12} {'恢复时间':<12}")
    print("-" * 60)
    
    for scenario, result in stress_results.items():
        trust_drop = result['trust_drop']
        max_aff = result['max_affected']
        rec_time = result['recovery_time']
        print(f"{scenario:<20} {trust_drop:<12.3f} {max_aff:<12} {rec_time:<12}")
    
    # 系统韧性指标
    print("\n【系统韧性指标】")
    risk_metrics = risk_model.calculate_systemic_risk_metrics()
    if risk_metrics:
        print(f"  平均级联规模: {risk_metrics.get('avg_cascade_size', 0):.1f}")
        print(f"  最大级联规模: {risk_metrics.get('max_cascade_size', 0)}")
        print(f"  系统韧性得分: {risk_metrics.get('system_resilience', 0):.3f}")
        print(f"  平均恢复时间: {risk_metrics.get('avg_recovery_time', 0):.1f}步")
    
    # 生成可视化
    print("\n" + "="*70)
    print("生成可视化...")
    lang_str = '英文' if en else '中文'
    print(f"语言: {lang_str}")
    visualize_systemic_risk_results(
        main_result, stress_results, risk_model,
        output_dir=RESULTS["exp3_risk"],
        en=en
    )
    
    print("\n" + "="*70)
    print("实验10完成!")
    print("="*70)
    
    return risk_model, main_result, stress_results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='运行实验10: 系统性风险')
    parser.add_argument('--en', action='store_true', help='生成英文版本的图表')
    args = parser.parse_args()
    
    risk_model, main_result, stress_results = run_experiment10(en=args.en)
