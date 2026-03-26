"""
批量重新生成所有可视化图表（带中文支持）
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 必须先导入中文字体配置
from visualization.chinese_font import setup_chinese_font
setup_chinese_font()

print("="*70)
print("批量重新生成可视化图表（带中文支持）")
print("="*70)

# 1. 基线实验
print("\n[1/7] 基线实验...")
try:
    from experiments.baseline_exp1.run_baseline import run_and_visualize
    # 重新运行并生成可视化
    exec(open("experiments/baseline_exp1/run_baseline.py").read())
except Exception as e:
    print(f"  跳过：{e}")

# 2. 实验 2
print("\n[2/7] 实验 2: 消费者记忆...")
try:
    from experiments.exp2_consumer_memory.run_comparison import main as run_exp2
    run_exp2()
except Exception as e:
    print(f"  跳过：{e}")

# 3. 实验 3
print("\n[3/7] 实验 3: AI 进化...")
try:
    from experiments.exp3_ai_evolution.run_evolution import run_experiment3
    run_experiment3()
except Exception as e:
    print(f"  跳过：{e}")

# 4. 实验 4
print("\n[4/7] 实验 4: 信息干预...")
try:
    from experiments.exp4_information_intervention.run_intervention import run_experiment4_policy
    for policy in ['balanced']:
        run_experiment4_policy(policy)
except Exception as e:
    print(f"  跳过：{e}")

# 5. 实验 8
print("\n[5/7] 实验 8: 情境敏感性...")
try:
    from experiments.exp8_context_sensitivity.run_context import run_experiment8
    run_experiment8()
except Exception as e:
    print(f"  跳过：{e}")

# 6. 实验 9
print("\n[6/7] 实验 9: 过滤气泡...")
try:
    from experiments.exp9_filter_bubble.run_filter_bubble import run_experiment9
    run_experiment9()
except Exception as e:
    print(f"  跳过：{e}")

# 7. 实验 10
print("\n[7/7] 实验 10: 系统性风险...")
try:
    from experiments.exp10_systemic_risk.run_systemic_risk import run_experiment10
    run_experiment10()
except Exception as e:
    print(f"  跳过：{e}")

print("\n" + "="*70)
print("所有可视化已重新生成！")
print("="*70)
