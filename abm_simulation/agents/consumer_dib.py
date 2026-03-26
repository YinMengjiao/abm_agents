"""
D-I-B模型消费者智能体
Desire-Intention-Behavior (欲望-意图-行为)
分层决策模型
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class DependencyLevel(Enum):
    """AI依赖等级"""
    AUTONOMOUS = 1      # L1: 完全自主型
    INFO_ASSISTED = 2   # L2: 信息辅助型
    SEMI_DELEGATED = 3  # L3: 半委托型
    HIGHLY_DEPENDENT = 4 # L4: 高度依赖型
    FULLY_DELEGATED = 5  # L5: 完全代理型


@dataclass
class ConsumerTraits:
    """消费者人格特质（长期稳定）"""
    tech_acceptance: float = 0.5      # 技术接受度
    trust_tendency: float = 0.5       # 信任倾向
    privacy_concern: float = 0.5      # 隐私关注
    control_need: float = 0.5         # 控制需求
    cognitive_laziness: float = 0.5   # 认知惰性
    social_conformity: float = 0.5    # 社会遵从性
    risk_aversion: float = 0.5        # 风险厌恶
    
    def __post_init__(self):
        for key in self.__dict__:
            value = getattr(self, key)
            setattr(self, key, max(0.0, min(1.0, value)))


@dataclass
class DesireState:
    """D层：欲望状态"""
    hunger: float = 0.0
    convenience_need: float = 0.0
    social_need: float = 0.0
    quality_pursuit: float = 0.0
    price_sensitivity: float = 0.0
    novelty_seeking: float = 0.0
    
    def normalize(self):
        values = np.array(list(self.__dict__.values()))
        total = np.sum(values)
        if total > 0:
            for key in self.__dict__:
                setattr(self, key, getattr(self, key) / total)


@dataclass
class IntentionState:
    """I层：意图状态"""
    use_ai_probability: float = 0.0
    search_depth: int = 0
    budget_limit: float = 100.0
    time_pressure: float = 0.0
    quality_threshold: float = 0.5
    risk_tolerance: float = 0.5
    perceived_benefit: float = 0.0
    perceived_risk: float = 0.0
    perceived_control: float = 0.0


@dataclass
class BehaviorOutcome:
    """B层：行为结果"""
    actual_choice: Any = None
    decision_time: float = 0.0
    ai_involvement_level: float = 0.0
    information_searched: int = 0
    alternatives_considered: int = 0
    satisfaction: float = 0.5
    regret: float = 0.0
    perceived_effort: float = 0.0
    actual_quality: float = 0.0
    actual_cost: float = 0.0
    error_occurred: bool = False
    error_type: Optional[str] = None


@dataclass
class Experience:
    """消费经验记录"""
    step: int = 0
    dependency_level: int = 3
    ai_involved: bool = False
    satisfaction: float = 0.5
    error_occurred: bool = False
    error_type: Optional[str] = None
    error_severity: str = 'none'
    context: Dict = field(default_factory=dict)


class ConsumerAgentDIB:
    """D-I-B模型消费者智能体"""
    
    def __init__(self, agent_id: int, initial_level: int = 3,
                 traits: Optional[ConsumerTraits] = None):
        self.id = agent_id
        self.dependency_level = initial_level
        self.spin = self._level_to_spin(initial_level)
        
        if traits is None:
            self.traits = ConsumerTraits(
                tech_acceptance=np.random.beta(2, 2),
                trust_tendency=np.random.beta(2, 2),
                privacy_concern=np.random.beta(2, 2),
                control_need=np.random.beta(2, 2),
                cognitive_laziness=np.random.beta(2, 2),
                social_conformity=np.random.beta(2, 2),
                risk_aversion=np.random.beta(2, 2),
            )
        else:
            self.traits = traits
        
        self.desire = DesireState()
        self.intention = IntentionState()
        self.behavior = BehaviorOutcome()
        
        self.experiences: List[Experience] = []
        self.dependency_trajectory = [initial_level]
        self.satisfaction_history = []
        self.current_context: Dict = {}
        
        self.total_decisions = 0
        self.ai_usage_count = 0
        self.error_count = 0
    
    def _level_to_spin(self, level: int) -> int:
        mapping = {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}
        return mapping.get(level, 0)
    
    def _spin_to_level(self, spin: int) -> int:
        spin = max(-2, min(2, spin))
        mapping = {-2: 1, -1: 2, 0: 3, 1: 4, 2: 5}
        return mapping[spin]
    
    def desire_formation(self, context: Dict) -> DesireState:
        """D层：欲望形成"""
        time_factor = context.get('time_since_last_meal', 0.5)
        self.desire.hunger = min(1.0, time_factor * 0.5 + np.random.normal(0, 0.05))
        
        base_convenience = self.traits.cognitive_laziness * 0.5
        social_boost = context.get('social_influence', 0) * self.traits.social_conformity
        self.desire.convenience_need = min(1.0, base_convenience + social_boost + np.random.normal(0, 0.05))
        
        self.desire.social_need = context.get('social_context', 0.3) * self.traits.social_conformity
        self.desire.quality_pursuit = self.traits.control_need * 0.5 + np.random.normal(0, 0.05)
        self.desire.price_sensitivity = 1 - self.traits.cognitive_laziness * 0.5
        self.desire.novelty_seeking = np.random.beta(2, 3)
        
        self.desire.normalize()
        return self.desire
    
    def intention_formation(self, desire: DesireState, context: Dict) -> IntentionState:
        """I层：意图形成"""
        base_intention = self.dependency_level / 5.0
        
        convenience_push = desire.convenience_need * self.traits.cognitive_laziness
        control_resistance = desire.quality_pursuit * self.traits.control_need * (1 - self.traits.trust_tendency)
        
        time_pressure = context.get('urgency', 0.5) * 0.3
        cognitive_relief = context.get('complexity', 0.5) * 0.2
        
        self.intention.use_ai_probability = np.clip(
            base_intention + convenience_push - control_resistance + time_pressure + cognitive_relief,
            0, 1
        )
        
        self.intention.search_depth = int((1 - self.intention.use_ai_probability) * 10)
        self.intention.budget_limit = context.get('budget', 100.0)
        self.intention.time_pressure = context.get('urgency', 0.5)
        
        self.intention.perceived_benefit = convenience_push + time_pressure
        self.intention.perceived_risk = (1 - self.traits.trust_tendency) * control_resistance
        self.intention.perceived_control = (1 - self.intention.use_ai_probability) * self.traits.control_need
        
        return self.intention
    
    def behavior_execution(self, intention: IntentionState, ai_recommendation: Optional[Any],
                          alternatives: List[Any]) -> BehaviorOutcome:
        """B层：行为执行"""
        intended_ai_use = intention.use_ai_probability
        actual_ai_use = np.random.random() < intended_ai_use
        
        if actual_ai_use and ai_recommendation is not None:
            self.behavior.ai_involvement_level = self.dependency_level / 5.0
            
            if self.dependency_level <= 2:
                choice = self._manual_override(ai_recommendation, alternatives)
                self.behavior.decision_time = np.random.exponential(5)
            elif self.dependency_level == 3:
                choice = self._rule_constrained_choice(ai_recommendation, intention)
                self.behavior.decision_time = np.random.exponential(2)
            else:
                choice = ai_recommendation
                self.behavior.decision_time = np.random.exponential(0.5)
        else:
            self.behavior.ai_involvement_level = 0
            choice = self._manual_search(alternatives, intention)
            self.behavior.decision_time = np.random.exponential(8)
        
        self.behavior.actual_choice = choice
        self.behavior.information_searched = intention.search_depth if not actual_ai_use else 1
        self.behavior.alternatives_considered = len(alternatives) if not actual_ai_use else 3
        
        self.total_decisions += 1
        if actual_ai_use:
            self.ai_usage_count += 1
        
        return self.behavior
    
    def _manual_override(self, recommendation, alternatives):
        if np.random.random() < 0.7:
            return recommendation
        return np.random.choice(alternatives) if alternatives else recommendation
    
    def _rule_constrained_choice(self, recommendation, intention):
        if np.random.random() < 0.8:
            return recommendation
        return None
    
    def _manual_search(self, alternatives, intention):
        n_to_consider = min(intention.search_depth, len(alternatives))
        if n_to_consider > 0:
            considered = np.random.choice(alternatives, n_to_consider, replace=False)
            return considered[0] if len(considered) > 0 else None
        return None
    
    def evaluate_outcome(self, outcome: Dict):
        """评估行为结果"""
        expected_quality = self.intention.quality_threshold
        actual_quality = outcome.get('quality', expected_quality)
        
        quality_gap = actual_quality - expected_quality
        effort = self.behavior.decision_time / 10.0
        
        self.behavior.satisfaction = np.clip(
            0.5 + quality_gap * 0.5 - effort * 0.2 + np.random.normal(0, 0.1),
            0, 1
        )
        
        self.behavior.regret = max(0, -quality_gap) * self.traits.risk_aversion
        self.behavior.perceived_effort = effort
        self.behavior.actual_quality = actual_quality
        self.behavior.actual_cost = outcome.get('cost', 0)
        self.behavior.error_occurred = outcome.get('error', False)
        self.behavior.error_type = outcome.get('error_type', None)
        
        if self.behavior.error_occurred:
            self.error_count += 1
        
        self.satisfaction_history.append(self.behavior.satisfaction)
    
    def record_experience(self, step: int, context: Dict):
        """记录消费经验"""
        exp = Experience(
            step=step,
            dependency_level=self.dependency_level,
            ai_involved=self.behavior.ai_involvement_level > 0,
            satisfaction=self.behavior.satisfaction,
            error_occurred=self.behavior.error_occurred,
            error_type=self.behavior.error_type,
            error_severity='high' if self.behavior.error_occurred and self.behavior.satisfaction < 0.3 else 'none',
            context=context
        )
        self.experiences.append(exp)
    
    def update_from_ising(self, new_spin: int, social_field: float, temperature: float):
        """基于Ising动力学更新依赖等级"""
        current_spin = self.spin
        
        if new_spin != current_spin:
            flip_energy = 2 * current_spin * social_field
            flip_prob = 1.0 / (1.0 + np.exp(flip_energy / temperature))
            
            if np.random.random() < flip_prob:
                self.spin = new_spin
                new_level = self._spin_to_level(new_spin)
                
                if new_level != self.dependency_level:
                    self.dependency_level = new_level
                    self.dependency_trajectory.append(new_level)
    
    def get_statistics(self) -> Dict:
        """获取智能体统计信息"""
        return {
            'agent_id': self.id,
            'current_level': self.dependency_level,
            'total_decisions': self.total_decisions,
            'ai_usage_rate': self.ai_usage_count / max(1, self.total_decisions),
            'error_rate': self.error_count / max(1, self.total_decisions),
            'avg_satisfaction': np.mean(self.satisfaction_history) if self.satisfaction_history else 0.5,
            'level_changes': len(self.dependency_trajectory) - 1,
        }
