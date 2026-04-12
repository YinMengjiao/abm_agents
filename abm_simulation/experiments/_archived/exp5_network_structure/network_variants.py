"""
实验5: 异质性社交网络结构
不同网络拓扑对依赖扩散的影响
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Optional
from enum import Enum


class NetworkTopology(Enum):
    """网络拓扑类型"""
    SMALL_WORLD = "small_world"          # 小世界网络（基线）
    SCALE_FREE = "scale_free"            # 无标度网络
    COMMUNITY = "community"              # 社区结构网络
    RANDOM = "random"                    # 随机网络
    REGULAR = "regular"                  # 规则网络
    STAR = "star"                        # 星型网络（意见领袖）


class NetworkGenerator:
    """
    网络生成器
    
    生成不同类型的社交网络用于对比实验
    """
    
    def __init__(self, n_nodes: int = 500):
        """
        初始化网络生成器
        
        Args:
            n_nodes: 节点数量
        """
        self.n_nodes = n_nodes
    
    def generate(self, topology: NetworkTopology, **kwargs) -> nx.Graph:
        """
        生成指定类型的网络
        
        Args:
            topology: 网络拓扑类型
            **kwargs: 网络特定参数
            
        Returns:
            NetworkX图对象
        """
        generators = {
            NetworkTopology.SMALL_WORLD: self._generate_small_world,
            NetworkTopology.SCALE_FREE: self._generate_scale_free,
            NetworkTopology.COMMUNITY: self._generate_community,
            NetworkTopology.RANDOM: self._generate_random,
            NetworkTopology.REGULAR: self._generate_regular,
            NetworkTopology.STAR: self._generate_star,
        }
        
        generator = generators.get(topology, self._generate_small_world)
        return generator(**kwargs)
    
    def _generate_small_world(self, k: int = 6, p: float = 0.3) -> nx.Graph:
        """
        生成小世界网络
        
        Args:
            k: 最近邻连接数
            p: 重连概率
        """
        return nx.watts_strogatz_graph(self.n_nodes, k, p)
    
    def _generate_scale_free(self, m: int = 3) -> nx.Graph:
        """
        生成无标度网络（Barabási-Albert模型）
        
        Args:
            m: 每个新节点连接的边数
        """
        return nx.barabasi_albert_graph(self.n_nodes, m)
    
    def _generate_community(self, n_communities: int = 5, p_in: float = 0.3, p_out: float = 0.05) -> nx.Graph:
        """
        生成社区结构网络（随机块模型）
        
        Args:
            n_communities: 社区数量
            p_in: 社区内连接概率
            p_out: 社区间连接概率
        """
        sizes = [self.n_nodes // n_communities] * n_communities
        # 调整最后一个社区大小以确保总和正确
        sizes[-1] += self.n_nodes - sum(sizes)
        
        # 创建概率矩阵
        probs = np.full((n_communities, n_communities), p_out)
        np.fill_diagonal(probs, p_in)
        
        return nx.stochastic_block_model(sizes, probs)
    
    def _generate_random(self, p: float = 0.02) -> nx.Graph:
        """
        生成随机网络（Erdős-Rényi模型）
        
        Args:
            p: 连接概率
        """
        return nx.erdos_renyi_graph(self.n_nodes, p)
    
    def _generate_regular(self, k: int = 6) -> nx.Graph:
        """
        生成规则网络（每个节点有k个邻居）
        
        Args:
            k: 每个节点的邻居数
        """
        return nx.random_regular_graph(k, self.n_nodes)
    
    def _generate_star(self, n_hubs: int = 5) -> nx.Graph:
        """
        生成星型/多中心网络（意见领袖结构）
        
        Args:
            n_hubs: 中心节点数量
        """
        G = nx.Graph()
        G.add_nodes_from(range(self.n_nodes))
        
        # 选择中心节点
        hubs = np.random.choice(self.n_nodes, n_hubs, replace=False)
        
        # 每个非中心节点连接到随机中心
        for node in range(self.n_nodes):
            if node not in hubs:
                hub = np.random.choice(hubs)
                G.add_edge(node, hub)
        
        # 中心节点之间互相连接
        for i in range(len(hubs)):
            for j in range(i+1, len(hubs)):
                G.add_edge(hubs[i], hubs[j])
        
        return G


class NetworkMetricsAnalyzer:
    """网络指标分析器"""
    
    @staticmethod
    def analyze(G: nx.Graph) -> Dict:
        """
        分析网络拓扑指标
        
        Args:
            G: NetworkX图对象
            
        Returns:
            指标字典
        """
        metrics = {}
        
        # 基本指标
        metrics['n_nodes'] = G.number_of_nodes()
        metrics['n_edges'] = G.number_of_edges()
        metrics['density'] = nx.density(G)
        
        # 连通性
        if nx.is_connected(G):
            metrics['avg_path_length'] = nx.average_shortest_path_length(G)
            metrics['diameter'] = nx.diameter(G)
        else:
            # 使用最大连通分量
            largest_cc = max(nx.connected_components(G), key=len)
            subgraph = G.subgraph(largest_cc)
            metrics['avg_path_length'] = nx.average_shortest_path_length(subgraph)
            metrics['diameter'] = nx.diameter(subgraph)
        
        # 聚类系数
        metrics['avg_clustering'] = nx.average_clustering(G)
        metrics['transitivity'] = nx.transitivity(G)
        
        # 度分布指标
        degrees = [d for n, d in G.degree()]
        metrics['avg_degree'] = np.mean(degrees)
        metrics['degree_std'] = np.std(degrees)
        metrics['max_degree'] = max(degrees)
        metrics['min_degree'] = min(degrees)
        
        # 中心性指标
        try:
            betweenness = nx.betweenness_centrality(G)
            metrics['avg_betweenness'] = np.mean(list(betweenness.values()))
            metrics['max_betweenness'] = max(betweenness.values())
        except:
            metrics['avg_betweenness'] = 0
            metrics['max_betweenness'] = 0
        
        try:
            eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
            metrics['avg_eigenvector'] = np.mean(list(eigenvector.values()))
        except:
            metrics['avg_eigenvector'] = 0
        
        # 社区结构（使用Louvain算法）
        try:
            import community as community_louvain
            partition = community_louvain.best_partition(G)
            metrics['n_communities'] = len(set(partition.values()))
            metrics['modularity'] = community_louvain.modularity(partition, G)
        except:
            metrics['n_communities'] = 1
            metrics['modularity'] = 0
        
        return metrics
    
    @staticmethod
    def compare_networks(networks: Dict[str, nx.Graph]) -> Dict:
        """
        对比多个网络的指标
        
        Args:
            networks: {名称: 网络} 字典
            
        Returns:
            对比结果
        """
        comparison = {}
        
        for name, G in networks.items():
            comparison[name] = NetworkMetricsAnalyzer.analyze(G)
        
        return comparison


class TopologyImpactAnalyzer:
    """拓扑影响分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.results = {}
    
    def record_simulation_result(self, 
                                 topology: NetworkTopology,
                                 metrics: Dict):
        """
        记录仿真结果
        
        Args:
            topology: 网络拓扑类型
            metrics: 仿真指标
        """
        self.results[topology.value] = metrics
    
    def analyze_critical_coupling(self) -> Dict:
        """
        分析不同拓扑的临界耦合强度
        
        Returns:
            临界耦合分析结果
        """
        analysis = {}
        
        for topo_name, metrics in self.results.items():
            # 计算相变相关指标
            mag_trend = metrics.get('magnetization_trend', {})
            
            analysis[topo_name] = {
                'final_magnetization': mag_trend.get('final', 0),
                'magnetization_change': mag_trend.get('change', 0),
                'convergence_speed': self._estimate_convergence_speed(metrics),
            }
        
        return analysis
    
    def _estimate_convergence_speed(self, metrics: Dict) -> float:
        """估计收敛速度"""
        # 基于满意度或磁化强度的变化率估计
        sat_trend = metrics.get('satisfaction_trend', {})
        if sat_trend:
            return abs(sat_trend.get('change', 0)) / max(1, sat_trend.get('duration', 1))
        return 0
    
    def get_topology_ranking(self, metric: str = 'satisfaction') -> List[Tuple[str, float]]:
        """
        获取拓扑排名
        
        Args:
            metric: 排名指标
            
        Returns:
            [(拓扑名, 指标值), ...] 按指标值排序
        """
        rankings = []
        
        for topo_name, metrics in self.results.items():
            if metric == 'satisfaction':
                value = metrics.get('satisfaction', {}).get('mean', 0)
            elif metric == 'ai_usage':
                value = metrics.get('ai_usage', 0)
            elif metric == 'convergence':
                value = -self._estimate_convergence_speed(metrics)  # 负号表示越快越好
            else:
                value = 0
            
            rankings.append((topo_name, value))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings
