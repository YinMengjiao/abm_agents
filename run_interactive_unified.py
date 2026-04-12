"""
交互式运行 ABM 仿真 - 统一实验平台

使用方法:
    python run_interactive_unified.py
    
功能:
    1. 提供统一的实验选择界面
    2. 支持4个核心实验 (基线/机制/后果/干预)
    3. 每个实验支持自定义初始人群比例
    4. 输出结果汇总和可视化
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'abm_simulation'))

from simulation import ABMSimulation, SimulationConfig
try:
    from visualization.plots import quick_visualize
    has_viz = True
except ImportError:
    has_viz = False
    print("  可视化模块未找到，将跳过图表生成")

# 导入所有实验模块
EXPERIMENTS = {
    '1': {
        'name': 'exp1 基准动态 (Baseline)',
        'module': 'experiments.exp1_baseline.run_baseline',
        'description': '基础 Ising-D-I-B 模型，包含耦合、温度、外部冲击'
    },
    '2': {
        'name': 'exp2 扩散机制 (AI进化)',
        'module': 'experiments.exp2_mechanism.run_evolution',
        'description': 'AI 从反馈中学习改进，探索正反馈环与满意度变化'
    },
    '3': {
        'name': 'exp3 系统后果 (过滤气泡+系统性风险)',
        'module': 'experiments.exp3_consequences',
        'description': 'L4主导带来的信息茧房效应与临界脆弱性'
    },
    '4': {
        'name': 'exp4 政策干预 (信息干预)',
        'module': 'experiments.exp4_intervention.run_intervention',
        'description': '三种干预模式：推广 AI、保护消费者、平衡策略'
    },
}


def show_experiment_menu():
    """显示实验选择菜单"""
    print("\n" + "="*70)
    print("ABM 消费决策代理仿真实验平台")
    print("模型：Ising-D-I-B (Desire-Intention-Behavior)")
    print("="*70)
    print("\n请选择实验:")
    print("-"*70)
    
    for key, exp in EXPERIMENTS.items():
        print(f"  [{key:>2}] {exp['name']:<30} - {exp['description']}")
    
    print("-"*70)
    print("  [0] 退出程序")
    print("="*70)


def get_user_input_distribution() -> dict:
    """从用户输入获取初始人群比例分布"""
    print("\n" + "="*60)
    print("请输入初始人群依赖等级分布 (L1-L5)")
    print("="*60)
    print("\n说明:")
    print("  L1: 极低 AI 依赖群体 (自主决策)")
    print("  L2: 低 AI 依赖群体 (信息辅助)")
    print("  L3: 中等 AI 依赖群体 (半委托)")
    print("  L4: 高 AI 依赖群体 (高度依赖)")
    print("  L5: 极高 AI 依赖群体 (完全代理)")
    print("\n要求:")
    print("  1. 每个等级的比例用小数表示 (如 0.2 表示 20%)")
    print("  2. 所有比例之和必须等于 1.0")
    print("  3. 直接回车使用默认值")
    print("="*60)
    
    default_dist = {1: 0.10, 2: 0.25, 3: 0.30, 4: 0.25, 5: 0.10}
    
    try:
        print("\n默认分布:")
        for level, ratio in default_dist.items():
            print(f"  L{level}: {ratio*100:.0f}%")
        
        print("\n是否使用默认分布？(Y/n): ", end='')
        use_default = input().strip().lower()
        
        if use_default == '' or use_default == 'y':
            print("\n 使用默认分布")
            return default_dist
        
        print("\n请依次输入各等级比例:")
        user_dist = {}
        for level in range(1, 6):
            prompt = f"  L{level} 比例 (默认{default_dist[level]*100:.0f}%): "
            user_input = input(prompt).strip()
            
            if user_input == '':
                user_dist[level] = default_dist[level]
            else:
                user_dist[level] = float(user_input)
        
        total = sum(user_dist.values())
        print(f"\n输入汇总：总和 = {total:.4f}")
        
        if abs(total - 1.0) > 0.001:
            print(f"警告：比例之和 ({total:.4f}) 不等于 1.0")
            print("是否自动归一化？(Y/n): ", end='')
            normalize = input().strip().lower()
            
            if normalize == '' or normalize == 'y':
                user_dist = {k: v/total for k, v in user_dist.items()}
                print(f" 已归一化到总和为 1.0")
            else:
                print("  请重新调整比例后再次运行程序")
                return default_dist
        
        print("\n最终使用的分布:")
        for level, ratio in sorted(user_dist.items()):
            print(f"  L{level}: {ratio*100:.2f}%")
        
        return user_dist
        
    except KeyboardInterrupt:
        print("\n\n  用户中断，使用默认分布")
        return default_dist
    except Exception as e:
        print(f"\n  输入错误：{e}，使用默认分布")
        return default_dist


def run_custom_experiment(exp_key):
    """运行自定义配置的实验"""
    exp_info = EXPERIMENTS[exp_key]
    
    print(f"\n{'='*70}")
    print(f"【实验】{exp_info['name']}")
    print(f"{'='*70}")
    
    # 获取用户自定义分布
    dist = get_user_input_distribution()
    
    # 创建配置
    config = SimulationConfig(
        n_consumers=500,
        n_merchants=20,
        n_ai_agents=3,
        network_type='small_world',
        n_steps=300,
        initial_coupling=0.2,
        initial_temperature=2.0,
        enable_adaptive_coupling=True,
        coupling_trend=0.0005,
        shock_probability=0.05,
        initial_level_distribution=dist
    )
    
    print(f"\n当前配置:")
    print(f"   消费者数量：{config.n_consumers}")
    print(f"   商家数量：{config.n_merchants}")
    print(f"   AI 代理数量：{config.n_ai_agents}")
    print(f"   仿真步数：{config.n_steps}")
    print(f"   网络类型：{config.network_type}")
    print(f"   初始耦合强度：{config.initial_coupling}")
    print(f"   初始温度：{config.initial_temperature}")
    print()
    
    # 显示初始分布
    print("初始依赖等级分布:")
    level_names = {
        1: 'L1 自主',
        2: 'L2 信息辅助',
        3: 'L3 半委托',
        4: 'L4 高度依赖',
        5: 'L5 完全代理'
    }
    for level in range(1, 6):
        ratio = dist.get(level, 0)
        bar = '' * int(ratio * 20)
        print(f"  {level_names[level]:<12}: {ratio*100:5.1f}% {bar}")
    print()
    
    # 询问是否开始
    print("是否开始运行实验？(Y/n): ", end='')
    response = input().strip().lower()
    
    if response != '' and response != 'y':
        print("\n已取消实验运行")
        return
    
    print("\n 开始实验...\n")
    
    # 根据实验类型调用不同的模块
    try:
        if exp_key == '1':
            from experiments.exp1_baseline.run_baseline import run_baseline
            sim, summary = run_baseline()
        elif exp_key == '2':
            from experiments.exp2_mechanism.run_evolution import run_experiment3 as run_exp2
            sim, summary = run_exp2()
        elif exp_key == '3':
            from experiments.exp3_consequences.filter_bubble.run_filter_bubble import run_experiment9 as run_bubble
            from experiments.exp3_consequences.systemic_risk.run_systemic_risk import run_experiment10 as run_risk
            analyzer, bubble_results = run_bubble()
            risk_model, main_result, stress_results = run_risk()
            return
        elif exp_key == '4':
            from experiments.exp4_intervention.run_intervention import run_experiment4
            results = run_experiment4()
            return
            
        print("\n" + "="*70)
        print("✅ 实验完成!")
        print("="*70)
        
    except ImportError as e:
        print(f"\n  实验模块导入失败：{e}")
        print("请检查实验文件是否存在")
    except Exception as e:
        print(f"\n  实验运行出错：{e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    while True:
        show_experiment_menu()
        
        try:
            choice = input("\n请输入实验编号 (0-4): ").strip()

            if choice == '0':
                print("\n" + "="*70)
                print("感谢使用，再见！")
                print("="*70)
                break
            elif choice in EXPERIMENTS:
                run_custom_experiment(choice)
            else:
                print("\n  无效的实验编号，请输入 1-4")
                
        except KeyboardInterrupt:
            print("\n\n  用户中断")
            print("\n" + "="*70)
            print("程序结束")
            print("="*70)
            break
        except Exception as e:
            print(f"\n  发生错误：{e}")
            import traceback
            traceback.print_exc()
        
        # 询问是否继续
        if choice != '0':
            print("\n是否继续其他实验？(y/N): ", end='')
            cont = input().strip().lower()
            if cont != 'y' and cont != '':
                print("\n" + "="*70)
                print("感谢使用，再见！")
                print("="*70)
                break


if __name__ == "__main__":
    main()
