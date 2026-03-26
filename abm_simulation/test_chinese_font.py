"""
测试中文字体并重新生成示例图表
"""

import matplotlib.pyplot as plt
from visualization.chinese_font import setup_chinese_font

# 设置中文字体
setup_chinese_font()

# 创建测试图表
fig, ax = plt.subplots(figsize=(10, 6))

# 测试中文显示
x = [1, 2, 3, 4, 5]
y = [2.3, 4.1, 3.5, 5.2, 4.8]

ax.plot(x, y, marker='o', linewidth=2, markersize=8, label='测试数据')
ax.set_xlabel('X 轴标签（中文测试）', fontsize=12)
ax.set_ylabel('Y 轴标签（中文测试）', fontsize=12)
ax.set_title('中文显示测试图表', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# 保存测试图表
output_path = "results/all_figures/00_中文字体测试.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"✓ 测试图表已保存：{output_path}")

# 验证字体
current_font = plt.rcParams['font.sans-serif'][0]
print(f"当前使用的字体：{current_font}")

# 检查系统中可用的中文字体
from matplotlib import font_manager
chinese_fonts = []
for font in font_manager.fontManager.ttflist:
    if any(keyword in font.name for keyword in ['SimHei', 'Microsoft', 'Chinese', 'CJK']):
        chinese_fonts.append(font.name)

if chinese_fonts:
    print(f"\n系统中可用的中文字体:")
    for font in set(chinese_fonts[:10]):  # 只显示前 10 个
        print(f"  - {font}")
else:
    print("\n⚠ 警告：未找到中文字体，可能需要安装中文字体包")

plt.close()
