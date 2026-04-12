"""
J扫描实验:测量修改版Ising模型的真实临界耦合强度
"""

import sys
import os
import numpy as np

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from models.ising_network import AdaptiveIsingNetwork
from config import RESULTS


def scan_J_critical():
    """
    扫描耦合强度J,测量稳态磁化强度,定位相变临界点
    
    方法:
    1. 固定其他参数,J从0.05到0.5取20个点
    2. 每个J值运行500步Monte Carlo达到稳态
    3. 再运行200步测量平均|M|
    4. 绘制|M|(J)曲线,从拐点读取J_c
    """
    print("="*70)
    print("J扫描实验:测量修改版Ising模型的真实临界点")
    print("="*70)
    
    # 扫描参数
    J_values = np.linspace(0.05, 0.50, 20)
    n_agents = 500
    temperature = 2.0  # 与基准实验一致
    thermalization_steps = 500  # 热化步数
    measurement_steps = 200  # 测量步数
    
    results = []
    
    print(f"\n网络规模: {n_agents} 智能体")
    print(f"温度: T = {temperature}")
    print(f"热化步数: {thermalization_steps}")
    print(f"测量步数: {measurement_steps}")
    print(f"J扫描范围: [{J_values[0]:.2f}, {J_values[-1]:.2f}], {len(J_values)}个点")
    print("="*70)
    
    for i, J in enumerate(J_values):
        # 创建网络
        network = AdaptiveIsingNetwork(
            n_agents=n_agents,
            network_type='small_world',
            coupling_strength=J,
            temperature=temperature
        )
        
        # 初始化自旋(随机)
        network.initialize_spins()
        
        # 设置外场(与基准实验一致)
        external_fields = np.random.normal(0, 0.5, n_agents)
        network.set_external_fields(external_fields)
        
        # 热化阶段:达到稳态
        for step in range(thermalization_steps):
            network.monte_carlo_step(update_type='random')
        
        # 测量阶段:收集磁化强度
        magnetizations = []
        for step in range(measurement_steps):
            network.monte_carlo_step(update_type='random')
            magnetizations.append(abs(network.get_magnetization()))
        
        avg_M = np.mean(magnetizations)
        std_M = np.std(magnetizations)
        
        results.append({
            'J': J,
            'avg_M': avg_M,
            'std_M': std_M,
            'final_spin_distribution': network.get_level_distribution()
        })
        
        # 进度输出
        if (i + 1) % 5 == 0:
            print(f"J = {J:.2f}: |M| = {avg_M:.4f} ± {std_M:.4f}")
    
    # 分析结果
    print("\n" + "="*70)
    print("扫描结果汇总")
    print("="*70)
    
    print(f"\n{'J':<8} {'|M|':<10} {'std':<10} {'L1':<6} {'L2':<6} {'L3':<6} {'L4':<6} {'L5':<6}")
    print("-" * 65)
    
    for r in results:
        dist = r['final_spin_distribution']
        print(f"{r['J']:<8.2f} {r['avg_M']:<10.4f} {r['std_M']:<10.4f} "
              f"{dist.get(1, 0):<6} {dist.get(2, 0):<6} {dist.get(3, 0):<6} "
              f"{dist.get(4, 0):<6} {dist.get(5, 0):<6}")
    
    # 估算J_c: 寻找|M|增长最快的点(数值导数最大值)
    M_values = np.array([r['avg_M'] for r in results])
    J_vals = np.array([r['J'] for r in results])
    
    # 计算数值导数 d|M|/dJ
    dM_dJ = np.gradient(M_values, J_vals)
    
    # J_c对应导数最大的位置(相变点)
    critical_idx = np.argmax(dM_dJ)
    J_c_estimated = J_vals[critical_idx]
    M_at_Jc = M_values[critical_idx]
    
    print("\n" + "="*70)
    print("临界点分析")
    print("="*70)
    print(f"\n估算方法: 数值导数 d|M|/dJ 最大值")
    print(f"临界耦合强度 J_c ≈ {J_c_estimated:.3f}")
    print(f"J_c 处的 |M| = {M_at_Jc:.4f}")
    print(f"\n平均场近似 J_c^MF = 1/<k> ≈ {1.0/6:.4f} (假设<k>=6)")
    print(f"修正系数: {J_c_estimated / (1.0/6):.2f}")
    
    # 保存数据供后续绘图使用
    output_data = {
        'J_values': J_vals,
        'M_values': M_values,
        'M_stds': np.array([r['std_M'] for r in results]),
        'dM_dJ': dM_dJ,
        'J_c': J_c_estimated,
        'results': results
    }
    
    print("\n" + "="*70)
    print("J扫描实验完成!")
    print("="*70)
    
    return output_data


def plot_J_scan(data):
    """绘制J扫描结果"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from visualization.chinese_font import setup_chinese_font
        setup_chinese_font()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 左图: |M|(J) 曲线
        ax1.errorbar(data['J_values'], data['M_values'], 
                    yerr=data['M_stds'], fmt='o-', capsize=3, 
                    markersize=4, linewidth=1.5, alpha=0.8)
        ax1.axvline(x=data['J_c'], color='red', linestyle='--', 
                   linewidth=2, alpha=0.7, label=f"J_c = {data['J_c']:.3f}")
        ax1.axvline(x=1.0/6, color='gray', linestyle=':', 
                   linewidth=1.5, alpha=0.5, label=f"J_c^MF = {1.0/6:.3f}")
        ax1.set_xlabel('耦合强度 J', fontsize=12)
        ax1.set_ylabel('平均磁化强度 |M|', fontsize=12)
        ax1.set_title('磁化强度 vs 耦合强度', fontsize=14)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # 右图: d|M|/dJ 曲线
        ax2.plot(data['J_values'], data['dM_dJ'], 's-', 
                markersize=4, linewidth=1.5, alpha=0.8, color='darkorange')
        ax2.axvline(x=data['J_c'], color='red', linestyle='--', 
                   linewidth=2, alpha=0.7, label=f"J_c = {data['J_c']:.3f}")
        ax2.set_xlabel('耦合强度 J', fontsize=12)
        ax2.set_ylabel('d|M|/dJ', fontsize=12)
        ax2.set_title('磁化强度变化率 (定位相变点)', fontsize=14)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_dir = RESULTS["baseline"]
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "J_scan_critical.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n[OK] J扫描图已保存: {output_path}")
        
        plt.close()
        
    except Exception as e:
        print(f"\n[警告] 绘图失败: {e}")


if __name__ == "__main__":
    data = scan_J_critical()
    plot_J_scan(data)
