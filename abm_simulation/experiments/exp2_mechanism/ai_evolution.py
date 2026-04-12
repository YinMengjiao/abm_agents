"""
实验3: AI代理进化机制
AI从消费者反馈中学习改进
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import deque
from enum import Enum


class AILearningMode(Enum):
    """AI学习模式"""
    PASSIVE = "passive"          # 被动学习：仅从错误中学习
    ACTIVE = "active"            # 主动学习：主动探索改进
    COLLABORATIVE = "collaborative"  # 协作学习：AI间共享经验


@dataclass
class LearningRecord:
    """学习记录"""
    timestamp: int
    feedback_type: str           # 'positive', 'negative', 'neutral'
    satisfaction_delta: float    # 满意度变化
    error_occurred: bool
    improvement_area: str        # 改进领域
    learning_gain: float         # 学习收益


class EvolvingAIAgent:
    """
    可进化的AI代理
    
    能够从消费者反馈中持续学习，动态提升能力
    """
    
    def __init__(self,
                 agent_id: int,
                 initial_capacity_level: str = 'medium',
                 learning_mode: AILearningMode = AILearningMode.ACTIVE,
                 evolution_rate: float = 0.02):
        """
        初始化可进化AI代理
        
        Args:
            agent_id: 代理标识
            initial_capacity_level: 初始能力等级
            learning_mode: 学习模式
            evolution_rate: 进化速率
        """
        self.id = agent_id
        self.learning_mode = learning_mode
        self.evolution_rate = evolution_rate
        
        # 动态能力属性（可进化）
        self._init_dynamic_capacity(initial_capacity_level)
        
        # 学习历史
        self.learning_history: deque = deque(maxlen=500)
        self.feedback_buffer: List[Dict] = []
        
        # 进化统计
        self.evolution_events = []
        self.capability_trajectory = []
        
        # 消费者知识库
        self.consumer_knowledge: Dict[int, Dict] = {}
        
        # 错误模式学习
        self.error_patterns: Dict[str, int] = {}
        self.success_patterns: Dict[str, int] = {}
        
    def _init_dynamic_capacity(self, level: str):
        """初始化动态能力（可随时间提升）"""
        base_params = {
            'low': {
                'recommendation_accuracy': 0.55,
                'understanding_depth': 0.45,
                'execution_reliability': 0.70,
                'adaptation_speed': 0.35,
                'personalization_ability': 0.30,
            },
            'medium': {
                'recommendation_accuracy': 0.75,
                'understanding_depth': 0.70,
                'execution_reliability': 0.85,
                'adaptation_speed': 0.60,
                'personalization_ability': 0.55,
            },
            'high': {
                'recommendation_accuracy': 0.90,
                'understanding_depth': 0.90,
                'execution_reliability': 0.95,
                'adaptation_speed': 0.85,
                'personalization_ability': 0.80,
            }
        }
        
        params = base_params.get(level, base_params['medium'])
        
        # 当前能力值
        self.recommendation_accuracy = params['recommendation_accuracy']
        self.understanding_depth = params['understanding_depth']
        self.execution_reliability = params['execution_reliability']
        self.adaptation_speed = params['adaptation_speed']
        self.personalization_ability = params['personalization_ability']
        
        # 能力上限（不同AI有不同的上限）
        self.accuracy_cap = min(0.98, params['recommendation_accuracy'] + 0.15)
        self.understanding_cap = min(0.98, params['understanding_depth'] + 0.15)
        self.reliability_cap = min(0.99, params['execution_reliability'] + 0.10)
        
        # 初始能力（用于计算进化程度）
        self.initial_accuracy = self.recommendation_accuracy
        self.initial_understanding = self.understanding_depth
        
    @property
    def current_error_rate(self) -> float:
        """计算当前错误率（随能力提升而降低）"""
        base_error = 0.25
        accuracy_discount = self.recommendation_accuracy * 0.20
        understanding_discount = self.understanding_depth * 0.15
        adaptation_discount = self.adaptation_speed * 0.10
        
        error_rate = max(0.02, base_error - accuracy_discount - understanding_discount - adaptation_discount)
        return error_rate
    
    @property
    def evolution_progress(self) -> float:
        """计算进化进度"""
        accuracy_progress = (self.recommendation_accuracy - self.initial_accuracy) / (self.accuracy_cap - self.initial_accuracy + 0.001)
        understanding_progress = (self.understanding_depth - self.initial_understanding) / (self.understanding_cap - self.initial_understanding + 0.001)
        return np.clip((accuracy_progress + understanding_progress) / 2, 0, 1)
    
    def process_feedback(self, 
                        consumer_id: int,
                        interaction_result: Dict,
                        step: int) -> LearningRecord:
        """
        处理消费者反馈并学习
        
        Args:
            consumer_id: 消费者ID
            interaction_result: 交互结果
            step: 当前时间步
            
        Returns:
            学习记录
        """
        satisfaction = interaction_result.get('satisfaction', 0.5)
        error_occurred = interaction_result.get('error', False)
        
        # 确定反馈类型
        if satisfaction >= 0.7:
            feedback_type = 'positive'
        elif satisfaction <= 0.3:
            feedback_type = 'negative'
        else:
            feedback_type = 'neutral'
        
        # 更新消费者知识
        self._update_consumer_knowledge(consumer_id, interaction_result)
        
        # 根据反馈类型学习
        learning_gain = 0.0
        improvement_area = "none"
        
        if feedback_type == 'negative' or error_occurred:
            # 从错误中学习（负向强化）
            learning_gain = self._learn_from_mistake(interaction_result)
            improvement_area = self._identify_improvement_area(interaction_result)
            
        elif feedback_type == 'positive':
            # 强化成功模式
            learning_gain = self._reinforce_success(interaction_result)
            improvement_area = "success_pattern"
            
        # 主动学习模式：额外探索
        if self.learning_mode == AILearningMode.ACTIVE and step % 10 == 0:
            exploration_gain = self._exploration_learning()
            learning_gain += exploration_gain
        
        # 记录学习
        record = LearningRecord(
            timestamp=step,
            feedback_type=feedback_type,
            satisfaction_delta=satisfaction - 0.5,
            error_occurred=error_occurred,
            improvement_area=improvement_area,
            learning_gain=learning_gain
        )
        self.learning_history.append(record)
        
        # 记录能力轨迹
        self.capability_trajectory.append({
            'step': step,
            'accuracy': self.recommendation_accuracy,
            'understanding': self.understanding_depth,
            'error_rate': self.current_error_rate
        })
        
        return record
    
    def _learn_from_mistake(self, interaction: Dict) -> float:
        """从错误中学习"""
        # 识别错误类型
        error_type = interaction.get('error_type', 'unknown')
        self.error_patterns[error_type] = self.error_patterns.get(error_type, 0) + 1
        
        # 根据错误类型针对性提升能力
        learning_gain = 0.0
        
        if error_type in ['misunderstanding', 'context_blindness']:
            # 提升理解深度
            old_val = self.understanding_depth
            self.understanding_depth = min(
                self.understanding_cap,
                self.understanding_depth + self.evolution_rate * self.adaptation_speed
            )
            learning_gain += (self.understanding_depth - old_val)
            
        elif error_type in ['preference_drift']:
            # 提升适应能力
            old_val = self.adaptation_speed
            self.adaptation_speed = min(0.95, self.adaptation_speed + self.evolution_rate)
            learning_gain += (self.adaptation_speed - old_val)
            
        elif error_type in ['execution_error']:
            # 提升执行可靠性
            old_val = self.execution_reliability
            self.execution_reliability = min(
                self.reliability_cap,
                self.execution_reliability + self.evolution_rate * 0.5
            )
            learning_gain += (self.execution_reliability - old_val)
        
        # 通用：提升推荐准确性
        old_accuracy = self.recommendation_accuracy
        self.recommendation_accuracy = min(
            self.accuracy_cap,
            self.recommendation_accuracy + self.evolution_rate * 0.5
        )
        learning_gain += (self.recommendation_accuracy - old_accuracy)
        
        return learning_gain
    
    def _reinforce_success(self, interaction: Dict) -> float:
        """强化成功模式"""
        context = interaction.get('context', 'general')
        self.success_patterns[context] = self.success_patterns.get(context, 0) + 1
        
        # 小幅提升个性化能力
        old_val = self.personalization_ability
        self.personalization_ability = min(0.95, self.personalization_ability + self.evolution_rate * 0.3)
        
        return self.personalization_ability - old_val
    
    def _identify_improvement_area(self, interaction: Dict) -> str:
        """识别需要改进的领域"""
        error_type = interaction.get('error_type', 'unknown')
        
        mapping = {
            'misunderstanding': 'understanding_depth',
            'context_blindness': 'context_awareness',
            'preference_drift': 'adaptation_speed',
            'execution_error': 'execution_reliability',
            'outdated_info': 'knowledge_update',
        }
        
        return mapping.get(error_type, 'general')
    
    def _exploration_learning(self) -> float:
        """主动探索学习"""
        # 随机选择一个能力维度小幅提升
        abilities = ['recommendation_accuracy', 'understanding_depth', 'personalization_ability']
        chosen = np.random.choice(abilities)
        
        if chosen == 'recommendation_accuracy':
            old_val = self.recommendation_accuracy
            self.recommendation_accuracy = min(self.accuracy_cap, self.recommendation_accuracy + self.evolution_rate * 0.2)
            return self.recommendation_accuracy - old_val
        elif chosen == 'understanding_depth':
            old_val = self.understanding_depth
            self.understanding_depth = min(self.understanding_cap, self.understanding_depth + self.evolution_rate * 0.2)
            return self.understanding_depth - old_val
        else:
            old_val = self.personalization_ability
            self.personalization_ability = min(0.95, self.personalization_ability + self.evolution_rate * 0.2)
            return self.personalization_ability - old_val
    
    def _update_consumer_knowledge(self, consumer_id: int, interaction: Dict):
        """更新消费者知识库"""
        if consumer_id not in self.consumer_knowledge:
            self.consumer_knowledge[consumer_id] = {
                'interactions': [],
                'preferences': {},
                'satisfaction_history': [],
                'error_history': []
            }
        
        knowledge = self.consumer_knowledge[consumer_id]
        knowledge['interactions'].append(interaction)
        knowledge['satisfaction_history'].append(interaction.get('satisfaction', 0.5))
        knowledge['error_history'].append(interaction.get('error', False))
        
        # 限制历史长度
        if len(knowledge['interactions']) > 50:
            knowledge['interactions'].pop(0)
            knowledge['satisfaction_history'].pop(0)
            knowledge['error_history'].pop(0)
    
    def update_from_interaction(self, consumer_id: int, interaction: Dict):
        """父类接口兼容：将 ABMSimulation 的学习调用委托给 process_feedback"""
        satisfaction = interaction.get('satisfaction', 0.5)
        error_occurred = interaction.get('error', False)
        interaction_result = {
            'satisfaction': satisfaction,
            'error': error_occurred,
            'error_type': interaction.get('error_type', 'unknown'),
            'context': interaction.get('context', 'general'),
        }
        # 用 step_count=0 占位；process_feedback 只用 step 做探索周期判断
        step = len(self.learning_history)
        self.process_feedback(consumer_id, interaction_result, step)

    def make_recommendation_with_evolution(self,
                                          consumer_id: int,
                                          available_options: List[Any],
                                          dependency_level: int) -> Dict:
        """
        生成推荐（考虑进化后的能力）
        
        Returns:
            推荐结果字典
        """
        if dependency_level == 1:
            return None
        
        # 根据当前能力计算推荐质量
        n_options = len(available_options)
        if n_options == 0:
            return {'items': [], 'quality': 0, 'error': True}
        
        # 进化后的错误率
        error_prob = self.current_error_rate
        
        # 个性化调整（基于消费者知识）
        personalization_boost = 0.0
        if consumer_id in self.consumer_knowledge:
            history = self.consumer_knowledge[consumer_id]
            if len(history['satisfaction_history']) > 5:
                avg_sat = np.mean(history['satisfaction_history'][-5:])
                personalization_boost = (avg_sat - 0.5) * 0.1
        
        effective_accuracy = self.recommendation_accuracy + personalization_boost
        effective_accuracy = np.clip(effective_accuracy, 0, 1)
        
        # 生成推荐
        error_occurred = np.random.random() < error_prob
        
        if error_occurred:
            # 错误推荐
            quality = np.random.beta(2, 5)
            error_type = np.random.choice(['misunderstanding', 'preference_drift', 'execution_error'])
        else:
            # 高质量推荐
            quality = np.random.beta(5 + effective_accuracy * 5, 2)
            error_type = None
        
        n_recommend = min(3, n_options)
        recommended_indices = np.random.choice(n_options, n_recommend, replace=False)
        recommended_items = [available_options[i] for i in recommended_indices]
        
        return {
            'items': recommended_items,
            'quality': quality,
            'error': error_occurred,
            'error_type': error_type,
            'confidence': effective_accuracy * (1 - error_prob)
        }
    
    def get_evolution_metrics(self) -> Dict:
        """获取进化指标"""
        recent_records = list(self.learning_history)[-50:] if self.learning_history else []
        
        return {
            'agent_id': self.id,
            'evolution_progress': self.evolution_progress,
            'current_error_rate': self.current_error_rate,
            'recommendation_accuracy': self.recommendation_accuracy,
            'understanding_depth': self.understanding_depth,
            'execution_reliability': self.execution_reliability,
            'personalization_ability': self.personalization_ability,
            'learning_mode': self.learning_mode.value,
            'total_learning_events': len(self.learning_history),
            'recent_positive_feedback': sum(1 for r in recent_records if r.feedback_type == 'positive'),
            'recent_negative_feedback': sum(1 for r in recent_records if r.feedback_type == 'negative'),
            'error_patterns': dict(self.error_patterns),
            'success_patterns': dict(self.success_patterns),
            'consumer_knowledge_size': len(self.consumer_knowledge),
        }


class EvolvingAIPopulation:
    """可进化的AI代理群体"""
    
    def __init__(self, n_agents: int = 3, evolution_rate: float = 0.02):
        """
        初始化AI群体
        
        Args:
            n_agents: AI代理数量
            evolution_rate: 群体进化速率
        """
        self.agents: List[EvolvingAIAgent] = []
        
        # 创建不同初始能力的AI
        capacities = ['low', 'medium', 'high']
        modes = [AILearningMode.PASSIVE, AILearningMode.ACTIVE, AILearningMode.COLLABORATIVE]
        
        for i in range(n_agents):
            capacity = capacities[i % len(capacities)]
            mode = modes[i % len(modes)]
            agent = EvolvingAIAgent(
                agent_id=i,
                initial_capacity_level=capacity,
                learning_mode=mode,
                evolution_rate=evolution_rate
            )
            self.agents.append(agent)
    
    def select_best_agent(self, consumer_id: int) -> EvolvingAIAgent:
        """为消费者选择最适合的AI（基于进化程度和历史表现）"""
        scores = []
        for agent in self.agents:
            score = agent.evolution_progress * 0.5 + (1 - agent.current_error_rate) * 0.5
            if consumer_id in agent.consumer_knowledge:
                history = agent.consumer_knowledge[consumer_id]
                if history['satisfaction_history']:
                    avg_sat = np.mean(history['satisfaction_history'][-5:])
                    score += avg_sat * 0.2
            scores.append(score)

        exp_scores = np.exp(np.array(scores) - np.max(scores))
        probs = exp_scores / np.sum(exp_scores)
        return np.random.choice(self.agents, p=probs)

    def select_agent_for_consumer(self, consumer_id: int, preference: str = 'random') -> EvolvingAIAgent:
        """父类接口兼容：委托给 select_best_agent（进化版始终选最优）"""
        return self.select_best_agent(consumer_id)

    def get_collective_metrics(self) -> Dict:
        """父类接口兼容：包装 get_population_evolution_metrics 以匹配 AIAgentPopulation 格式"""
        pop = self.get_population_evolution_metrics()
        return {
            'n_agents': pop['n_agents'],
            'total_recommendations': sum(
                len(a.learning_history) for a in self.agents
            ),
            'collective_error_rate': pop['avg_error_rate'],
            'agent_metrics': pop['agent_metrics'],
        }

    def get_population_evolution_metrics(self) -> Dict:
        """获取群体进化指标"""
        individual_metrics = [a.get_evolution_metrics() for a in self.agents]
        
        return {
            'n_agents': len(self.agents),
            'avg_evolution_progress': np.mean([m['evolution_progress'] for m in individual_metrics]),
            'avg_error_rate': np.mean([m['current_error_rate'] for m in individual_metrics]),
            'avg_accuracy': np.mean([m['recommendation_accuracy'] for m in individual_metrics]),
            'best_agent_id': max(individual_metrics, key=lambda x: x['evolution_progress'])['agent_id'],
            'agent_metrics': individual_metrics
        }
