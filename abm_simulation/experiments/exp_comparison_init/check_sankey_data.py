"""验证桑基图数据"""
import json
import numpy as np

# 加载数据
with open('results/comparison_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*70)
print("桑基图数据验证")
print("="*70)

# 初始调查分布
print("\n【初始调查分布】")
survey_init = data['parameters']['survey_distribution']
for level in ['1', '2', '3', '4', '5']:
    pct = survey_init[level] * 100
    print(f"  L{level}: {pct:.2f}%")
total = sum(survey_init.values()) * 100
print(f"  总计: {total:.2f}%")

# 初始理论分布
print("\n【初始理论分布】")
theo_init = data['parameters']['theoretical_distribution']
for level in ['1', '2', '3', '4', '5']:
    pct = theo_init[level] * 100
    print(f"  L{level}: {pct:.2f}%")
total = sum(theo_init.values()) * 100
print(f"  总计: {total:.2f}%")

# 最终调查分布（平均值）
print("\n【最终调查分布 - 平均值】")
survey_finals = [r['final_distribution'] for r in data['results_survey']]
final_counts = []
for level in ['1', '2', '3', '4', '5']:
    vals = [d.get(level, 0) for d in survey_finals]
    mean_val = np.mean(vals)
    final_counts.append(mean_val)
    print(f"  L{level}: {mean_val:.2f}")

total_final = sum(final_counts)
print(f"  总计(人数): {total_final:.2f}")
print(f"  转换为百分比:")
for i, level in enumerate(['1', '2', '3', '4', '5']):
    pct = (final_counts[i] / total_final) * 100 if total_final > 0 else 0
    print(f"    L{level}: {pct:.2f}%")
total_pct = sum([(c / total_final) * 100 for c in final_counts]) if total_final > 0 else 0
print(f"  百分比总计: {total_pct:.2f}%")

# 最终理论分布（平均值）
print("\n【最终理论分布 - 平均值】")
theo_finals = [r['final_distribution'] for r in data['results_theoretical']]
final_counts = []
for level in ['1', '2', '3', '4', '5']:
    vals = [d.get(level, 0) for d in theo_finals]
    mean_val = np.mean(vals)
    final_counts.append(mean_val)
    print(f"  L{level}: {mean_val:.2f}")

total_final = sum(final_counts)
print(f"  总计(人数): {total_final:.2f}")
print(f"  转换为百分比:")
for i, level in enumerate(['1', '2', '3', '4', '5']):
    pct = (final_counts[i] / total_final) * 100 if total_final > 0 else 0
    print(f"    L{level}: {pct:.2f}%")
total_pct = sum([(c / total_final) * 100 for c in final_counts]) if total_final > 0 else 0
print(f"  百分比总计: {total_pct:.2f}%")

print("\n" + "="*70)
print("当前代码显示格式: :.1f (小数点后1位)")
print("建议修改为: :.2f (小数点后2位)")
print("="*70)
