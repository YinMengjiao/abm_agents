"""
实验2：带有复杂记忆机制的消费者智能体
基于基线模型，增加经验记忆对决策的影响
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import deque
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from agents.consumer_dib import ConsumerAgentDIB, ConsumerTraits, DesireState, IntentionState, BehaviorOutcome


@dataclass
class ExperienceMemory:
    """单次经验记忆"""
    step: int
    dependency_level: int
    ai_involved: bool
    satisfaction: float
    error_occurred: bool
    error_type: Optional[str]
    decision_time: float
    actual_cost: float
    expected_quality: float
    actual_quality: float
    surprise: float  # 预期与实际差异
    
    # 情境信息
    market_condition: str = 'normal'
    social_influence: float = 0.0
    urgency: float = 0.5


@dataclass
class MemorySummary:
    """记忆统计摘要"""
    # AI使用经验统计
    ai_experiences_count: int = 0
    ai_satisfaction_avg: float = 0.5
    ai_error_rate: float = 0.0
    ai_satisfaction_variance: float = 0.0
    
    # 非AI使用经验统计
    non_ai_experiences_count: int = 0
    non_ai_satisfaction_avg: float = 0.5
    non_ai_error_rate: float = 0.0
    
    # 近期趋势（最近20次）
    recent_ai_satisfaction_trend: float = 0.0
    recent_satisfaction_volatility: float = 0.0
    
    # 错误模式
    error_recovery_rate: float = 0.0  # 错误后恢复满意度比例
    consecutive_errors: int = 0
    
    # 记忆权重（时间衰减后的有效记忆）
    effective_memory_weight: float = 1.0


class ConsumerAgentWithMemory(ConsumerAgentDIB):
    """
    带有复杂记忆机制的消费者智能体
    
    扩展功能：
    1. 经验记忆存储（时间窗口+重要性筛选）
    2. 记忆衰减与强化
    3. 记忆影响D-I-B决策
    4. 错误恢复学习
    """
    
    def __init__(self, agent_id: int, initial_level: int = 3,
                 traits: Optional[ConsumerTraits] = None,
                 memory_capacity: int = 50,
                 memory_decay_rate: float = 0.95):
        """
        初始化带记忆消费者
        
        Args:
            memory_capacity: 记忆容量（最近N次经验）
            memory_decay_rate: 记忆衰减率
        """
        super().__init__(agent_id, initial_level, traits)
        
        # 记忆系统
        self.memory_capacity = memory_capacity
        self.memory_decay_rate = memory_decay_rate
        self.experiences_memory: deque = deque(maxlen=memory_capacity)
        
        # 记忆权重（每次经验的权重随时间衰减）
        self.memory_weights: List[float] = []
        
        # 记忆摘要（缓存）
        self.memory_summary = MemorySummary()
        
        # 错误恢复追踪
        self.error_history: List[bool] = []
        self.post_error_satisfaction: List[float] = []
        
        # 信任动态（基于经验）
        self.dynamic_trust = self.traits.trust_tendency  # 动态信任度
        self.trust_momentum = 0.0  # 信任变化动量
        
        # 探索-利用平衡
        self.exploration_tendency = 0.2  # 探索新方式的概率
        self.exploitation_streak = 0  # 连续使用同策略次数
        
    def store_experience(self, step: int, context: Dict):
        """存储经验到记忆"""
        # 计算惊喜度（预期vs实际）
        expected_quality = self.intention.quality_threshold
        actual_quality = self.behavior.actual_quality
        surprise = abs(actual_quality - expected_quality)
        
        exp_memory = ExperienceMemory(
            step=step,
            dependency_level=self.dependency_level,
            ai_involved=self.behavior.ai_involvement_level > 0,
            satisfaction=self.behavior.satisfaction,
            error_occurred=self.behavior.error_occurred,
            error_type=self.behavior.error_type,
            decision_time=self.behavior.decision_time,
            actual_cost=self.behavior.actual_cost,
            expected_quality=expected_quality,
            actual_quality=actual_quality,
            surprise=surprise,
            market_condition=context.get('market_condition', 'normal'),
            social_influence=context.get('social_influence', 0.0),
            urgency=context.get('urgency', 0.5)
        )
        
        self.experiences_memory.append(exp_memory)
        
        # 更新记忆权重（新记忆权重为1，旧记忆衰减）
        self.memory_weights = [w * self.memory_decay_rate for w in self.memory_weights]
        self.memory_weights.append(1.0)
        
        # 更新记忆摘要
        self._update_memory_summary()
        
        # 更新信任动态
        self._update_trust_dynamics(exp_memory)
        
        # 记录原始经验
        self.record_experience(step, context)
    
    def _update_memory_summary(self):
        """更新记忆统计摘要"""
        if not self.experiences_memory:
            return
        
        memories = list(self.experiences_memory)
        weights = np.array(self.memory_weights[-len(memories):])
        weights = weights / np.sum(weights) if np.sum(weights) > 0 else np.ones(len(memories)) / len(memories)
        
        # AI使用经验
        ai_memories = [m for m in memories if m.ai_involved]
        if ai_memories:
            ai_satisfactions = [m.satisfaction for m in ai_memories]
            self.memory_summary.ai_experiences_count = len(ai_memories)
            self.memory_summary.ai_satisfaction_avg = np.mean(ai_satisfactions)
            self.memory_summary.ai_error_rate = np.mean([m.error_occurred for m in ai_memories])
            self.memory_summary.ai_satisfaction_variance = np.var(ai_satisfactions)
        
        # 非AI使用经验
        non_ai_memories = [m for m in memories if not m.ai_involved]
        if non_ai_memories:
            self.memory_summary.non_ai_experiences_count = len(non_ai_memories)
            self.memory_summary.non_ai_satisfaction_avg = np.mean([m.satisfaction for m in non_ai_memories])
            self.memory_summary.non_ai_error_rate = np.mean([m.error_occurred for m in non_ai_memories])
        
        # 近期趋势（最近20次或全部）
        recent_n = min(20, len(memories))
        recent_memories = memories[-recent_n:]
        recent_satisfactions = [m.satisfaction for m in recent_memories]
        
        if len(recent_satisfactions) >= 5:
            # 趋势：后半段vs前半段
            mid = len(recent_satisfactions) // 2
            self.memory_summary.recent_ai_satisfaction_trend = (
                np.mean(recent_satisfactions[mid:]) - np.mean(recent_satisfactions[:mid])
            )
            self.memory_summary.recent_satisfaction_volatility = np.std(recent_satisfactions)
        
        # 错误恢复率
        self._calculate_error_recovery()
        
        # 连续错误计数
        self.memory_summary.consecutive_errors = self._count_consecutive_errors()
        
        # 有效记忆权重
        self.memory_summary.effective_memory_weight = np.mean(weights)
    
    def _calculate_error_recovery(self):
        """计算错误恢复能力"""
        memories = list(self.experiences_memory)
        error_followed_by_recovery = 0
        total_errors = 0
        
        for i, mem in enumerate(memories):
            if mem.error_occurred:
                total_errors += 1
                # 看后续几次经验是否恢复满意度
                subsequent = memories[i+1:i+4]
                if subsequent and np.mean([m.satisfaction for m in subsequent]) > 0.5:
                    error_followed_by_recovery += 1
        
        self.memory_summary.error_recovery_rate = (
            error_followed_by_recovery / total_errors if total_errors > 0 else 1.0
        )
    
    def _count_consecutive_errors(self) -> int:
        """计算最近连续错误次数"""
        memories = list(self.experiences_memory)
        consecutive = 0
        for mem in reversed(memories):
            if mem.error_occurred:
                consecutive += 1
            else:
                break
        return consecutive
    
    def _update_trust_dynamics(self, new_memory: ExperienceMemory):
        """基于新经验更新信任动态"""
        # 信任调整因子
        trust_adjustment = 0.0
        
        if new_memory.ai_involved:
            # AI使用经验影响信任
            if new_memory.error_occurred:
                # 错误大幅降低信任
                trust_adjustment = -0.15 * (1 + self.memory_summary.consecutive_errors * 0.5)
            elif new_memory.satisfaction > 0.7:
                # 高满意度小幅提升信任
                trust_adjustment = 0.05
            elif new_memory.surprise > 0.3:
                # 大惊喜（无论正负）增加不确定性
                trust_adjustment = -0.02
        else:
            # 非AI经验影响
            if new_memory.satisfaction > 0.7 and new_memory.decision_time < 3:
                # 高效且满意的非AI经验降低AI信任
                trust_adjustment = -0.03
        
        # 应用动量
        self.trust_momentum = 0.7 * self.trust_momentum + 0.3 * trust_adjustment
        
        # 更新动态信任
        self.dynamic_trust = np.clip(
            self.dynamic_trust + trust_adjustment + 0.1 * self.trust_momentum,
            0.0, 1.0
        )
    
    def desire_formation(self, context: Dict) -> DesireState:
        """
        D层：欲望形成（记忆增强版）
        
        过往经验影响当前欲望强度
        """
        # 基础欲望形成
        desire = super().desire_formation(context)
        
        # 记忆影响：如果AI经验差，增加控制需求
        if self.memory_summary.ai_error_rate > 0.2:
            # AI错误率高时，更追求控制感
            desire.quality_pursuit = min(1.0, desire.quality_pursuit * 1.3)
            desire.convenience_need *= 0.9
        
        # 连续错误后，降低便利需求（更谨慎）
        if self.memory_summary.consecutive_errors >= 2:
            desire.convenience_need *= 0.8
            desire.quality_pursuit = min(1.0, desire.quality_pursuit * 1.2)
        
        # 近期满意度下降趋势时，增加价格敏感
        if self.memory_summary.recent_ai_satisfaction_trend < -0.1:
            desire.price_sensitivity = min(1.0, desire.price_sensitivity * 1.2)
        
        desire.normalize()
        return desire
    
    def intention_formation(self, desire: DesireState, context: Dict) -> IntentionState:
        """
        I层：意图形成（记忆增强版）
        
        过往经验显著影响AI使用意图
        """
        # 基础意图形成
        intention = super().intention_formation(desire, context)
        
        # 记忆驱动的意图调整
        memory_adjustment = 0.0
        
        # 1. 基于AI经验质量的调整
        if self.memory_summary.ai_experiences_count >= 3:
            ai_avg = self.memory_summary.ai_satisfaction_avg
            non_ai_avg = self.memory_summary.non_ai_satisfaction_avg
            
            # 如果AI经验显著差于非AI，降低AI意图
            if ai_avg < non_ai_avg - 0.15:
                memory_adjustment -= 0.2
            # 如果AI经验显著更好，增加AI意图
            elif ai_avg > non_ai_avg + 0.15:
                memory_adjustment += 0.15
        
        # 2. 错误率影响
        if self.memory_summary.ai_error_rate > 0.15:
            memory_adjustment -= 0.15 * self.memory_summary.ai_error_rate
        
        # 3. 连续错误惩罚
        if self.memory_summary.consecutive_errors >= 2:
            memory_adjustment -= 0.1 * self.memory_summary.consecutive_errors
        
        # 4. 近期趋势影响
        if self.memory_summary.recent_ai_satisfaction_trend < -0.1:
            memory_adjustment -= 0.1
        elif self.memory_summary.recent_ai_satisfaction_trend > 0.1:
            memory_adjustment += 0.05
        
        # 5. 探索-利用平衡
        if self.exploitation_streak > 10:
            # 长期同一策略，增加探索概率
            memory_adjustment += np.random.uniform(-0.1, 0.1)
            self.exploitation_streak = 0
        
        # 应用记忆调整（加权平均）
        memory_weight = min(1.0, self.memory_summary.ai_experiences_count / 10)
        adjusted_probability = (
            (1 - memory_weight) * intention.use_ai_probability +
            memory_weight * np.clip(intention.use_ai_probability + memory_adjustment, 0, 1)
        )
        
        intention.use_ai_probability = adjusted_probability
        
        # 动态信任也影响意图
        intention.use_ai_probability *= (0.5 + 0.5 * self.dynamic_trust)
        intention.use_ai_probability = np.clip(intention.use_ai_probability, 0, 1)
        
        # 更新搜索深度（基于记忆）
        if self.memory_summary.ai_error_rate > 0.1:
            # AI错误多，增加人工审核深度
            intention.search_depth = int(intention.search_depth * 1.5)
        
        return intention
    
    def behavior_execution(self, intention: IntentionState, ai_recommendation: Optional[Any],
                          alternatives: List[Any]) -> BehaviorOutcome:
        """
        B层：行为执行（记忆增强版）
        
        基于经验调整实际行为
        """
        # 记录当前策略以追踪探索-利用
        intended_ai_use = intention.use_ai_probability
        
        behavior = super().behavior_execution(intention, ai_recommendation, alternatives)
        
        # 更新探索-利用追踪
        actual_ai_used = behavior.ai_involvement_level > 0
        if actual_ai_used == (intended_ai_use > 0.5):
            self.exploitation_streak += 1
        else:
            self.exploitation_streak = 0
        
        return behavior
    
    def get_memory_statistics(self) -> Dict:
        """获取记忆相关统计"""
        return {
            'agent_id': self.id,
            'memory_count': len(self.experiences_memory),
            'dynamic_trust': self.dynamic_trust,
            'trust_momentum': self.trust_momentum,
            'ai_satisfaction_avg': self.memory_summary.ai_satisfaction_avg,
            'ai_error_rate': self.memory_summary.ai_error_rate,
            'consecutive_errors': self.memory_summary.consecutive_errors,
            'error_recovery_rate': self.memory_summary.error_recovery_rate,
            'recent_trend': self.memory_summary.recent_ai_satisfaction_trend,
            'exploration_streak': self.exploitation_streak,
        }
