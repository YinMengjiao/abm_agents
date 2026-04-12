"""
实验2仿真引擎: AI进化机制
在基线（exp1）基础上，启用AI从消费者反馈中学习的能力
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict, List
from dataclasses import dataclass, field

from simulation import ABMSimulation, SimulationConfig
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
    实验2: AI进化仿真

    与基线（exp1）完全相同的 Ising-D-I-B 流程，唯一区别是
    AI 代理群体替换为 EvolvingAIPopulation，可以从消费者反馈
    中持续学习并提升能力。

    继承结构：
      run() → step() [本类覆盖] → super().step() + _collect_evolution_metrics()
    """

    def __init__(self, config: SimulationConfig, evolution_rate: float = 0.02):
        self.evolution_rate = evolution_rate
        self.evolution_metrics_history: List[EvolutionMetrics] = []

        # 父类初始化：建立 Ising 网络、消费者、普通 AI 群体
        super().__init__(config)

        # 用可进化 AI 群体替换父类建立的普通群体
        self.ai_population = EvolvingAIPopulation(
            n_agents=config.n_ai_agents,
            evolution_rate=evolution_rate
        )

    def step(self) -> Dict:
        """
        覆盖父类 step()：先执行完整标准流程，再追加进化指标收集

        父类 step() 已经包含：
          1. Ising Monte Carlo 更新 + 自旋同步到消费者
          2. 每位消费者的 D-I-B 决策循环（含 AI 推荐与 ai.update_from_interaction）
          3. 时间推进
          4. 自适应耦合参数更新
          5. 记录基础指标到 self.metrics_history
        """
        # 记录本步前各 AI 的学习事件数，用于统计本步新增学习量
        before_counts = [len(a.learning_history) for a in self.ai_population.agents]

        # 执行完整标准仿真步（Ising + D-I-B + 市场 + 指标）
        metrics = super().step()

        # 统计本步新增学习事件
        after_counts = [len(a.learning_history) for a in self.ai_population.agents]
        learning_events = sum(a - b for a, b in zip(after_counts, before_counts))

        # 收集进化专项指标
        self._collect_evolution_metrics(learning_events)

        return metrics

    def _collect_evolution_metrics(self, learning_events: int):
        """收集进化指标，追加到 evolution_metrics_history"""
        pop_metrics = self.ai_population.get_population_evolution_metrics()

        evolution_metric = EvolutionMetrics(
            step=self.step_count,
            avg_ai_error_rate=pop_metrics['avg_error_rate'],
            avg_evolution_progress=pop_metrics['avg_evolution_progress'],
            ai_accuracy_trajectory=[
                m['recommendation_accuracy'] for m in pop_metrics['agent_metrics']
            ],
            consumer_trust_recovery=self._calculate_trust_recovery(),
            learning_events_count=learning_events
        )

        self.evolution_metrics_history.append(evolution_metric)

    def _calculate_trust_recovery(self) -> float:
        """高依赖等级（L4-L5）消费者占比，作为信任恢复代理指标"""
        if not self.consumers:
            return 0.0
        high_dep = sum(1 for c in self.consumers if c.dependency_level >= 4)
        return high_dep / len(self.consumers)

    def get_evolution_summary(self) -> Dict:
        """获取进化实验汇总统计"""
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
                'total_learning_events': sum(
                    m.learning_events_count for m in self.evolution_metrics_history
                )
            },
            'ai_population_metrics': self.ai_population.get_population_evolution_metrics()
        }

    def get_summary_statistics(self) -> Dict:
        """获取完整统计（父类基础指标 + 进化专项指标）"""
        base_summary = super().get_summary_statistics()
        evolution_summary = self.get_evolution_summary()
        return {**base_summary, **evolution_summary}
