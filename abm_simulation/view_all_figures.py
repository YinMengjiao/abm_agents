"""
快速查看所有可视化图表
在默认图片查看器中打开所有图表
"""

import os
import subprocess
from pathlib import Path

def view_all_figures():
    """在默认图片查看器中打开所有图表"""
    
    figures_dir = Path("results/all_figures")
    
    if not figures_dir.exists():
        print(f"错误：图表目录不存在：{figures_dir}")
        print("请先运行：python visualization/collect_all_figures.py")
        return
    
    png_files = list(figures_dir.glob("*.png"))
    
    if not png_files:
        print("错误：未找到任何 PNG 图表文件")
        return
    
    print(f"找到 {len(png_files)} 张图表")
    print("="*60)
    
    # Windows: 使用默认程序打开
    import platform
    system = platform.system()
    
    for i, png_file in enumerate(png_files, 1):
        print(f"[{i}/{len(png_files)}] {png_file.name}")
        
        if system == 'Windows':
            os.startfile(png_file)
        elif system == 'Darwin':  # Mac
            subprocess.run(['open', str(png_file)])
        else:  # Linux
            subprocess.run(['xdg-open', str(png_file)])
    
    print("="*60)
    print(f"已打开所有 {len(png_files)} 张图表")
    print("\n提示：可以使用左右键在图片查看器中浏览")


if __name__ == "__main__":
    view_all_figures()
