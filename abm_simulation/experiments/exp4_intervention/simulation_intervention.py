"""
实验4仿真引擎: 信息干预
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict, List
from dataclasses import dataclass, field

from simulation import ABMSimulation, SimulationConfig
from experiments.exp4_intervention.intervention import (
    InformationIntervention, InterventionType, InterventionPolicyOptimizer
)


@dataclass
class InterventionMetrics:
    """干预实验特有指标"""
    step: int
    active_interventions: int = 0
    consumers_affected: int = 0
    level_changes_count: int = 0
    intervention_impact_score: float = 0.0


class InterventionSimulation(ABMSimulation):
    """
    实验4: 信息干预仿真
    
    研究外部信息冲击对系统演化的影响
    """
    
    def __init__(self, 
                 config: SimulationConfig,
                 intervention_schedule: List = None,
                 policy_type: str = 'balanced'):
        """
        初始化干预仿真
        
        Args:
            config: 仿真配置
            intervention_schedule: 自定义干预时间表
            policy_type: 政策类型 ('balanced', 'promote_ai', 'protect_consumers', 'custom')
        """
        super().__init__(config)
        
        # 初始化干预系统
        self.intervention_system = InformationIntervention()
        self.intervention_metrics_history: List[InterventionMetrics] = []
        self.policy_type = policy_type
        
        # 设置干预时间表
        if intervention_schedule:
            for event in intervention_schedule:
                self.intervention_system.schedule_intervention(
                    event.intervention_type,
                    event.timing,
                    event.intensity,
                    event.duration,
                    event.target_group
                )
        else:
            # 使用预设策略
            self._setup_default_interventions(policy_type, config.n_steps)
    
    def _setup_default_interventions(self, policy_type: str, n_steps: int):
        """设置默认干预"""
        optimizer = InterventionPolicyOptimizer()
        schedule = optimizer.generate_optimal_schedule(n_steps, policy_type)
        
        for event in schedule:
            self.intervention_system.schedule_intervention(
                event.intervention_type,
                event.timing,
                event.intensity,
                event.duration,
                event.target_group
            )
    
    def run_step(self) -> Dict:
        """运行单步仿真（包含干预）"""
        # 1. 应用干预
        intervention_effects = self.intervention_system.apply_intervention(
            self.current_step, self.consumers, self.network
        )
        
        # 2. 标准Ising步骤
        self.network.monte_carlo_step(self.current_step)
        
        # 3. 更新消费者依赖等级
        for consumer in self.consumers:
            new_spin = self.network.get_node_spin(consumer.id)
            new_level = self.network.spin_to_level(new_spin)
            consumer.update_dependency_level(new_level)
        
        # 4. 收集指标
        self._collect_intervention_metrics(intervention_effects)
        
        self.current_step += 1
        return intervention_effects
    
    def _collect_intervention_metrics(self, effects: Dict):
        """收集干预指标"""
        metric = InterventionMetrics(
            step=self.current_step,
            active_interventions=len(self.intervention_system.active_interventions),
            consumers_affected=effects.get('consumers_affected', 0),
            level_changes_count=len(effects.get('level_changes', [])),
            intervention_impact_score=self._calculate_impact_score(effects)
        )
        self.intervention_metrics_history.append(metric)
    
    def _calculate_impact_score(self, effects: Dict) -> float:
        """计算干预影响分数"""
        if not effects.get('level_changes'):
            return 0.0
        
        # 计算等级变化的平均幅度
        total_change = sum(abs(new - old) for _, old, new in effects['level_changes'])
        return total_change / max(1, len(effects['level_changes']))
    
    def get_intervention_summary(self) -> Dict:
        """获取干预实验汇总"""
        intervention_summary = self.intervention_system.get_intervention_summary()
        
        # 计算干预效果
        pre_intervention_levels = []
        post_intervention_levels = []
        
        for event in self.intervention_system.intervention_history:
            # 获取干预前后的依赖等级分布
            pre_step = max(0, event.timing - 1)
            post_step = min(len(self.metrics_history) - 1, event.timing + event.duration)
            
            if pre_step < len(self.metrics_history) and post_step < len(self.metrics_history):
                pre_dist = self.metrics_history[pre_step].level_distribution
                post_dist = self.metrics_history[post_step].level_distribution
                
                # 计算高依赖比例变化
                pre_high = sum(pre_dist.get(l, 0) for l in [4, 5])
                post_high = sum(post_dist.get(l, 0) for l in [4, 5])
                
                pre_intervention_levels.append(pre_high)
                post_intervention_levels.append(post_high)
        
        avg_impact = 0
        if pre_intervention_levels and post_intervention_levels:
            changes = [post - pre for pre, post in zip(pre_intervention_levels, post_intervention_levels)]
            avg_impact = np.mean(changes) if changes else 0
        
        return {
            'intervention_summary': intervention_summary,
            'policy_type': self.policy_type,
            'avg_impact_on_high_dependency': avg_impact,
            'total_level_changes': sum(m.level_changes_count for m in self.intervention_metrics_history),
            'peak_intervention_impact': max((m.intervention_impact_score for m in self.intervention_metrics_history), default=0)
        }
    
    def get_summary_statistics(self) -> Dict:
        """获取完整统计"""
        base_summary = super().get_summary_statistics()
        intervention_summary = self.get_intervention_summary()
        
        return {**base_summary, **intervention_summary}
