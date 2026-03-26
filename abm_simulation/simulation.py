"""
ABM仿真主引擎
整合Ising-D-I-B模型的完整仿真系统
"""

import numpy as np
import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.ising_network import IsingSocialNetwork, AdaptiveIsingNetwork
from agents.consumer_dib import ConsumerAgentDIB, ConsumerTraits
from agents.ai_agent import AIAgentPopulation, AIAgent
from environment.market import MarketEnvironment, SimulationContext, ProductCategory


@dataclass
class SimulationConfig:
    """仿真配置"""
    # 规模参数
    n_consumers: int = 1000
    n_merchants: int = 20
    n_ai_agents: int = 3
    
    # 网络参数
    network_type: str = 'small_world'
    initial_coupling: float = 0.5
    initial_temperature: float = 1.0
    
    # 仿真参数
    n_steps: int = 500
    burn_in_steps: int = 50
    
    # 初始分布
    initial_level_distribution: Dict[int, float] = field(default_factory=lambda: {
        1: 0.10,  # L1: 10%
        2: 0.25,  # L2: 25%
        3: 0.30,  # L3: 30%
        4: 0.25,  # L4: 25%
        5: 0.10,  # L5: 10%
    })
    
    # 动态参数
    enable_adaptive_coupling: bool = True
    coupling_trend: float = 0.001  # 每步社会耦合增长
    shock_probability: float = 0.01  # 外部冲击概率


@dataclass
class SimulationMetrics:
    """仿真指标记录"""
    step: int = 0
    
    # 依赖等级分布
    level_distribution: Dict[int, int] = field(default_factory=dict)
    magnetization: float = 0.0
    
    # 系统指标
    avg_satisfaction: float = 0.0
    avg_decision_time: float = 0.0
    ai_usage_rate: float = 0.0
    error_rate: float = 0.0
    
    # Ising指标
    coupling_strength: float = 0.0
    temperature: float = 0.0
    susceptibility: float = 0.0
    
    # AI指标
    ai_error_rate: float = 0.0
    ai_satisfaction_impact: float = 0.0


class ABMSimulation:
    """
    ABM仿真主类
    
    整合Ising社交网络、D-I-B消费者、AI代理和市场环境
    """
    
    def __init__(self, config: Optional[SimulationConfig] = None):
        """初始化仿真"""
        self.config = config or SimulationConfig()
        
        # 初始化组件
        self.network: Optional[AdaptiveIsingNetwork] = None
        self.consumers: List[ConsumerAgentDIB] = []
        self.ai_population: Optional[AIAgentPopulation] = None
        self.market: Optional[MarketEnvironment] = None
        self.context: Optional[SimulationContext] = None
        
        # 历史记录
        self.metrics_history: List[SimulationMetrics] = []
        self.step_count = 0
        
        # 是否已初始化
        self._initialized = False
    
    def initialize(self):
        """初始化仿真组件"""
        print("初始化仿真...")
        
        # 1. 创建Ising社交网络
        self.network = AdaptiveIsingNetwork(
            n_agents=self.config.n_consumers,
            network_type=self.config.network_type,
            coupling_strength=self.config.initial_coupling,
            temperature=self.config.initial_temperature
        )
        
        # 2. 初始化自旋（依赖等级）
        levels = self._sample_initial_levels()
        self.network.initialize_spins(levels)
        
        # 3. 设置外场（个体倾向）
        external_fields = self._generate_external_fields()
        self.network.set_external_fields(external_fields)
        
        # 4. 创建消费者智能体
        self.consumers = []
        for i in range(self.config.n_consumers):
            traits = ConsumerTraits(
                tech_acceptance=np.random.beta(2, 2),
                trust_tendency=np.random.beta(2, 2),
                privacy_concern=np.random.beta(2, 2),
                control_need=np.random.beta(2, 2),
                cognitive_laziness=np.random.beta(2, 2),
                social_conformity=np.random.beta(2, 2),
                risk_aversion=np.random.beta(2, 2),
            )
            
            consumer = ConsumerAgentDIB(
                agent_id=i,
                initial_level=levels[i],
                traits=traits
            )
            self.consumers.append(consumer)
        
        # 5. 创建AI代理群体
        self.ai_population = AIAgentPopulation(n_agents=self.config.n_ai_agents)
        
        # 6. 创建市场环境
        self.market = MarketEnvironment(
            n_merchants=self.config.n_merchants,
            market_condition='normal'
        )
        
        # 7. 创建仿真上下文
        self.context = SimulationContext()
        
        self._initialized = True
        print(f"初始化完成: {self.config.n_consumers}消费者, {self.config.n_merchants}商家, {self.config.n_ai_agents}AI代理")
        
        # 记录初始状态
        self._record_metrics()
    
    def _sample_initial_levels(self) -> List[int]:
        """根据分布采样初始依赖等级"""
        levels = []
        dist = self.config.initial_level_distribution
        for level, prob in dist.items():
            n = int(prob * self.config.n_consumers)
            levels.extend([level] * n)
        
        # 补齐或截断
        while len(levels) < self.config.n_consumers:
            levels.append(3)
        levels = levels[:self.config.n_consumers]
        
        np.random.shuffle(levels)
        return levels
    
    def _generate_external_fields(self) -> np.ndarray:
        """生成外场（个体固有倾向）"""
        # 基于技术接受度等特质生成
        fields = np.random.normal(0, 0.2, self.config.n_consumers)
        return fields
    
    def step(self) -> SimulationMetrics:
        """
        执行单步仿真
        
        流程：
        1. Ising网络更新（社会影响）
        2. 消费者D-I-B决策
        3. AI代理交互
        4. 市场交易
        5. 反馈与更新
        """
        if not self._initialized:
            raise RuntimeError("仿真未初始化，请先调用initialize()")
        
        self.step_count += 1
        self.context.step = self.step_count
        
        # 1. Ising网络更新（社会影响传播）
        self._update_ising_network()
        
        # 2. 消费者决策循环
        for i, consumer in enumerate(self.consumers):
            self._consumer_decision_cycle(consumer, i)
        
        # 3. 更新环境
        self.context.advance_time(hours=0.5)
        
        # 4. 动态调整系统参数
        if self.config.enable_adaptive_coupling:
            self._update_system_parameters()
        
        # 5. 记录指标
        metrics = self._record_metrics()
        
        return metrics
    
    def _update_ising_network(self):
        """更新Ising网络"""
        # Monte Carlo更新
        self.network.monte_carlo_step(update_type='random')
        
        # 同步到消费者
        for i, consumer in enumerate(self.consumers):
            new_spin = self.network.spins[i]
            if new_spin != consumer.spin:
                social_field = self.network.calculate_local_field(i)
                consumer.update_from_ising(new_spin, social_field, self.network.T)
    
    def _consumer_decision_cycle(self, consumer: ConsumerAgentDIB, agent_idx: int):
        """
        消费者D-I-B决策循环
        """
        # 获取上下文
        context = self.context.get_consumer_context(consumer.id)
        
        # 添加社交影响
        neighbor_spins = self.network.get_neighbor_levels(agent_idx)
        avg_neighbor_level = np.mean(neighbor_spins) if neighbor_spins else 3
        context['social_influence'] = (avg_neighbor_level - 3) / 2  # 归一化到[-1, 1]
        
        # D层：欲望形成
        desire = consumer.desire_formation(context)
        
        # I层：意图形成
        intention = consumer.intention_formation(desire, context)
        
        # 获取AI推荐
        ai_recommendation = None
        if intention.use_ai_probability > 0.5:
            ai_agent = self.ai_population.select_agent_for_consumer(consumer.id)
            available = self.market.get_available_options(n_options=20)
            ai_recommendation = ai_agent.make_recommendation(
                consumer.id, desire, available, consumer.dependency_level
            )
        
        # B层：行为执行
        alternatives = self.market.get_available_options(n_options=20)
        behavior = consumer.behavior_execution(intention, ai_recommendation, alternatives)
        
        # 市场交易
        if behavior.actual_choice:
            outcome = self.market.simulate_transaction(
                behavior.actual_choice,
                behavior.ai_involvement_level > 0,
                consumer.dependency_level
            )
            
            # 评估结果
            consumer.evaluate_outcome(outcome)
            
            # 记录经验
            consumer.record_experience(self.step_count, context)
            
            # AI学习更新
            if behavior.ai_involvement_level > 0 and ai_recommendation:
                ai_agent = self.ai_population.select_agent_for_consumer(consumer.id)
                ai_agent.update_from_interaction(consumer.id, {
                    'satisfaction': consumer.behavior.satisfaction,
                    'preferences': desire.__dict__,
                })
    
    def _update_system_parameters(self):
        """动态更新系统参数"""
        # 缓慢增加社会耦合（模拟AI技术扩散）
        shock = 0
        if np.random.random() < self.config.shock_probability:
            shock = np.random.normal(0, 0.1)
        
        self.network.update_parameters(
            J_trend=self.config.coupling_trend,
            shock_magnitude=shock
        )
    
    def _record_metrics(self) -> SimulationMetrics:
        """记录当前指标"""
        metrics = SimulationMetrics(step=self.step_count)
        
        # 依赖等级分布
        metrics.level_distribution = self.network.get_level_distribution()
        metrics.magnetization = self.network.get_magnetization()
        
        # 消费者统计
        satisfactions = [c.behavior.satisfaction for c in self.consumers]
        decision_times = [c.behavior.decision_time for c in self.consumers]
        ai_usage = [c.ai_usage_count for c in self.consumers]
        errors = [c.error_count for c in self.consumers]
        total_decisions = sum(c.total_decisions for c in self.consumers)
        
        metrics.avg_satisfaction = np.mean(satisfactions) if satisfactions else 0
        metrics.avg_decision_time = np.mean(decision_times) if decision_times else 0
        metrics.ai_usage_rate = sum(ai_usage) / max(1, total_decisions)
        metrics.error_rate = sum(errors) / max(1, total_decisions)
        
        # Ising指标
        metrics.coupling_strength = self.network.J
        metrics.temperature = self.network.T
        metrics.susceptibility = self.network.calculate_susceptibility()
        
        # AI指标
        ai_metrics = self.ai_population.get_collective_metrics()
        metrics.ai_error_rate = ai_metrics['collective_error_rate']
        
        self.metrics_history.append(metrics)
        return metrics
    
    def run(self, n_steps: Optional[int] = None) -> List[SimulationMetrics]:
        """
        运行完整仿真
        
        Args:
            n_steps: 仿真步数，None则使用配置值
        
        Returns:
            指标历史
        """
        if not self._initialized:
            self.initialize()
        
        steps = n_steps or self.config.n_steps
        
        print(f"\n开始仿真: {steps}步")
        print("-" * 50)
        
        for i in range(steps):
            self.step()
            
            # 进度输出
            if (i + 1) % 50 == 0:
                metrics = self.metrics_history[-1]
                print(f"Step {i+1}/{steps}: "
                      f"M={metrics.magnetization:.3f}, "
                      f"Sat={metrics.avg_satisfaction:.3f}, "
                      f"AI_use={metrics.ai_usage_rate:.3f}")
        
        print("-" * 50)
        print("仿真完成!")
        
        return self.metrics_history
    
    def get_summary_statistics(self) -> Dict:
        """获取汇总统计"""
        if not self.metrics_history:
            return {}
        
        final_metrics = self.metrics_history[-1]
        
        # 演化趋势
        magnetizations = [m.magnetization for m in self.metrics_history]
        satisfaction_trend = [m.avg_satisfaction for m in self.metrics_history]
        
        return {
            'final_level_distribution': final_metrics.level_distribution,
            'final_magnetization': final_metrics.magnetization,
            'magnetization_trend': {
                'initial': magnetizations[0],
                'final': magnetizations[-1],
                'change': magnetizations[-1] - magnetizations[0],
            },
            'satisfaction': {
                'mean': np.mean(satisfaction_trend),
                'final': satisfaction_trend[-1],
            },
            'ai_usage': final_metrics.ai_usage_rate,
            'error_rate': final_metrics.error_rate,
            'network_metrics': self.network.get_network_metrics() if self.network else {},
        }


def run_simulation_example():
    """运行示例仿真"""
    config = SimulationConfig(
        n_consumers=500,  # 小规模测试
        n_steps=200,
        initial_coupling=0.3,
        enable_adaptive_coupling=True,
        coupling_trend=0.002,
    )
    
    sim = ABMSimulation(config)
    sim.run()
    
    # 输出结果
    summary = sim.get_summary_statistics()
    print("\n=== 仿真结果汇总 ===")
    print(f"最终依赖等级分布: {summary['final_level_distribution']}")
    print(f"磁化强度变化: {summary['magnetization_trend']['initial']:.3f} -> {summary['magnetization_trend']['final']:.3f}")
    print(f"平均满意度: {summary['satisfaction']['mean']:.3f}")
    print(f"AI使用率: {summary['ai_usage']:.3f}")
    print(f"错误率: {summary['error_rate']:.3f}")
    
    return sim


if __name__ == "__main__":
    sim = run_simulation_example()
