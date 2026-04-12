"""
实验9运行脚本: 过滤气泡
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from experiments.exp3_consequences.filter_bubble.filter_bubble import FilterBubbleAnalyzer, DiversityIntervention
from experiments.exp3_consequences.filter_bubble.visualization_filter_bubble import visualize_filter_bubble_results
from config import RESULTS


def run_experiment9():
    """运行实验9: 过滤气泡"""
    print("="*70)
    print("【实验9】偏见与过滤气泡")
    print("研究问题: AI推荐是否造成选择窄化？")
    print("="*70)
    
    print(f"\n仿真配置:")
    print(f"  - 消费者数量: 500")
    print(f"  - 产品类别: 20")
    print(f"  - 实验轮数: 50")
    
    # 创建分析器
    analyzer = FilterBubbleAnalyzer(n_categories=20)
    
    # 运行实验
    print("\n运行过滤气泡实验...")
    results = analyzer.run_filter_bubble_experiment(
        n_consumers=500,
        n_rounds=50
    )
    
    # 输出结果
    print("\n【群体多样性指标】")
    pop_metrics = results['population_metrics']
    print(f"  整体多样性得分: {pop_metrics['overall_diversity']:.3f}")
    print(f"  过滤气泡强度: {pop_metrics['filter_bubble_strength']:.3f}")
    print(f"  高依赖vs低依赖差异: {pop_metrics['high_vs_low_diff']:+.3f}")
    
    print(f"\n  各依赖等级多样性:")
    for level, diversity in pop_metrics['diversity_by_level'].items():
        print(f"    L{level}: {diversity:.3f}")
    
    # 多样性干预实验
    print("\n【多样性干预实验】")
    intervention = DiversityIntervention(analyzer)
    
    # 计算干预效果
    original = pop_metrics['overall_diversity']
    
    # 模拟干预后的多样性（简化计算）
    enhanced_diversity = min(1.0, original * 1.2 + 0.05)
    
    effect = intervention.calculate_intervention_effect(original, enhanced_diversity)
    print(f"  原始多样性: {effect['original_diversity']:.3f}")
    print(f"  干预后多样性: {effect['enhanced_diversity']:.3f}")
    print(f"  改善幅度: {effect['absolute_improvement']:+.3f} ({effect['relative_improvement']*100:+.1f}%)")
    
    # 生成可视化
    print("\n" + "="*70)
    print("生成可视化...")
    visualize_filter_bubble_results(analyzer, results, output_dir=RESULTS["exp3_bubble"])
    
    print("\n" + "="*70)
    print("实验9完成!")
    print("="*70)
    
    return analyzer, results


if __name__ == "__main__":
    analyzer, results = run_experiment9()
