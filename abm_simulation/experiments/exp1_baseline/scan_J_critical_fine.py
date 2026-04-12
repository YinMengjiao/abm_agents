"""
细网格J扫描:在0.40-0.50区间用ΔJ=0.01精确定位J_c
同时计算磁化率χ和Binder累积量U
"""

import sys
import os
import numpy as np

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from models.ising_network import AdaptiveIsingNetwork
from config import RESULTS


def fine_scan_J_critical():
    """
    细网格扫描:0.40-0.50,ΔJ=0.01,20次独立运行
    
    计算:
    1. |M|(J) - 平均磁化强度
    2. χ(J) = N·(⟨M²⟩ - ⟨M⟩²)/T - 磁化率
    3. U(J) = 1 - ⟨M⁴⟩/(3⟨M²⟩²) - Binder累积量
    """
    print("="*70)
    print("细网格J扫描:精确定位临界点 (0.40-0.50, ΔJ=0.01)")
    print("="*70)
    
    # 扫描参数
    # 用 linspace 代替 arange，避免浮点累积导致最后一个点（0.50）被漏掉
    J_values = np.linspace(0.40, 0.50, 11)
    n_agents = 500
    temperature = 2.0
    n_runs = 20  # 20次独立运行
    thermalization_steps = 500
    measurement_steps = 200
    
    print(f"\n网络规模: N = {n_agents}")
    print(f"温度: T = {temperature}")
    print(f"独立运行次数: {n_runs}")
    print(f"J范围: [{J_values[0]:.2f}, {J_values[-1]:.2f}], {len(J_values)}个点")
    print(f"热化: {thermalization_steps}步, 测量: {measurement_steps}步")
    print("="*70)
    
    # 存储所有J点的统计量
    all_M = []  # 每个J点的M列表
    all_M2 = []  # M²
    all_M4 = []  # M⁴
    
    for i, J in enumerate(J_values):
        M_runs = []
        
        for run in range(n_runs):
            # 设置随机种子
            np.random.seed(run * 1000 + int(J * 100))
            
            # 创建网络
            network = AdaptiveIsingNetwork(
                n_agents=n_agents,
                network_type='small_world',
                coupling_strength=J,
                temperature=temperature
            )
            
            # 初始化
            network.initialize_spins()
            external_fields = np.random.normal(0, 0.5, n_agents)
            network.set_external_fields(external_fields)
            
            # 热化
            for step in range(thermalization_steps):
                network.monte_carlo_step(update_type='random')
            
            # 测量
            M_samples = []
            for step in range(measurement_steps):
                network.monte_carlo_step(update_type='random')
                M_samples.append(network.get_magnetization())
            
            M_runs.append(np.mean(M_samples))
        
        # 计算统计量
        M_array = np.array(M_runs)
        all_M.append(M_array)
        all_M2.append(M_array**2)
        all_M4.append(M_array**4)
        
        # 进度
        avg_M = np.mean(np.abs(M_array))
        std_M = np.std(np.abs(M_array))
        if (i + 1) % 2 == 0:
            print(f"J = {J:.2f}: ⟨|M|⟩ = {avg_M:.4f} ± {std_M:.4f}")
    
    # 转换为数组
    all_M = np.array(all_M)
    all_M2 = np.array(all_M2)
    all_M4 = np.array(all_M4)
    
    # 计算统计量
    avg_abs_M = np.mean(np.abs(all_M), axis=1)
    std_abs_M = np.std(np.abs(all_M), axis=1)
    
    # 磁化率 χ = N·(⟨M²⟩ - ⟨M⟩²)/T
    avg_M2 = np.mean(all_M2, axis=1)
    avg_M_squared = np.mean(all_M, axis=1)**2
    chi = n_agents * (avg_M2 - avg_M_squared) / temperature
    
    # Binder累积量 U = 1 - ⟨M⁴⟩/(3⟨M²⟩²)
    avg_M4 = np.mean(all_M4, axis=1)
    U = 1 - avg_M4 / (3 * avg_M2**2)
    
    # 定位J_c:χ最大值
    J_c_from_chi = J_values[np.argmax(chi)]
    chi_max = np.max(chi)
    
    # 定位J_c:d|M|/dJ最大值
    dM_dJ = np.gradient(avg_abs_M, J_values)
    J_c_from_dM = J_values[np.argmax(dM_dJ)]
    
    # 定位J_c:U的拐点(最小值附近)
    J_c_from_U = J_values[np.argmin(U)]
    
    print("\n" + "="*70)
    print("细网格扫描结果汇总")
    print("="*70)
    
    print(f"\n{'J':<8} {'⟨|M|⟩':<10} {'std':<10} {'χ':<10} {'U':<10}")
    print("-" * 55)
    for i, J in enumerate(J_values):
        print(f"{J:<8.2f} {avg_abs_M[i]:<10.4f} {std_abs_M[i]:<10.4f} "
              f"{chi[i]:<10.2f} {U[i]:<10.4f}")
    
    print("\n" + "="*70)
    print("临界点分析 (三种方法)")
    print("="*70)
    print(f"\n方法1: 磁化率χ最大值 → J_c = {J_c_from_chi:.2f}, χ_max = {chi_max:.2f}")
    print(f"方法2: d⟨|M|⟩/dJ最大值 → J_c = {J_c_from_dM:.2f}")
    print(f"方法3: Binder累积量拐点 → J_c ≈ {J_c_from_U:.2f}")
    print(f"\n综合估计: J_c ≈ {(J_c_from_chi + J_c_from_dM + J_c_from_U)/3:.2f} (N={n_agents})")
    print(f"理论预期: σ_M ≈ 1/√N = {1/np.sqrt(n_agents):.4f}")
    print(f"实测无序相 σ_M (J=0.20) = {std_abs_M[0]:.4f}")
    
    # 保存数据
    output_data = {
        'J_values': J_values,
        'avg_abs_M': avg_abs_M,
        'std_abs_M': std_abs_M,
        'chi': chi,
        'U': U,
        'dM_dJ': dM_dJ,
        'J_c_from_chi': J_c_from_chi,
        'J_c_from_dM': J_c_from_dM,
        'J_c_from_U': J_c_from_U,
        'n_agents': n_agents,
        'n_runs': n_runs
    }
    
    print("\n" + "="*70)
    print("细网格扫描完成!")
    print("="*70)
    
    return output_data


def plot_fine_scan(data):
    """绘制细网格扫描结果"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from visualization.chinese_font import setup_chinese_font
        setup_chinese_font()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        J = data['J_values']
        
        # 左上图: ⟨|M|⟩(J)
        ax1.errorbar(J, data['avg_abs_M'], yerr=data['std_abs_M'], 
                    fmt='o-', capsize=4, markersize=5, linewidth=1.5, alpha=0.8)
        ax1.set_xlabel('耦合强度 J', fontsize=12)
        ax1.set_ylabel('平均磁化强度 ⟨|M|⟩', fontsize=12)
        ax1.set_title('磁化强度 vs 耦合强度 (20次独立运行)', fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        # 右上图: χ(J)
        ax2.plot(J, data['chi'], 's-', markersize=5, linewidth=1.5, 
                alpha=0.8, color='darkorange')
        ax2.axvline(x=data['J_c_from_chi'], color='red', linestyle='--', 
                   linewidth=2, alpha=0.7, label=f"J_c^χ = {data['J_c_from_chi']:.2f}")
        ax2.set_xlabel('耦合强度 J', fontsize=12)
        ax2.set_ylabel('磁化率 χ', fontsize=12)
        ax2.set_title('磁化率峰值定位相变点', fontsize=14)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # 左下图: U(J) - Binder累积量
        ax3.plot(J, data['U'], '^-', markersize=5, linewidth=1.5, 
                alpha=0.8, color='purple')
        ax3.axvline(x=data['J_c_from_U'], color='red', linestyle='--', 
                   linewidth=2, alpha=0.7, label=f"J_c^U ≈ {data['J_c_from_U']:.2f}")
        ax3.set_xlabel('耦合强度 J', fontsize=12)
        ax3.set_ylabel('Binder累积量 U', fontsize=12)
        ax3.set_title('Binder累积量 (判断相变阶数)', fontsize=14)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)
        
        # 右下图: d⟨|M|⟩/dJ
        ax4.plot(J, data['dM_dJ'], 'd-', markersize=5, linewidth=1.5, 
                alpha=0.8, color='teal')
        ax4.axvline(x=data['J_c_from_dM'], color='red', linestyle='--', 
                   linewidth=2, alpha=0.7, label=f"J_c^dM = {data['J_c_from_dM']:.2f}")
        ax4.set_xlabel('耦合强度 J', fontsize=12)
        ax4.set_ylabel('d⟨|M|⟩/dJ', fontsize=12)
        ax4.set_title('磁化强度变化率', fontsize=14)
        ax4.legend(fontsize=10)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_dir = RESULTS["baseline"]
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "J_scan_fine_critical.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n[OK] 细网格扫描图已保存: {output_path}")
        
        plt.close()
        
    except Exception as e:
        print(f"\n[警告] 绘图失败: {e}")


if __name__ == "__main__":
    data = fine_scan_J_critical()
    plot_fine_scan(data)
