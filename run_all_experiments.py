"""
批量运行所有 ABM 实验并生成完整可视化图集

功能:
    1. 自动运行所有 10 个实验
    2. 支持自定义初始参数配置
    3. 生成统一的可视化结果目录
    4. 输出详细的实验报告

使用方法:
    python run_all_experiments.py
    
自定义参数:
    修改下方的 CONFIG 字典即可
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# ============================================================================
# 🔧 自定义配置区域 (修改这里的参数)
# ============================================================================

CONFIG = {
    # ========== 基础参数 ==========
    'num_consumers': 500,        # 消费者数量
    'num_merchants': 20,         # 商家数量
    'num_ai_agents': 3,          # AI 代理数量
    'num_steps': 300,            # 仿真步数
    'network_type': 'small_world',  # 网络类型：small_world/random/scale_free/chain
    
    # ========== Ising 模型参数 ==========
    'initial_coupling': 0.2,     # 初始耦合强度 (J)
    'initial_temperature': 2.0,  # 初始温度
    'enable_adaptive_coupling': True,  # 是否启用自适应耦合
    'coupling_trend': 0.0005,    # 耦合变化趋势
    
    # ========== 外部冲击参数 ==========
    'shock_probability': 0.05,   # 外部冲击概率
    
    # ========== 初始依赖等级分布 (L1-L5) ==========
    # 注意：所有比例之和必须等于 1.0
    'level_distribution': {
        1: 0.04,  # L1: 自主型 (10%)
        2: 0.26,  # L2: 信息辅助 (25%)
        3: 0.46,  # L3: 半委托 (30%)
        4: 0.21,  # L4: 高度依赖 (25%)
        5: 0.03,  # L5: 完全代理 (10%)
    },
    
    # ========== 实验控制 ==========
    'experiments_to_run': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # 要运行的实验编号
    'generate_visualizations': True,  # 是否生成可视化图表
    'save_results': True,  # 是否保存结果
}

# ============================================================================


# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'abm_simulation'))

def print_config(config):
    """打印配置信息"""
    print("\n" + "="*70)
    print("⚙️  实验配置")
    print("="*70)
    
    print(f"\n📊 基础参数:")
    print(f"   消费者数量：{config['num_consumers']}")
    print(f"   商家数量：{config['num_merchants']}")
    print(f"   AI 代理数量：{config['num_ai_agents']}")
    print(f"   仿真步数：{config['num_steps']}")
    print(f"   网络类型：{config['network_type']}")
    
    print(f"\n⚛️  Ising 模型参数:")
    print(f"   初始耦合强度：{config['initial_coupling']}")
    print(f"   初始温度：{config['initial_temperature']}")
    print(f"   自适应耦合：{'是' if config['enable_adaptive_coupling'] else '否'}")
    print(f"   耦合趋势：{config['coupling_trend']}")
    
    print(f"\n🌊 外部冲击:")
    print(f"   冲击概率：{config['shock_probability']}")
    
    print(f"\n👥 初始依赖等级分布:")
    level_names = {
        1: 'L1 自主',
        2: 'L2 信息辅助',
        3: 'L3 半委托',
        4: 'L4 高度依赖',
        5: 'L5 完全代理'
    }
    for level, ratio in sorted(config['level_distribution'].items()):
        bar = '█' * int(ratio * 20)
        print(f"   {level_names[level]:<12}: {ratio*100:5.1f}%  {bar}")
    
    total = sum(config['level_distribution'].values())
    print(f"\n   总和：{total:.4f} {'✓' if abs(total - 1.0) < 0.001 else '✗ 警告：不等于 1.0!'}")
    
    print(f"\n🎯 实验计划:")
    print(f"   运行实验：{config['experiments_to_run']}")
    print(f"   生成可视化：{'是' if config['generate_visualizations'] else '否'}")
    print(f"   保存结果：{'是' if config['save_results'] else '否'}")
    
    print("\n" + "="*70)


def validate_config(config):
    """验证配置的有效性"""
    # 检查 L1-L5 分布
    total = sum(config['level_distribution'].values())
    if abs(total - 1.0) > 0.001:
        print(f"\n❌ 错误：L1-L5 分布总和 ({total:.4f}) 不等于 1.0!")
        print("请调整配置中的 level_distribution 参数")
        return False
    
    # 检查实验编号
    valid_exps = set(range(1, 11))
    requested_exps = set(config['experiments_to_run'])
    invalid = requested_exps - valid_exps
    if invalid:
        print(f"\n❌ 错误：无效的实验编号：{invalid}")
        print("有效的实验编号为 1-10")
        return False
    
    return True


def run_experiment(exp_num, config):
    """运行单个实验"""
    print(f"\n{'='*70}")
    print(f"▶️  开始实验 {exp_num}")
    print(f"{'='*70}\n")
    
    try:
        # 根据实验编号导入并运行
        if exp_num == 1:
            from experiments.baseline_exp1.run_baseline import run_baseline
            sim, summary = run_baseline()
            
        elif exp_num == 2:
            from experiments.exp2_consumer_memory.run_comparison import main as exp2_main
            exp2_main()
            
        elif exp_num == 3:
            from experiments.exp3_ai_evolution.run_evolution import run_experiment3
            sim, summary = run_experiment3()
            
        elif exp_num == 4:
            from experiments.exp4_information_intervention.run_intervention import run_experiment4
            results = run_experiment4()
            
        elif exp_num == 5:
            from experiments.exp5_network_structure.run_network import run_experiment5
            run_experiment5()
            
        elif exp_num == 6:
            from experiments.exp6_generational_dynamics.run_generational import run_experiment6
            runner, results = run_experiment6()
            
        elif exp_num == 7:
            from experiments.exp7_ai_competition.run_competition import run_experiment7
            sim, summary = run_experiment7()
            
        elif exp_num == 8:
            from experiments.exp8_context_sensitivity.run_context import run_experiment8
            runner, results = run_experiment8()
            
        elif exp_num == 9:
            from experiments.exp9_filter_bubble.run_filter_bubble import run_experiment9
            analyzer, results = run_experiment9()
            
        elif exp_num == 10:
            from experiments.exp10_systemic_risk.run_systemic_risk import run_experiment10
            risk_model, main_result, stress_results = run_experiment10()
        
        print(f"\n✅ 实验 {exp_num} 完成!\n")
        return True
        
    except ImportError as e:
        print(f"\n❌ 实验 {exp_num} 导入失败：{e}\n")
        return False
    except Exception as e:
        print(f"\n❌ 实验 {exp_num} 运行出错：{e}\n")
        import traceback
        traceback.print_exc()
        return False


def clear_old_results():
    """清空旧的实验结果和图表"""
    print("\n" + "="*70)
    print("🗑️  清空旧的实验结果")
    print("="*70)
    
    import shutil
    
    # 实验目录列表
    experiments_dirs = [
        Path.cwd() / "experiments" / "baseline_exp1" / "results",
        Path.cwd() / "experiments" / "experiment2_memory" / "results",
        Path.cwd() / "experiments" / "exp3_ai_evolution" / "results",
        Path.cwd() / "experiments" / "exp4_information_intervention" / "results",
        Path.cwd() / "experiments" / "exp5_network_structure" / "results",
        Path.cwd() / "experiments" / "exp6_generational_dynamics" / "results",
        Path.cwd() / "experiments" / "exp7_ai_competition" / "results",
        Path.cwd() / "experiments" / "exp8_context_sensitivity" / "results",
        Path.cwd() / "experiments" / "exp9_filter_bubble" / "results",
        Path.cwd() / "experiments" / "exp10_systemic_risk" / "results",
    ]
    
    # 统一输出目录
    unified_output_dir = Path.cwd() / "results" / "all_experiments_figures"
    
    # results 根目录
    results_root = Path.cwd() / "results"
    
    # 实验报告目录
    report_dir = Path.cwd() / "results"
    
    deleted_count = 0
    
    # 删除各实验的 results 目录
    for exp_results_dir in experiments_dirs:
        if exp_results_dir.exists():
            try:
                # 删除目录下的所有 PNG 文件
                for png_file in exp_results_dir.glob("*.png"):
                    png_file.unlink()
                    deleted_count += 1
                print(f"  ✓ 清空：{exp_results_dir.relative_to(Path.cwd())}")
            except Exception as e:
                print(f"  ⚠ 清空失败 {exp_results_dir}: {e}")
    
    # 删除统一输出目录的所有 PNG 文件
    if unified_output_dir.exists():
        try:
            for png_file in unified_output_dir.glob("*.png"):
                png_file.unlink()
                deleted_count += 1
            print(f"  ✓ 清空：{unified_output_dir.relative_to(Path.cwd())}")
        except Exception as e:
            print(f"  ⚠ 清空失败 {unified_output_dir}: {e}")
    
    # 清空 results 根目录下的所有 PNG 文件 (包括 all_figures 等子目录)
    if results_root.exists():
        try:
            # 递归查找并删除所有 PNG 文件
            for png_file in results_root.rglob("*.png"):
                png_file.unlink()
                deleted_count += 1
            print(f"  ✓ 清空：{results_root.relative_to(Path.cwd())} 及其子目录")
        except Exception as e:
            print(f"  ⚠ 清空失败 {results_root}: {e}")
    
    # 删除旧的实验报告 (保留最新的 3 个)
    if report_dir.exists():
        try:
            report_files = sorted(report_dir.glob("experiment_report_*.txt"))
            if len(report_files) > 3:
                # 删除最旧的报告
                for old_report in report_files[:-3]:
                    old_report.unlink()
                    deleted_count += 1
                print(f"  ✓ 清理旧报告：{len(report_files) - 3} 个")
        except Exception as e:
            print(f"  ⚠ 清理报告失败：{e}")
    
    print(f"\n✅ 已删除 {deleted_count} 个旧文件")


def collect_all_figures():
    """收集所有生成的图片到统一目录"""
    print("\n" + "="*70)
    print("📂 收集所有可视化图片")
    print("="*70)
    
    # 运行收集脚本
    try:
        from abm_simulation.experiments.collect_all_png_final import project_root
        from pathlib import Path
        import shutil
        
        output_dir = Path.cwd() / "results" / "all_experiments_figures"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 实验目录列表
        experiments_dirs = [
            Path.cwd() / "experiments" / "baseline_exp1",
            Path.cwd() / "experiments" / "experiment2_memory",
            Path.cwd() / "experiments" / "exp3_ai_evolution",
            Path.cwd() / "experiments" / "exp4_information_intervention",
            Path.cwd() / "experiments" / "exp5_network_structure",
            Path.cwd() / "experiments" / "exp6_generational_dynamics",
            Path.cwd() / "experiments" / "exp7_ai_competition",
            Path.cwd() / "experiments" / "exp8_context_sensitivity",
            Path.cwd() / "experiments" / "exp9_filter_bubble",
            Path.cwd() / "experiments" / "exp10_systemic_risk",
        ]
        
        total_count = 0
        
        for exp_dir in experiments_dirs:
            exp_folder = exp_dir.name
            exp_results_dir = exp_dir / "results"
            
            if not exp_results_dir.exists():
                continue
            
            # 递归查找所有 PNG 文件
            png_files = list(exp_results_dir.rglob("*.png"))
            
            for png_file in png_files:
                relative_path = png_file.relative_to(exp_results_dir)
                
                # 构建文件名
                if str(relative_path.parent) == '.':
                    new_filename = f"{exp_folder}_{png_file.name}"
                else:
                    subdir_name = relative_path.parent.name
                    new_filename = f"{exp_folder}_{subdir_name}_{png_file.name}"
                
                dest_path = output_dir / new_filename
                shutil.copy2(png_file, dest_path)
                print(f"  ✓ {new_filename}")
                total_count += 1
        
        print(f"\n✅ 已收集 {total_count} 张图片到：{output_dir}")
        
    except Exception as e:
        print(f"\n❌ 收集图片失败：{e}")


def generate_report(config, success_exps, failed_exps):
    """生成实验报告"""
    print("\n" + "="*70)
    print("📄 生成实验报告")
    print("="*70)
    
    report_dir = Path.cwd() / "results"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"experiment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("ABM 仿真实验报告\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("⚙️  实验配置\n")
        f.write("-"*70 + "\n")
        f.write(json.dumps(config, indent=2, ensure_ascii=False))
        f.write("\n\n")
        
        f.write("✅ 成功完成的实验\n")
        f.write("-"*70 + "\n")
        for exp in success_exps:
            f.write(f"  - 实验 {exp}\n")
        
        if failed_exps:
            f.write("\n❌ 失败的实验\n")
            f.write("-"*70 + "\n")
            for exp in failed_exps:
                f.write(f"  - 实验 {exp}\n")
        
        f.write("\n📊 可视化结果目录\n")
        f.write("-"*70 + "\n")
        f.write(f"  {Path.cwd() / 'results' / 'all_experiments_figures'}\n")
    
    print(f"\n✅ 实验报告已保存到：{report_path}")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🚀 ABM 仿真实验 - 批量运行工具")
    print("="*70)
    
    # 打印配置
    print_config(CONFIG)
    
    # 验证配置
    if not validate_config(CONFIG):
        print("\n❌ 配置验证失败，程序终止")
        return
    
    # 清空旧结果
    clear_old_results()
    
    # 询问是否继续
    print("\n是否按此配置运行所有实验？(y/n): ", end='')
    try:
        response = input().strip().lower()
        if response != 'y' and response != '':
            print("\n❌ 已取消运行")
            return
    except:
        pass
    
    # 运行实验
    success_exps = []
    failed_exps = []
    
    for exp_num in CONFIG['experiments_to_run']:
        success = run_experiment(exp_num, CONFIG)
        if success:
            success_exps.append(exp_num)
        else:
            failed_exps.append(exp_num)
    
    # 收集图片
    if CONFIG['generate_visualizations']:
        collect_all_figures()
    
    # 生成报告
    if CONFIG['save_results']:
        generate_report(CONFIG, success_exps, failed_exps)
    
    # 总结
    print("\n" + "="*70)
    print("🎉 所有实验运行完成!")
    print("="*70)
    print(f"\n✅ 成功：{len(success_exps)} 个实验 ({success_exps})")
    if failed_exps:
        print(f"❌ 失败：{len(failed_exps)} 个实验 ({failed_exps})")
    
    print(f"\n📂 结果查看:")
    print(f"   可视化图片：{Path.cwd() / 'results' / 'all_experiments_figures'}")
    print(f"   实验报告：{Path.cwd() / 'results' / '*.txt'}")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
