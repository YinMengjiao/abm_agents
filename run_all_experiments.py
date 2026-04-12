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
    'level_distribution': { #问卷结果
        1: 0.04,  # L1: 自主型 (10%)
        2: 0.26,  # L2: 信息辅助 (25%)
        3: 0.46,  # L3: 半委托 (30%)
        4: 0.21,  # L4: 高度依赖 (25%)
        5: 0.03,  # L5: 完全代理 (10%)
    },
    
    # ========== 实验控制 ==========
    'experiments_to_run': [1, 2, 3, 4],  # 要运行的实验编号 (1=基线, 2=机制, 3=后果, 4=干预)
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
    valid_exps = set(range(1, 5))
    requested_exps = set(config['experiments_to_run'])
    invalid = requested_exps - valid_exps
    if invalid:
        print(f"\n❌ 错误：无效的实验编号：{invalid}")
        print("有效的实验编号为 1-4 (1=基线, 2=机制, 3=后果, 4=干预)")
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
            # 基准动态
            from experiments.exp1_baseline.run_baseline import run_baseline
            sim, summary = run_baseline()

        elif exp_num == 2:
            # 扩散机制: AI进化
            from experiments.exp2_mechanism.run_evolution import run_experiment3 as run_exp2
            sim, summary = run_exp2()

        elif exp_num == 3:
            # 系统后果: 过滤气泡 + 系统性风险
            from experiments.exp3_consequences.filter_bubble.run_filter_bubble import run_experiment9 as run_bubble
            from experiments.exp3_consequences.systemic_risk.run_systemic_risk import run_experiment10 as run_risk
            analyzer, bubble_results = run_bubble()
            risk_model, main_result, stress_results = run_risk()

        elif exp_num == 4:
            # 政策干预
            from experiments.exp4_intervention.run_intervention import run_experiment4
            results = run_experiment4()
        
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
    
    # 统一输出目录 (主要存储位置)
    unified_output_dir = Path.cwd() / "results" / "all_experiments_figures"
    
    # results 根目录
    results_root = Path.cwd() / "results"
    
    # 实验报告目录
    report_dir = Path.cwd() / "results"
    
    deleted_count = 0
    
    # 清空统一输出目录的所有 PNG 文件
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
    """收集所有生成的图片到统一目录 (已在运行时直接保存)"""
    print("\n" + "="*70)
    print("📂 检查可视化图片")
    print("="*70)
    
    output_dir = Path.cwd() / "results" / "all_experiments_figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 统计图片数量
    png_files = list(output_dir.glob("*.png"))
    
    if png_files:
        print(f"\n✅ 已生成 {len(png_files)} 张图片:")
        for file in sorted(png_files):
            size_kb = file.stat().st_size / 1024
            print(f"   ✓ {file.name} ({size_kb:.1f} KB)")
    else:
        print(f"\n⚠️ 未找到图片文件")
    
    print(f"\n📂 图片目录：{output_dir}")


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
