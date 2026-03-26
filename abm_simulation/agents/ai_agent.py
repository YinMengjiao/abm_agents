"""
AI代理智能体
作为独立行动者参与消费决策
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class AIErrorType(Enum):
    """AI错误类型"""
    MISUNDERSTANDING = "misunderstanding"      # 误解用户需求
    OUTDATED_INFO = "outdated_info"            # 信息过时
    PREFERENCE_DRIFT = "preference_drift"      # 偏好漂移未识别
    CONTEXT_BLINDNESS = "context_blindness"    # 上下文盲区
    EXECUTION_ERROR = "execution_error"        # 执行错误
    FILTER_BUBBLE = "filter_bubble"            # 过滤气泡


@dataclass
class AIRecommendation:
    """AI推荐结果"""
    items: List[Any] = field(default_factory=list)
    confidence: float = 0.0
    explanation: str = ""
    error_probability: float = 0.0
    error_type: Optional[AIErrorType] = None
    personalization_score: float = 0.0


@dataclass
class ConsumerProfile:
    """消费者画像"""
    consumer_id: int
    preference_history: List[Dict] = field(default_factory=list)
    interaction_count: int = 0
    satisfaction_history: List[float] = field(default_factory=list)
    personalization_level: float = 0.0
    
    def update(self, interaction: Dict):
        self.interaction_count += 1
        self.preference_history.append(interaction.get('preferences', {}))
        self.satisfaction_history.append(interaction.get('satisfaction', 0.5))
        self.personalization_level = min(1.0, self.interaction_count / 20)


class AIAgent:
    """
    AI代理智能体
    
    作为独立行动者，具有不同能力等级和错误模式
    """
    
    def __init__(self, 
                 agent_id: int,
                 capacity_level: str = 'medium',
                 learning_rate: float = 0.1):
        """
        初始化AI代理
        
        Args:
            agent_id: 代理标识
            capacity_level: 能力等级 ('low', 'medium', 'high')
            learning_rate: 学习率
        """
        self.id = agent_id
        self.capacity_level = capacity_level
        self.learning_rate = learning_rate
        
        # 能力属性（根据等级初始化）
        self._init_capacity()
        
        # 消费者画像库
        self.consumer_profiles: Dict[int, ConsumerProfile] = {}
        
        # 经验缓冲区
        self.experience_buffer: List[Dict] = []
        
        # 错误统计
        self.error_count = 0
        self.total_recommendations = 0
        self.error_by_type: Dict[AIErrorType, int] = {t: 0 for t in AIErrorType}
        
        # 性能指标
        self.avg_satisfaction_impact = 0.5
    
    def _init_capacity(self):
        """根据能力等级初始化属性"""
        capacity_params = {
            'low': {
                'recommendation_accuracy': (0.5, 0.15),
                'understanding_depth': (0.4, 0.2),
                'execution_reliability': (0.7, 0.15),
                'adaptation_speed': (0.3, 0.1),
            },
            'medium': {
                'recommendation_accuracy': (0.75, 0.1),
                'understanding_depth': (0.7, 0.15),
                'execution_reliability': (0.85, 0.1),
                'adaptation_speed': (0.6, 0.1),
            },
            'high': {
                'recommendation_accuracy': (0.9, 0.05),
                'understanding_depth': (0.9, 0.08),
                'execution_reliability': (0.95, 0.05),
                'adaptation_speed': (0.85, 0.08),
            }
        }
        
        params = capacity_params.get(self.capacity_level, capacity_params['medium'])
        
        self.recommendation_accuracy = np.random.normal(*params['recommendation_accuracy'])
        self.understanding_depth = np.random.normal(*params['understanding_depth'])
        self.execution_reliability = np.random.normal(*params['execution_reliability'])
        self.adaptation_speed = np.random.normal(*params['adaptation_speed'])
        
        # 确保在有效范围内
        self.recommendation_accuracy = np.clip(self.recommendation_accuracy, 0, 1)
        self.understanding_depth = np.clip(self.understanding_depth, 0, 1)
        self.execution_reliability = np.clip(self.execution_reliability, 0, 1)
        self.adaptation_speed = np.clip(self.adaptation_speed, 0, 1)
        
        # 基础错误率
        self.base_error_rates = {
            AIErrorType.MISUNDERSTANDING: max(0, 0.2 - self.understanding_depth * 0.15),
            AIErrorType.OUTDATED_INFO: 0.05,
            AIErrorType.PREFERENCE_DRIFT: max(0, 0.15 - self.adaptation_speed * 0.1),
            AIErrorType.CONTEXT_BLINDNESS: max(0, 0.12 - self.understanding_depth * 0.08),
            AIErrorType.EXECUTION_ERROR: max(0, 0.1 - self.execution_reliability * 0.08),
            AIErrorType.FILTER_BUBBLE: 0.08,
        }
    
    def get_or_create_profile(self, consumer_id: int) -> ConsumerProfile:
        """获取或创建消费者画像"""
        if consumer_id not in self.consumer_profiles:
            self.consumer_profiles[consumer_id] = ConsumerProfile(consumer_id=consumer_id)
        return self.consumer_profiles[consumer_id]
    
    def make_recommendation(self, 
                           consumer_id: int,
                           desire_state: Any,
                           available_options: List[Any],
                           dependency_level: int) -> AIRecommendation:
        """
        为消费者生成推荐
        
        Args:
            consumer_id: 消费者ID
            desire_state: 消费者欲望状态
            available_options: 可用选项
            dependency_level: 消费者依赖等级
        
        Returns:
            AI推荐结果
        """
        self.total_recommendations += 1
        
        # 获取消费者画像
        profile = self.get_or_create_profile(consumer_id)
        
        # 根据依赖等级调整服务深度
        if dependency_level == 1:
            return None  # L1用户不使用AI
        
        # 计算个性化提升
        personalization_boost = profile.personalization_level * 0.2
        effective_accuracy = self.recommendation_accuracy + personalization_boost
        
        # 根据依赖等级计算错误概率
        error_prob = self._calculate_error_risk(dependency_level, profile)
        
        # 模拟推荐过程
        n_options = len(available_options)
        if n_options == 0:
            return AIRecommendation(
                items=[],
                confidence=0.0,
                error_probability=1.0,
                error_type=AIErrorType.MISUNDERSTANDING
            )
        
        # 选择推荐项（考虑准确性）
        n_recommendations = min(3, n_options)
        
        # 准确性影响选择质量
        if np.random.random() < effective_accuracy:
            # 高质量推荐
            recommended_indices = np.random.choice(n_options, n_recommendations, replace=False)
        else:
            # 次优推荐
            recommended_indices = np.random.choice(n_options, n_recommendations, replace=False)
        
        recommended_items = [available_options[i] for i in recommended_indices]
        
        # 确定是否出错
        error_occurred = np.random.random() < error_prob
        error_type = None
        
        if error_occurred:
            error_type = self._select_error_type()
            self.error_count += 1
            self.error_by_type[error_type] += 1
            
            # 错误影响推荐质量
            recommended_items = self._apply_error_effect(recommended_items, error_type)
        
        recommendation = AIRecommendation(
            items=recommended_items,
            confidence=effective_accuracy * (1 - error_prob),
            error_probability=error_prob,
            error_type=error_type if error_occurred else None,
            personalization_score=profile.personalization_level
        )
        
        return recommendation
    
    def _calculate_error_risk(self, dependency_level: int, profile: ConsumerProfile) -> float:
        """
        计算错误风险
        
        高依赖等级可能导致"过度自信"错误
        """
        base_error = sum(self.base_error_rates.values()) / len(self.base_error_rates)
        
        # 依赖等级影响：L4-L5可能因过度信任而增加某些错误
        if dependency_level >= 4:
            autonomy_error_boost = 0.05
        else:
            autonomy_error_boost = 0.0
        
        # 个性化降低错误
        personalization_discount = profile.personalization_level * 0.1
        
        error_prob = base_error + autonomy_error_boost - personalization_discount
        return np.clip(error_prob, 0, 1)
    
    def _select_error_type(self) -> AIErrorType:
        """根据概率选择错误类型"""
        error_types = list(self.base_error_rates.keys())
        probabilities = list(self.base_error_rates.values())
        
        # 归一化概率
        total = sum(probabilities)
        if total > 0:
            probabilities = [p / total for p in probabilities]
        else:
            probabilities = [1 / len(error_types)] * len(error_types)
        
        return np.random.choice(error_types, p=probabilities)
    
    def _apply_error_effect(self, items: List[Any], error_type: AIErrorType) -> List[Any]:
        """应用错误对推荐结果的影响"""
        if error_type == AIErrorType.MISUNDERSTANDING:
            # 完全错误推荐
            return items[::-1] if len(items) > 1 else items
        elif error_type == AIErrorType.FILTER_BUBBLE:
            # 过滤气泡：减少多样性
            return [items[0]] * len(items) if items else items
        else:
            return items
    
    def execute_order(self, recommendation: AIRecommendation, consumer_level: int) -> Dict:
        """
        执行订单（模拟）
        
        Args:
            recommendation: 推荐结果
            consumer_level: 消费者依赖等级
        
        Returns:
            执行结果
        """
        # 执行可靠性影响成功率
        success_prob = self.execution_reliability
        
        if consumer_level <= 2:
            # L1-L2用户会审核，降低执行错误影响
            success_prob = min(0.95, success_prob + 0.1)
        
        success = np.random.random() < success_prob
        
        outcome = {
            'success': success,
            'executed_by_ai': consumer_level >= 3,
            'quality': np.random.beta(5, 2) if success else np.random.beta(2, 5),
            'cost': np.random.normal(50, 15),
            'error': not success,
            'error_type': AIErrorType.EXECUTION_ERROR.value if not success else None
        }
        
        return outcome
    
    def update_from_interaction(self, 
                               consumer_id: int,
                               interaction: Dict):
        """
        从交互中学习更新
        
        Args:
            consumer_id: 消费者ID
            interaction: 交互记录
        """
        profile = self.get_or_create_profile(consumer_id)
        profile.update(interaction)
        
        # 经验回放
        self.experience_buffer.append({
            'consumer_id': consumer_id,
            'interaction': interaction,
        })
        
        # 限制缓冲区大小
        if len(self.experience_buffer) > 1000:
            self.experience_buffer.pop(0)
        
        # 更新满意度影响
        satisfaction = interaction.get('satisfaction', 0.5)
        self.avg_satisfaction_impact = (
            0.9 * self.avg_satisfaction_impact + 0.1 * satisfaction
        )
        
        # 学习能力：根据反馈调整
        if satisfaction < 0.3:
            # 负面反馈：提升理解深度
            self.understanding_depth = min(1.0, self.understanding_depth + self.learning_rate * 0.1)
    
    def get_performance_metrics(self) -> Dict:
        """获取性能指标"""
        error_rate = self.error_count / max(1, self.total_recommendations)
        
        return {
            'agent_id': self.id,
            'capacity_level': self.capacity_level,
            'total_recommendations': self.total_recommendations,
            'error_rate': error_rate,
            'error_breakdown': {t.value: c for t, c in self.error_by_type.items()},
            'avg_satisfaction_impact': self.avg_satisfaction_impact,
            'consumer_coverage': len(self.consumer_profiles),
            'recommendation_accuracy': self.recommendation_accuracy,
            'personalization_avg': np.mean([p.personalization_level for p in self.consumer_profiles.values()]) if self.consumer_profiles else 0,
        }


class AIAgentPopulation:
    """AI代理群体"""
    
    def __init__(self, n_agents: int = 2):
        """
        初始化AI代理群体
        
        Args:
            n_agents: AI代理数量
        """
        self.agents: List[AIAgent] = []
        
        # 创建不同能力等级的AI
        capacities = ['low', 'medium', 'high']
        for i in range(n_agents):
            capacity = capacities[i % len(capacities)]
            agent = AIAgent(agent_id=i, capacity_level=capacity)
            self.agents.append(agent)
    
    def select_agent_for_consumer(self, consumer_id: int, 
                                   preference: str = 'random') -> AIAgent:
        """
        为消费者选择AI代理
        
        Args:
            consumer_id: 消费者ID
            preference: 选择策略 ('random', 'best', 'closest')
        
        Returns:
            选中的AI代理
        """
        if preference == 'random':
            return np.random.choice(self.agents)
        elif preference == 'best':
            # 选择表现最好的
            return max(self.agents, key=lambda a: a.avg_satisfaction_impact)
        else:
            return np.random.choice(self.agents)
    
    def get_collective_metrics(self) -> Dict:
        """获取群体指标"""
        total_recs = sum(a.total_recommendations for a in self.agents)
        total_errors = sum(a.error_count for a in self.agents)
        
        return {
            'n_agents': len(self.agents),
            'total_recommendations': total_recs,
            'collective_error_rate': total_errors / max(1, total_recs),
            'agent_metrics': [a.get_performance_metrics() for a in self.agents],
        }
