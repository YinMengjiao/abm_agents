"""
Ising模型社交邻居网络
基于统计物理的自旋模型模拟社会影响
"""

import numpy as np
import networkx as nx
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class SpinConfig:
    """自旋配置"""
    level_map: Dict[int, int] = None  # 依赖等级到自旋的映射
    
    def __post_init__(self):
        if self.level_map is None:
            # L1(自主) → -2, L2 → -1, L3 → 0, L4 → +1, L5(代理) → +2
            self.level_map = {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}
    
    def level_to_spin(self, level: int) -> int:
        return self.level_map.get(level, 0)
    
    def spin_to_level(self, spin: int) -> int:
        reverse_map = {v: k for k, v in self.level_map.items()}
        # 限制在有效范围内
        spin = max(-2, min(2, spin))
        return reverse_map.get(spin, 3)


class IsingSocialNetwork:
    """
    Ising模型社交邻居网络
    
    将消费者的AI依赖等级建模为自旋状态
    邻居之间的社会影响通过自旋相互作用实现
    """
    
    def __init__(self, 
                 n_agents: int = 1000,
                 network_type: str = 'small_world',
                 coupling_strength: float = 0.5,
                 external_field: float = 0.0,
                 temperature: float = 1.0):
        """
        初始化Ising社交网络
        
        Args:
            n_agents: 智能体数量
            network_type: 网络类型 ('small_world', 'scale_free', 'random', 'lattice')
            coupling_strength: 耦合强度J (社会影响强度)
            external_field: 外场h (系统性偏向)
            temperature: 温度T (决策随机性)
        """
        self.n_agents = n_agents
        self.network_type = network_type
        self.J = coupling_strength
        self.h = external_field
        self.T = temperature
        
        self.spin_config = SpinConfig()
        
        # 生成网络
        self.graph = self._generate_network()
        self.adjacency = nx.to_numpy_array(self.graph)
        
        # 初始化自旋状态
        self.spins = np.zeros(n_agents, dtype=int)
        self.external_fields = np.zeros(n_agents)
        
        # 历史记录
        self.spin_history = []
        self.magnetization_history = []
        
    def _generate_network(self) -> nx.Graph:
        """生成社交网络拓扑"""
        if self.network_type == 'small_world':
            # Watts-Strogatz小世界网络：高聚类+短路径
            k = 6  # 每个节点的邻居数
            p = 0.3  # 重连概率
            return nx.watts_strogatz_graph(self.n_agents, k, p)
        
        elif self.network_type == 'scale_free':
            # Barabási-Albert无标度网络：少数意见领袖
            m = 3  # 每个新节点连接的边数
            return nx.barabasi_albert_graph(self.n_agents, m)
        
        elif self.network_type == 'random':
            # Erdős-Rényi随机网络
            p = 0.01
            return nx.erdos_renyi_graph(self.n_agents, p)
        
        elif self.network_type == 'lattice':
            # 二维格子网络
            side = int(np.sqrt(self.n_agents))
            return nx.grid_2d_graph(side, side)
        
        else:
            raise ValueError(f"Unknown network type: {self.network_type}")
    
    def initialize_spins(self, initial_levels: Optional[List[int]] = None):
        """
        初始化自旋状态
        
        Args:
            initial_levels: 初始依赖等级列表，None则随机初始化
        """
        if initial_levels is None:
            # 随机初始化，偏向中间等级
            levels = np.random.choice([1, 2, 3, 4, 5], 
                                     size=self.n_agents,
                                     p=[0.1, 0.25, 0.3, 0.25, 0.1])
        else:
            levels = np.array(initial_levels)
        
        self.spins = np.array([self.spin_config.level_to_spin(l) for l in levels])
        self.spin_history.append(self.spins.copy())
        self.magnetization_history.append(self.get_magnetization())
    
    def set_external_fields(self, fields: np.ndarray):
        """
        设置外场（个体固有倾向）
        
        Args:
            fields: 每个智能体的外场值数组
        """
        self.external_fields = fields[:self.n_agents]
    
    def calculate_local_field(self, i: int) -> float:
        """
        计算节点i的局部场（邻居影响+外场）
        
        H_i = J * Σ_j(s_j) + h_i
        
        Returns:
            局部场值
        """
        # 邻居自旋和
        neighbor_sum = np.sum(self.adjacency[i] * self.spins)
        
        # 局部场
        local_field = self.J * neighbor_sum + self.external_fields[i] + self.h
        
        return local_field
    
    def glauber_flip_probability(self, i: int) -> float:
        """
        Glauber动力学：计算自旋翻转概率
        
        P(s_i → -s_i) = 1 / (1 + exp(ΔE / T))
        其中 ΔE = 2 * s_i * H_i
        
        Returns:
            翻转概率
        """
        local_field = self.calculate_local_field(i)
        delta_E = 2 * self.spins[i] * local_field
        
        # 避免数值溢出
        if delta_E > 10:
            return 0.0
        elif delta_E < -10:
            return 1.0
        
        prob = 1.0 / (1.0 + np.exp(delta_E / self.T))
        return prob
    
    def monte_carlo_step(self, update_type: str = 'random') -> int:
        """
        执行一次Monte Carlo更新
        
        Args:
            update_type: 更新类型 ('random', 'sequential', 'checkerboard')
        
        Returns:
            实际翻转次数
        """
        n_flips = 0
        
        if update_type == 'random':
            # 随机顺序更新
            indices = np.random.permutation(self.n_agents)
        elif update_type == 'sequential':
            indices = range(self.n_agents)
        else:
            indices = range(self.n_agents)
        
        for i in indices:
            flip_prob = self.glauber_flip_probability(i)
            
            if np.random.random() < flip_prob:
                # 翻转自旋
                self.spins[i] = -self.spins[i]
                n_flips += 1
        
        # 记录历史
        self.spin_history.append(self.spins.copy())
        self.magnetization_history.append(self.get_magnetization())
        
        return n_flips
    
    def get_magnetization(self) -> float:
        """
        计算系统磁化强度（平均自旋）
        
        Returns:
            归一化磁化强度 [-1, 1]
        """
        return np.mean(self.spins) / 2.0  # 归一化到[-1, 1]
    
    def get_level_distribution(self) -> Dict[int, int]:
        """
        获取当前依赖等级分布
        
        Returns:
            等级计数字典
        """
        levels = [self.spin_config.spin_to_level(s) for s in self.spins]
        unique, counts = np.unique(levels, return_counts=True)
        return dict(zip(unique, counts))
    
    def get_neighbor_levels(self, i: int) -> List[int]:
        """获取邻居的依赖等级"""
        neighbors = list(self.graph.neighbors(i))
        return [self.spin_config.spin_to_level(self.spins[n]) for n in neighbors]
    
    def calculate_susceptibility(self) -> float:
        """
        计算磁化率（系统对外场的响应敏感度）
        
        χ = (<m²> - <m>²) / T
        """
        if len(self.magnetization_history) < 10:
            return 0.0
        
        recent_m = np.array(self.magnetization_history[-100:])
        return np.var(recent_m) / self.T
    
    def detect_phase_transition(self, J_values: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        扫描耦合强度，检测相变
        
        Args:
            J_values: 待扫描的耦合强度数组
        
        Returns:
            (J_values, magnetizations)
        """
        original_J = self.J
        magnetizations = []
        
        for J in J_values:
            self.J = J
            # 热化
            for _ in range(100):
                self.monte_carlo_step()
            # 测量
            mags = []
            for _ in range(50):
                self.monte_carlo_step()
                mags.append(abs(self.get_magnetization()))
            magnetizations.append(np.mean(mags))
        
        self.J = original_J
        return J_values, np.array(magnetizations)
    
    def get_network_metrics(self) -> Dict:
        """获取网络拓扑指标"""
        return {
            'n_nodes': self.n_agents,
            'n_edges': self.graph.number_of_edges(),
            'avg_clustering': nx.average_clustering(self.graph),
            'avg_path_length': nx.average_shortest_path_length(self.graph) 
                              if nx.is_connected(self.graph) else float('inf'),
            'degree_assortativity': nx.degree_assortativity_coefficient(self.graph),
        }


class AdaptiveIsingNetwork(IsingSocialNetwork):
    """
    适应性Ising网络
    耦合强度随时间动态变化（模拟AI技术扩散）
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.J_history = [self.J]
        self.T_history = [self.T]
    
    def update_parameters(self, 
                         J_trend: float = 0.0,
                         T_trend: float = 0.0,
                         shock_magnitude: float = 0.0):
        """
        动态更新系统参数
        
        Args:
            J_trend: 耦合强度变化趋势（技术扩散速度）
            T_trend: 温度变化趋势（社会环境稳定性）
            shock_magnitude: 外部冲击强度（如重大AI事件）
        """
        # 趋势项
        self.J = max(0.1, min(2.0, self.J + J_trend))
        self.T = max(0.1, min(2.0, self.T + T_trend))
        
        # 随机冲击
        if shock_magnitude > 0:
            self.J += np.random.normal(0, shock_magnitude)
            self.J = max(0.1, min(2.0, self.J))
        
        self.J_history.append(self.J)
        self.T_history.append(self.T)
    
    def get_critical_J(self) -> float:
        """
        估算临界耦合强度（平均场近似）
        
        对于小世界网络：Jc ≈ 1 / <k>
        """
        avg_degree = 2 * self.graph.number_of_edges() / self.n_agents
        return 1.0 / avg_degree if avg_degree > 0 else 0.5
