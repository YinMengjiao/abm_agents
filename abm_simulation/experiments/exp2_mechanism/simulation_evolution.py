"""
实验3仿真引擎: AI进化机制
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from simulation import ABMSimulation, SimulationConfig
from agents.consumer_dib import ConsumerAgentDIB, ConsumerTraits
from environment.market import MarketEnvironment, Product
from experiments.exp2_mechanism.ai_evolution import EvolvingAIPopulation, AILearningMode


@dataclass
class EvolutionMetrics:
    """进化实验特有指标"""
    step: int
    avg_ai_error_rate: float = 0.0
    avg_evolution_progress: float = 0.0
    ai_accuracy_trajectory: List[float] = field(default_factory=list)
    consumer_trust_recovery: float = 0.0
    learning_events_count: int = 0


class EvolutionSimulation(ABMSimulation):
    """
    实验3: AI进化仿真
    
    研究AI从消费者反馈中学习改进的过程
    """
    
    def __init__(self, config: SimulationConfig, evolution_rate: float = 0.02):
        """
        初始化进化仿真
        
        Args:
            config: 仿真配置
            evolution_rate: AI进化速率
        """
        self.evolution_rate = evolution_rate
        self.evolution_metrics_history: List[EvolutionMetrics] = []
        
        # 先调用父类初始化（但会创建普通AI群体，需要覆盖）
        super().__init__(config)
        
        # 替换为可进化的AI群体
        self.ai_population = EvolvingAIPopulation(
            n_agents=config.n_ai_agents,
            evolution_rate=evolution_rate
        )
        
    def run_step(self) -> Dict:
        """运行单步仿真（包含AI学习）"""
        step_metrics = {
            'ai_learning_events': 0,
            'ai_evolution_progress': [],
            'consumer_ai_interactions': 0,
        }
        
        # 1. 消费者决策和AI交互
        for consumer in self.consumers:
            if consumer.dependency_level == 1:
                continue  # L1用户不使用AI
            
            # 选择最适合的AI代理
            ai_agent = self.ai_population.select_best_agent(consumer.id)
            
            # 获取可用商品
            available_products = self.market.get_available_products(10)
            
            # AI生成推荐
            recommendation = ai_agent.make_recommendation_with_evolution(
                consumer_id=consumer.id,
                available_options=available_products,
                dependency_level=consumer.dependency_level
            )
            
            if recommendation is None:
                continue
            
            step_metrics['consumer_ai_interactions'] += 1
            
            # 模拟消费者决策
            actual_choice = consumer.make_decision(
                desire_state={'products': available_products},
                intention_state={'candidates': recommendation['items']},
                ai_recommendation=recommendation
            )
            
            # 计算满意度
            satisfaction = self._calculate_satisfaction(
                consumer, actual_choice, recommendation
            )
            
            # 记录交互结果
            interaction_result = {
                'satisfaction': satisfaction,
                'error': recommendation.get('error', False),
                'error_type': recommendation.get('error_type', 'unknown'),
                'context': 'general',
                'chosen_product': actual_choice.id if hasattr(actual_choice, 'id') else None
            }
            
            # AI从反馈中学习
            learning_record = ai_agent.process_feedback(
                consumer_id=consumer.id,
                interaction_result=interaction_result,
                step=self.current_step
            )
            
            step_metrics['ai_learning_events'] += 1
            step_metrics['ai_evolution_progress'].append(ai_agent.evolution_progress)
        
        # 2. 标准Ising步骤（社会影响）
        self.network.monte_carlo_step(self.current_step)
        
        # 3. 更新消费者依赖等级
        for consumer in self.consumers:
            new_spin = self.network.get_node_spin(consumer.id)
            new_level = self.network.spin_to_level(new_spin)
            consumer.update_dependency_level(new_level)
        
        # 4. 收集指标
        self._collect_evolution_metrics(step_metrics)
        
        self.current_step += 1
        return step_metrics
    
    def _calculate_satisfaction(self, 
                               consumer: ConsumerAgentDIB,
                               actual_choice,
                               recommendation: Dict) -> float:
        """计算消费者满意度"""
        if recommendation.get('error', False):
            base_satisfaction = 0.3
        else:
            base_satisfaction = 0.7 + recommendation.get('quality', 0.5) * 0.3
        
        # 个性化调整
        if hasattr(consumer, 'traits'):
            base_satisfaction += (consumer.traits.satisfaction_sensitivity - 0.5) * 0.1
        
        return np.clip(base_satisfaction, 0, 1)
    
    def _collect_evolution_metrics(self, step_metrics: Dict):
        """收集进化指标"""
        pop_metrics = self.ai_population.get_population_evolution_metrics()
        
        # 计算消费者信任恢复度
        trust_recovery = self._calculate_trust_recovery()
        
        evolution_metric = EvolutionMetrics(
            step=self.current_step,
            avg_ai_error_rate=pop_metrics['avg_error_rate'],
            avg_evolution_progress=pop_metrics['avg_evolution_progress'],
            ai_accuracy_trajectory=[m['recommendation_accuracy'] for m in pop_metrics['agent_metrics']],
            consumer_trust_recovery=trust_recovery,
            learning_events_count=step_metrics['ai_learning_events']
        )
        
        self.evolution_metrics_history.append(evolution_metric)
    
    def _calculate_trust_recovery(self) -> float:
        """计算消费者信任恢复度"""
        if not self.consumers:
            return 0.0
        
        # 计算高依赖等级（L4-L5）消费者比例
        high_dependency = sum(1 for c in self.consumers if c.dependency_level >= 4)
        return high_dependency / len(self.consumers)
    
    def get_evolution_summary(self) -> Dict:
        """获取进化实验汇总"""
        if not self.evolution_metrics_history:
            return {}
        
        initial = self.evolution_metrics_history[0]
        final = self.evolution_metrics_history[-1]
        
        return {
            'evolution_summary': {
                'initial_error_rate': initial.avg_ai_error_rate,
                'final_error_rate': final.avg_ai_error_rate,
                'error_rate_reduction': initial.avg_ai_error_rate - final.avg_ai_error_rate,
                'initial_evolution_progress': initial.avg_evolution_progress,
                'final_evolution_progress': final.avg_evolution_progress,
                'trust_recovery': final.consumer_trust_recovery,
                'total_learning_events': sum(m.learning_events_count for m in self.evolution_metrics_history)
            },
            'ai_population_metrics': self.ai_population.get_population_evolution_metrics()
        }
    
    def get_summary_statistics(self) -> Dict:
        """获取完整统计（包含进化指标）"""
        base_summary = super().get_summary_statistics()
        evolution_summary = self.get_evolution_summary()
        
        return {**base_summary, **evolution_summary}
