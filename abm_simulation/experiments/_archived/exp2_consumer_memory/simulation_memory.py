"""
实验2：带有记忆机制的ABM仿真
"""

import numpy as np
import sys
import os
from typing import Dict

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import ABMSimulation, SimulationConfig, SimulationMetrics
from experiments.exp2_consumer_memory.consumer_with_memory import ConsumerAgentWithMemory
from agents.consumer_dib import ConsumerTraits
from models.ising_network import AdaptiveIsingNetwork
from agents.ai_agent import AIAgentPopulation
from environment.market import MarketEnvironment, SimulationContext


class Experiment2Simulation(ABMSimulation):
    """
    实验2：记忆增强版仿真
    
    使用ConsumerAgentWithMemory替代基线的ConsumerAgentDIB
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        self.memory_statistics_history = []
    
    def initialize(self):
        """初始化仿真（使用带记忆的消费者）"""
        print("初始化实验2（记忆增强版）...")
        
        # 1. 创建Ising社交网络
        self.network = AdaptiveIsingNetwork(
            n_agents=self.config.n_consumers,
            network_type=self.config.network_type,
            coupling_strength=self.config.initial_coupling,
            temperature=self.config.initial_temperature
        )
        
        # 2. 初始化自旋
        levels = self._sample_initial_levels()
        self.network.initialize_spins(levels)
        
        # 3. 设置外场
        external_fields = self._generate_external_fields()
        self.network.set_external_fields(external_fields)
        
        # 4. 创建带记忆的消费者智能体
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
            
            consumer = ConsumerAgentWithMemory(
                agent_id=i,
                initial_level=levels[i],
                traits=traits,
                memory_capacity=50,
                memory_decay_rate=0.95
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
        print(f"初始化完成: {self.config.n_consumers}消费者(带记忆), {self.config.n_merchants}商家, {self.config.n_ai_agents}AI代理")
        
        self._record_metrics()
    
    def _consumer_decision_cycle(self, consumer, agent_idx):
        """消费者决策循环（记忆增强版）"""
        # 获取上下文
        context = self.context.get_consumer_context(consumer.id)
        
        # 添加社交影响
        neighbor_spins = self.network.get_neighbor_levels(agent_idx)
        avg_neighbor_level = np.mean(neighbor_spins) if neighbor_spins else 3
        context['social_influence'] = (avg_neighbor_level - 3) / 2
        
        # D层：欲望形成（记忆影响）
        desire = consumer.desire_formation(context)
        
        # I层：意图形成（记忆影响）
        intention = consumer.intention_formation(desire, context)
        
        # 获取AI推荐
        ai_recommendation = None
        if intention.use_ai_probability > 0.5:
            ai_agent = self.ai_population.select_agent_for_consumer(consumer.id)
            available = self.market.get_available_options(n_options=20)
            ai_recommendation = ai_agent.make_recommendation(
                consumer.id, desire, available, consumer.dependency_level
            )
        
        # B层：行为执行（记忆影响）
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
            
            # 存储经验到记忆（实验2核心）
            consumer.store_experience(self.step_count, context)
            
            # AI学习更新
            if behavior.ai_involvement_level > 0 and ai_recommendation:
                ai_agent = self.ai_population.select_agent_for_consumer(consumer.id)
                ai_agent.update_from_interaction(consumer.id, {
                    'satisfaction': consumer.behavior.satisfaction,
                    'preferences': desire.__dict__,
                })
    
    def _record_metrics(self):
        """记录指标（增加记忆统计）"""
        metrics = super()._record_metrics()
        
        # 记录记忆统计
        if self.consumers:
            memory_stats = [c.get_memory_statistics() for c in self.consumers]
            avg_dynamic_trust = np.mean([s['dynamic_trust'] for s in memory_stats])
            avg_consecutive_errors = np.mean([s['consecutive_errors'] for s in memory_stats])
            
            self.memory_statistics_history.append({
                'step': self.step_count,
                'avg_dynamic_trust': avg_dynamic_trust,
                'avg_consecutive_errors': avg_consecutive_errors,
            })
        
        return metrics
    
    def get_experiment_summary(self) -> Dict:
        """获取实验2特有汇总"""
        summary = self.get_summary_statistics()
        
        # 记忆相关统计
        if self.memory_statistics_history:
            final_memory = self.memory_statistics_history[-1]
            summary['memory_dynamics'] = {
                'final_avg_dynamic_trust': final_memory['avg_dynamic_trust'],
                'final_avg_consecutive_errors': final_memory['avg_consecutive_errors'],
                'trust_trend': [m['avg_dynamic_trust'] for m in self.memory_statistics_history],
            }
        
        return summary


def run_experiment2():
    """运行实验2"""
    from simulation import SimulationConfig
    
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
    )
    
    sim = Experiment2Simulation(config)
    sim.run()
    
    # 输出结果
    summary = sim.get_experiment_summary()
    print("\n=== 实验2（记忆增强版）结果汇总 ===")
    print(f"最终依赖等级分布: {summary['final_level_distribution']}")
    print(f"磁化强度变化: {summary['magnetization_trend']['initial']:.3f} -> {summary['magnetization_trend']['final']:.3f}")
    print(f"平均满意度: {summary['satisfaction']['mean']:.3f}")
    print(f"AI使用率: {summary['ai_usage']:.3f}")
    print(f"错误率: {summary['error_rate']:.3f}")
    
    if 'memory_dynamics' in summary:
        print(f"\n【记忆动态】")
        print(f"  平均动态信任: {summary['memory_dynamics']['final_avg_dynamic_trust']:.3f}")
        print(f"  平均连续错误: {summary['memory_dynamics']['final_avg_consecutive_errors']:.2f}")
    
    return sim


if __name__ == "__main__":
    sim = run_experiment2()
