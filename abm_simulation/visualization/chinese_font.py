"""字体配置模块
支持中英文字体切换
"""

import matplotlib.pyplot as plt
import matplotlib

def setup_chinese_font():
    """
    设置中文字体
    在 Windows 上使用 SimHei，在 Mac 上使用 Arial Unicode MS
    """
    import platform
    
    system = platform.system()
    
    if system == 'Windows':
        # Windows 使用黑体
        font_list = ['SimHei', 'Microsoft YaHei', 'Microsoft JhengHei', 'Arial Unicode MS']
    elif system == 'Darwin':
        # Mac 使用 Arial Unicode MS 或 PingFang
        font_list = ['Arial Unicode MS', 'PingFang TC', 'Heiti TC', 'SimHei']
    else:
        # Linux 尝试使用文泉驿
        font_list = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
    
    # 设置字体优先级列表
    plt.rcParams['font.sans-serif'] = font_list
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    print(f"已设置中文字体：{font_list}")
    return True

def setup_english_font():
    """
    设置英文字体（Times New Roman）
    用于英文可视化
    """
    # Times New Roman 作为主要字体
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'Georgia', 'Times']
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置字体大小
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    
    print("已设置英文字体：Times New Roman")
    return True

# 默认应用中文字体
setup_chinese_font()
