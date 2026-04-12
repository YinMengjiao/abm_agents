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

# 1. exp1 基准动态
print("\n[1/4] exp1 基准动态...")
try:
    from experiments.exp1_baseline.run_baseline import run_baseline
    run_baseline()
except Exception as e:
    print(f"  跳过：{e}")

# 2. exp2 扩散机制: AI进化
print("\n[2/4] exp2 扩散机制: AI 进化...")
try:
    from experiments.exp2_mechanism.run_evolution import run_experiment3 as run_exp2
    run_exp2()
except Exception as e:
    print(f"  跳过：{e}")

# 3. exp3 系统后果: 过滤气泡 + 系统性风险
print("\n[3/4] exp3 系统后果: 过滤气泡...")
try:
    from experiments.exp3_consequences.filter_bubble.run_filter_bubble import run_experiment9 as run_bubble
    run_bubble()
except Exception as e:
    print(f"  跳过：{e}")

print("\n[3/4] exp3 系统后果: 系统性风险...")
try:
    from experiments.exp3_consequences.systemic_risk.run_systemic_risk import run_experiment10 as run_risk
    run_risk()
except Exception as e:
    print(f"  跳过：{e}")

# 4. exp4 政策干预
print("\n[4/4] exp4 政策干预: 信息干预...")
try:
    from experiments.exp4_intervention.run_intervention import run_experiment4
    run_experiment4()
except Exception as e:
    print(f"  跳过：{e}")

print("\n" + "="*70)
print("所有可视化已重新生成！")
print("="*70)
