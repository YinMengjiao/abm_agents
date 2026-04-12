"""
简单图片收集脚本
从所有实验目录收集 PNG 文件到统一目录
"""
import shutil
from pathlib import Path
import os

# 项目根目录
project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 输出目录
output_dir = project_root / "results" / "all_experiments_figures"
output_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("ABM 仿真实验 - 图片收集")
print("="*70)
print(f"\n输出目录：{output_dir}\n")
print(f"项目根目录：{project_root}\n")

# 实验目录列表 (使用正确的相对路径)
experiments = [
    '../experiments/baseline_exp1',
    '../experiments/exp2_consumer_memory',
    '../experiments/exp3_ai_evolution',
    '../experiments/exp4_information_intervention',
    '../experiments/exp5_network_structure',
    '../experiments/exp6_generational_dynamics',
    '../experiments/exp7_ai_competition',
    '../experiments/exp8_context_sensitivity',
    '../experiments/exp9_filter_bubble',
    '../experiments/exp10_systemic_risk',
]

total_count = 0

for exp_folder in experiments:
    print(f"\n处理实验：{exp_folder}")
    
    # 实验结果目录 (使用相对路径)
    exp_results_dir = project_root / exp_folder / "results"
    
    if not exp_results_dir.exists():
        print(f"  ⚠️ 目录不存在：{exp_results_dir}")
        continue
    
    # 查找所有 PNG 文件
    png_files = list(exp_results_dir.glob("*.png"))
    
    if not png_files:
        print(f"  ⚠️ 未找到 PNG 文件")
        continue
    
    # 复制到统一目录
    for png_file in png_files:
        # 重命名文件，添加实验前缀
        new_filename = f"{exp_folder}_{png_file.name}"
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
