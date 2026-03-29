"""
统一可视化收集脚本
运行所有实验并将可视化结果收集到统一目录
"""
import sys
import os
import shutil
from pathlib import Path

# 添加路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_all_experiments():
    """运行所有实验 1-10"""
    
    print("="*70)
    print("ABM 仿真实验 - 统一可视化生成")
    print("="*70)
    
    experiments = [
        ('baseline_exp1', 'run_baseline', 'run_experiment1', 'Baseline Experiment'),
        ('exp2_consumer_memory', 'consumer_with_memory', 'run_experiment2', 'Consumer Memory'),
        ('exp3_ai_evolution', 'ai_evolution', 'run_experiment3', 'AI Evolution'),
        ('exp4_information_intervention', 'intervention', 'run_experiment4', 'Information Intervention'),
        ('exp5_network_structure', 'run_network', 'run_experiment5', 'Network Structure'),
        ('exp6_generational_dynamics', 'run_generational', 'run_experiment6', 'Generational Dynamics'),
        ('exp7_ai_competition', 'run_competition', 'run_experiment7', 'AI Competition'),
        ('exp8_context_sensitivity', 'run_context', 'run_experiment8', 'Context Sensitivity'),
        ('exp9_filter_bubble', 'run_bubble', 'run_experiment9', 'Filter Bubble'),
        ('exp10_systemic_risk', 'run_systemic_risk', 'run_experiment10', 'Systemic Risk'),
    ]
    
    output_dir = Path(project_root) / "results" / "all_experiments_figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n输出目录：{output_dir}\n")
    
    for exp_folder, module_name, func_name, exp_title in experiments:
        try:
            print(f"\n{'='*70}")
            print(f"运行实验：{exp_title}")
            print(f"{'='*70}")
            
            # 动态导入并运行实验
            if exp_folder == 'baseline_exp1':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_baseline')
            elif exp_folder == 'exp2_consumer_memory':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_comparison')
            elif exp_folder == 'exp3_ai_evolution':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_evolution')
            elif exp_folder == 'exp4_information_intervention':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_intervention')
            elif exp_folder == 'exp5_network_structure':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_network')
            elif exp_folder == 'exp6_generational_dynamics':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_generational')
            elif exp_folder == 'exp7_ai_competition':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_competition')
            elif exp_folder == 'exp8_context_sensitivity':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_context')
            elif exp_folder == 'exp9_filter_bubble':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_bubble')
            elif exp_folder == 'exp10_systemic_risk':
                module = __import__(f'experiments.{exp_folder}.{module_name}', fromlist=[''])
                run_func = getattr(module, 'run_systemic_risk')
            else:
                raise ValueError(f"Unknown experiment folder: {exp_folder}")
            
            # 运行实验（不关心返回值）
            run_func()
            
            # 查找并复制图片
            exp_results_dir = Path(project_root) / "experiments" / exp_folder / "results"
            
            if exp_results_dir.exists():
                png_files = list(exp_results_dir.glob("*.png"))
                
                for png_file in png_files:
                    # 重命名文件，添加实验前缀
                    new_filename = f"{exp_folder}_{png_file.name}"
                    dest_path = output_dir / new_filename
                    
                    shutil.copy2(png_file, dest_path)
                    print(f"  ✓ 已复制：{new_filename}")
            
            print(f"✅ 实验 {exp_title} 完成\n")
            
        except Exception as e:
            print(f"❌ 实验 {exp_title} 失败：{str(e)}\n")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("所有实验完成！")
    print("="*70)
    
    # 显示生成的文件列表
    print(f"\n📊 生成的图片文件:")
    print(f"   目录：{output_dir}\n")
    
    if output_dir.exists():
        files = sorted(output_dir.glob("*.png"))
        for file in files:
            size_kb = file.stat().st_size / 1024
            print(f"   ✓ {file.name} ({size_kb:.1f} KB)")
        
        print(f"\n总计：{len(files)} 个文件")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    run_all_experiments()
