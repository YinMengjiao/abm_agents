"""
简单图片收集脚本 - 最终版本
从所有实验目录收集 PNG 文件到统一目录
"""
import shutil
from pathlib import Path
import os

# 使用工作目录作为项目根目录
project_root = Path(os.getcwd())

# 输出目录
output_dir = project_root / "results" / "all_experiments_figures"
output_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("ABM 仿真实验 - 图片收集")
print("="*70)
print(f"\n输出目录：{output_dir}\n")

# 实验目录列表 (使用绝对路径)
experiments_dirs = [
    project_root / "experiments" / "baseline_exp1",
    project_root / "experiments" / "experiment2_memory",  # 修正：实验 2 的正确目录
    project_root / "experiments" / "exp3_ai_evolution",
    project_root / "experiments" / "exp4_information_intervention",
    project_root / "experiments" / "exp5_network_structure",
    project_root / "experiments" / "exp6_generational_dynamics",
    project_root / "experiments" / "exp7_ai_competition",
    project_root / "experiments" / "exp8_context_sensitivity",
    project_root / "experiments" / "exp9_filter_bubble",
    project_root / "experiments" / "exp10_systemic_risk",
]

total_count = 0

for exp_dir in experiments_dirs:
    exp_folder = exp_dir.name
    print(f"\n处理实验：{exp_folder}")
    
    # 实验结果目录
    exp_results_dir = exp_dir / "results"
    
    if not exp_results_dir.exists():
        print(f"  ⚠️ 目录不存在：{exp_results_dir}")
        continue
    
    # 递归查找所有 PNG 文件 (包括子目录)
    png_files = list(exp_results_dir.rglob("*.png"))
    
    if not png_files:
        print(f"  ⚠️ 未找到 PNG 文件")
        continue
    
    # 复制到统一目录
    for i, png_file in enumerate(png_files):
        # 重命名文件，添加实验前缀和子目录信息
        relative_path = png_file.relative_to(exp_results_dir)
        
        # 构建文件名
        if str(relative_path.parent) == '.':
            # 直接在 results 目录下的文件
            new_filename = f"{exp_folder}_{png_file.name}"
        else:
            # 在子目录下的文件，添加子目录名
            subdir_name = relative_path.parent.name
            new_filename = f"{exp_folder}_{subdir_name}_{png_file.name}"
        
        dest_path = output_dir / new_filename
        
        shutil.copy2(png_file, dest_path)
        print(f"  ✓ 已复制：{new_filename}")
        total_count += 1

print("\n" + "="*70)
print("图片收集完成！")
print("="*70)

# 显示生成的文件列表
print(f"\n📊 生成的图片文件:")
print(f"   目录：{output_dir}\n")

if output_dir.exists():
    files = sorted(output_dir.glob("*.png"))
    for file in files:
        size_kb = file.stat().st_size / 1024
        print(f"   ✓ {file.name} ({size_kb:.1f} KB)")
    
    print(f"\n总计：{len(files)} 个文件 (共 {total_count} 次复制)")

print("\n" + "="*70)
