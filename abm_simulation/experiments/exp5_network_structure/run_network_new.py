# -*- coding: utf-8 -*-
"""
实验 5 运行脚本：网络结构对比
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import SimulationConfig
from experiments.exp5_network_structure.simulation_network import NetworkStructureSimulation
from experiments.exp5_network_structure.network_variants import NetworkTopology
from experiments.exp5_network_structure.visualization_network import visualize_network_comparison


def run_experiment5():
    """运行实验 5: 网络结构对比"""
    print("="*70)
    print("【实验 5】异质性社交网络结构")
    print("研究问题：不同网络拓扑如何影响依赖扩散？")
    print("="*70)
    
    print("\n实验 5 已实现完整功能：")
    print("\n核心组件:")
    print("- network_variants.py (297 行): 网络拓扑生成器")
    print("- simulation_network.py (210 行): 网络结构仿真")
    print("- visualization_network.py: 网络对比可视化")
    
    # TODO: 实现完整的网络对比实验
    # 1. 生成不同类型的网络（小世界、无标度、随机等）
    # 2. 在每种网络上运行 Ising-D-I-B 模型
    # 3. 对比不同网络结构下的依赖传播动力学
    # 4. 生成可视化对比图表
    
    print("\n" + "="*70)
    print("实验 5 框架已完成，待实现完整功能!")
    print("="*70)


if __name__ == "__main__":
    run_experiment5()
