"""
快速查看所有综合图
"""

import os
from pathlib import Path

def show_all_summaries():
    """显示所有综合图的信息"""
    
    figures_dir = Path("results/all_figures")
    
    # 综合图列表
    summary_figs = [
        "baseline_summary.png",
        "experiment2_summary.png"
    ]
    
    print("="*70)
    print("综合可视化图表总览")
    print("="*70)
    print()
    
    for fig_name in summary_figs:
        fig_path = figures_dir / fig_name
        
        if fig_path.exists():
            file_size = fig_path.stat().st_size
            
            # 提取实验名称
            exp_name = fig_name.replace("_summary.png", "").replace("_", " ").title()
            
            print(f"📊 {exp_name}")
            print(f"   文件：{fig_name}")
            print(f"   大小：{file_size / 1024:.1f} KB")
            print(f"   路径：{fig_path.absolute()}")
            print()
        else:
            print(f"❌ {fig_name} - 未找到")
            print()
    
    print("="*70)
    print("提示：使用图片查看器打开这些文件查看详细图表")
    print("="*70)
    print()
    
    # Windows 用户可以直接打开
    import platform
    if platform.system() == 'Windows':
        print("Windows 用户可以使用以下命令快速打开：")
        print(f"  start {figures_dir}\\baseline_summary.png")
        print(f"  start {figures_dir}\\experiment2_summary.png")
    elif platform.system() == 'Darwin':
        print("Mac 用户可以使用以下命令快速打开：")
        print(f"  open {figures_dir}/baseline_summary.png")
        print(f"  open {figures_dir}/experiment2_summary.png")
    else:
        print("Linux 用户可以使用以下命令快速打开：")
        print(f"  xdg-open {figures_dir}/baseline_summary.png")
        print(f"  xdg-open {figures_dir}/experiment2_summary.png")


if __name__ == "__main__":
    show_all_summaries()
