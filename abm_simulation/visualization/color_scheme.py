"""
顶刊风格配色方案
基于Nature/Science等顶级期刊的视觉标准
"""

# ===== 主配色方案（柔和、学术） =====
# 适用于折线图、柱状图的主要颜色
MAIN_COLORS = [
    '#4C72B0',  # 柔和蓝
    '#DD8452',  # 暖橙
    '#55A868',  # 自然绿
    '#C44E52',  # 柔和红
    '#8172B3',  # 淡紫
    '#937860',  # 棕褐
    '#DA8BC3',  # 粉紫
    '#8C8C8C',  # 中灰
    '#CCB974',  # 金黄
    '#64B5CD',  # 天蓝
]

# ===== 依赖等级专用配色（L1-L5） =====
LEVEL_COLORS = [
    '#4C72B0',  # L1: 柔和蓝 - 自主
    '#5B9BD5',  # L2: 天蓝 - 信息辅助
    '#55A868',  # L3: 自然绿 - 半委托
    '#DD8452',  # L4: 暖橙 - 高度依赖
    '#C44E52',  # L5: 柔和红 - 完全代理
]

# ===== 热力图配色 =====
HEATMAP_CMAPS = {
    'diverging': 'RdBu_r',      # 发散型（正负值）
    'sequential': 'YlOrBr',     # 连续型（热度）
    'categorical': 'Set3',      # 分类数据
}

# ===== 渐变色板（单色深浅） =====
SEQUENTIAL_BLUE = ['#D6EAF8', '#AED6F1', '#85C1E9', '#5DADE2', '#3498DB', '#2E86C1', '#2874A6', '#1F618D']
SEQUENTIAL_GREEN = ['#D5F5E3', '#ABEBC6', '#82E0AA', '#58D68D', '#2ECC71', '#28B463', '#239B56', '#1D8348']
SEQUENTIAL_ORANGE = ['#FDEBD0', '#FAD7A0', '#F5CBA7', '#F0B27A', '#EB984E', '#E67E22', '#CA6F1E', '#AF601A']
SEQUENTIAL_RED = ['#FADBD8', '#F5B7B1', '#F1948A', '#EC7063', '#E74C3C', '#CB4335', '#B03A2E', '#943126']

# ===== 统计检验显著性标注 =====
SIGNIFICANCE_COLORS = {
    'not_significant': '#95A5A6',  # ns: 灰色
    'p_0.05': '#F39C12',           # *: 橙色
    'p_0.01': '#E67E22',           # **: 深橙
    'p_0.001': '#E74C3C',          # ***: 红色
}

# ===== 背景与网格 =====
BACKGROUND_COLOR = '#FFFFFF'
GRID_COLOR = '#E0E0E0'
GRID_ALPHA = 0.3

# ===== 文本颜色 =====
TEXT_PRIMARY = '#2C3E50'      # 主要文本
TEXT_SECONDARY = '#7F8C8D'    # 次要文本
TEXT_LIGHT = '#BDC3C7'        # 浅色文本

# ===== 特殊用途 =====
POSITIVE_COLOR = '#55A868'    # 正向/增长
NEGATIVE_COLOR = '#C44E52'    # 负向/下降
NEUTRAL_COLOR = '#95A5A6'     # 中性/基准
WARNING_COLOR = '#F39C12'     # 警告
CRITICAL_COLOR = '#E74C3C'    # 严重


def get_level_color(level):
    """获取依赖等级颜色"""
    if 1 <= level <= 5:
        return LEVEL_COLORS[level - 1]
    return TEXT_LIGHT


def get_sequential_color(base_color, intensity, max_intensity=1.0):
    """获取渐变色"""
    import matplotlib.colors as mcolors
    base = mcolors.to_rgba(base_color)
    alpha = min(intensity / max_intensity, 1.0)
    return (*base[:3], alpha)


# matplotlib rcParams 配置建议
MPL_STYLE = {
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#2C3E50',
    'axes.linewidth': 1.0,
    'grid.color': GRID_COLOR,
    'grid.alpha': GRID_ALPHA,
    'text.color': TEXT_PRIMARY,
    'axes.labelcolor': TEXT_PRIMARY,
    'xtick.color': TEXT_PRIMARY,
    'ytick.color': TEXT_PRIMARY,
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
}
