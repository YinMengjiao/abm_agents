"""
实验8: 情境敏感性
不同消费场景下的依赖行为差异
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ConsumptionContext(Enum):
    """消费情境类型"""
    HIGH_FREQ_LOW_COST = "high_freq_low_cost"      # 高频低额（外卖）
    LOW_FREQ_HIGH_COST = "low_freq_high_cost"      # 低频高额（旅游）
    TIME_PRESSURE = "time_pressure"                # 时间压力
    SOCIAL_VISIBLE = "social_visible"              # 社交可见
    PERSONAL_PRIVATE = "personal_private"          # 个人私密
    EMERGENCY = "emergency"                        # 紧急情况


@dataclass
class ContextCharacteristics:
    """情境特征"""
    context_type: ConsumptionContext
    price_level: float              # 价格水平 (0-1, 越高越贵)
    frequency: float                # 消费频率 (0-1, 越高越频繁)
    time_pressure: float            # 时间压力 (0-1)
    social_visibility: float        # 社交可见性 (0-1)
    personal_importance: float      # 个人重要性 (0-1)
    risk_level: float               # 风险水平 (0-1)
    ai_suitability: float           # AI适用性 (0-1)


class ContextManager:
    """
    情境管理器
    
    管理不同消费情境及其对消费者决策的影响
    """
    
    def __init__(self):
        """初始化情境管理器"""
        self.contexts: Dict[ConsumptionContext, ContextCharacteristics] = {}
        self._init_default_contexts()
        self.current_context: Optional[ConsumptionContext] = None
    
    def _init_default_contexts(self):
        """初始化默认情境"""
        self.contexts = {
            ConsumptionContext.HIGH_FREQ_LOW_COST: ContextCharacteristics(
                context_type=ConsumptionContext.HIGH_FREQ_LOW_COST,
                price_level=0.2,
                frequency=0.9,
                time_pressure=0.4,
                social_visibility=0.3,
                personal_importance=0.3,
                risk_level=0.2,
                ai_suitability=0.8
            ),
            ConsumptionContext.LOW_FREQ_HIGH_COST: ContextCharacteristics(
                context_type=ConsumptionContext.LOW_FREQ_HIGH_COST,
                price_level=0.9,
                frequency=0.1,
                time_pressure=0.3,
                social_visibility=0.5,
                personal_importance=0.8,
                risk_level=0.6,
                ai_suitability=0.4
            ),
            ConsumptionContext.TIME_PRESSURE: ContextCharacteristics(
                context_type=ConsumptionContext.TIME_PRESSURE,
                price_level=0.5,
                frequency=0.5,
                time_pressure=0.9,
                social_visibility=0.4,
                personal_importance=0.6,
                risk_level=0.4,
                ai_suitability=0.7
            ),
            ConsumptionContext.SOCIAL_VISIBLE: ContextCharacteristics(
                context_type=ConsumptionContext.SOCIAL_VISIBLE,
                price_level=0.6,
                frequency=0.4,
                time_pressure=0.3,
                social_visibility=0.9,
                personal_importance=0.7,
                risk_level=0.5,
                ai_suitability=0.3
            ),
            ConsumptionContext.PERSONAL_PRIVATE: ContextCharacteristics(
                context_type=ConsumptionContext.PERSONAL_PRIVATE,
                price_level=0.4,
                frequency=0.6,
                time_pressure=0.2,
                social_visibility=0.1,
                personal_importance=0.5,
                risk_level=0.3,
                ai_suitability=0.6
            ),
            ConsumptionContext.EMERGENCY: ContextCharacteristics(
                context_type=ConsumptionContext.EMERGENCY,
                price_level=0.7,
                frequency=0.1,
                time_pressure=1.0,
                social_visibility=0.2,
                personal_importance=0.9,
                risk_level=0.8,
                ai_suitability=0.5
            )
        }
    
    def set_context(self, context: ConsumptionContext):
        """设置当前情境"""
        self.current_context = context
    
    def get_context_modifier(self, base_dependency_level: int, 
                            consumer_traits: Dict) -> int:
        """
        获取情境对依赖等级的修正
        
        Args:
            base_dependency_level: 基础依赖等级
            consumer_traits: 消费者特征
            
        Returns:
            修正后的依赖等级
        """
        if self.current_context is None:
            return base_dependency_level
        
        context = self.contexts[self.current_context]
        
        # 计算情境调整因子
        adjustment = 0
        
        # 高频低额情境：更倾向使用AI
        if context.frequency > 0.7 and context.price_level < 0.3:
            adjustment += 1
        
        # 低频高额情境：更谨慎
        if context.frequency < 0.3 and context.price_level > 0.7:
            adjustment -= 1
        
        # 时间压力：可能增加AI使用（如果信任AI）
        if context.time_pressure > 0.7:
            trust = consumer_traits.get('trust_tendency', 0.5)
            if trust > 0.6:
                adjustment += 1
        
        # 社交可见性：可能减少AI使用（面子考虑）
        if context.social_visibility > 0.7:
            adjustment -= 1
        
        # 风险水平：高风险更谨慎
        if context.risk_level > 0.6:
            risk_tolerance = consumer_traits.get('risk_tolerance', 0.5)
            if risk_tolerance < 0.5:
                adjustment -= 1
        
        # 应用调整
        new_level = base_dependency_level + adjustment
        return max(1, min(5, new_level))
    
    def calculate_context_satisfaction(self, 
                                      base_satisfaction: float,
                                      used_ai: bool) -> float:
        """
        计算情境调整后的满意度
        
        Args:
            base_satisfaction: 基础满意度
            used_ai: 是否使用AI
            
        Returns:
            调整后满意度
        """
        if self.current_context is None:
            return base_satisfaction
        
        context = self.contexts[self.current_context]
        
        modifier = 0.0
        
        # 在适合AI的情境使用AI：满意度提升
        if used_ai and context.ai_suitability > 0.6:
            modifier += 0.1
        
        # 在不适合AI的情境使用AI：满意度下降
        if used_ai and context.ai_suitability < 0.4:
            modifier -= 0.15
        
        # 时间压力情境下快速决策：满意度提升
        if context.time_pressure > 0.7 and used_ai:
            modifier += 0.05
        
        return np.clip(base_satisfaction + modifier, 0, 1)


class ContextualConsumer:
    """
    情境化消费者
    
    在不同情境下表现出不同行为的消费者
    """
    
    def __init__(self, consumer_id: int, base_dependency_level: int = 3):
        """
        初始化情境化消费者
        
        Args:
            consumer_id: 消费者ID
            base_dependency_level: 基础依赖等级
        """
        self.id = consumer_id
        self.base_dependency_level = base_dependency_level
        self.context_history: List[Tuple[ConsumptionContext, int]] = []
        self.satisfaction_by_context: Dict[str, List[float]] = {
            ctx.value: [] for ctx in ConsumptionContext
        }
    
    def make_contextual_decision(self, 
                                 context: ConsumptionContext,
                                 context_manager: ContextManager,
                                 consumer_traits: Dict) -> Dict:
        """
        做出情境化决策
        
        Args:
            context: 当前情境
            context_manager: 情境管理器
            consumer_traits: 消费者特征
            
        Returns:
            决策结果
        """
        # 设置情境
        context_manager.set_context(context)
        
        # 获取情境调整后的依赖等级
        adjusted_level = context_manager.get_context_modifier(
            self.base_dependency_level,
            consumer_traits
        )
        
        # 记录历史
        self.context_history.append((context, adjusted_level))
        
        # 决定是否使用AI
        uses_ai = adjusted_level >= 3
        
        # 模拟结果
        context_char = context_manager.contexts[context]
        base_satisfaction = np.random.beta(5, 2) if uses_ai else np.random.beta(4, 3)
        
        # 应用情境满意度调整
        final_satisfaction = context_manager.calculate_context_satisfaction(
            base_satisfaction, uses_ai
        )
        
        # 记录满意度
        self.satisfaction_by_context[context.value].append(final_satisfaction)
        
        return {
            'base_level': self.base_dependency_level,
            'adjusted_level': adjusted_level,
            'uses_ai': uses_ai,
            'satisfaction': final_satisfaction,
            'context': context.value
        }
    
    def get_context_preference(self) -> Dict[str, float]:
        """获取各情境的AI使用偏好"""
        preferences = {}
        
        for context_type, history in self.satisfaction_by_context.items():
            if history:
                avg_satisfaction = np.mean(history)
                preferences[context_type] = avg_satisfaction
            else:
                preferences[context_type] = 0.5
        
        return preferences


class ContextExperimentRunner:
    """情境实验运行器"""
    
    def __init__(self, n_consumers: int = 500):
        """
        初始化实验运行器
        
        Args:
            n_consumers: 消费者数量
        """
        self.n_consumers = n_consumers
        self.context_manager = ContextManager()
        self.consumers: List[ContextualConsumer] = []
        self._init_consumers()
        
        self.results_by_context: Dict[str, List[Dict]] = {
            ctx.value: [] for ctx in ConsumptionContext
        }
    
    def _init_consumers(self):
        """初始化消费者"""
        for i in range(self.n_consumers):
            # 随机基础依赖等级
            base_level = np.random.choice([1, 2, 3, 4, 5], p=[0.15, 0.20, 0.30, 0.25, 0.10])
            consumer = ContextualConsumer(i, base_level)
            self.consumers.append(consumer)
    
    def run_context_experiment(self, 
                              context: ConsumptionContext,
                              n_rounds: int = 50) -> Dict:
        """
        运行单一情境实验
        
        Args:
            context: 测试情境
            n_rounds: 轮数
            
        Returns:
            实验结果
        """
        results = []
        
        for _ in range(n_rounds):
            for consumer in self.consumers:
                traits = {
                    'trust_tendency': np.random.beta(3, 3),
                    'risk_tolerance': np.random.beta(3, 3)
                }
                
                decision = consumer.make_contextual_decision(
                    context, self.context_manager, traits
                )
                results.append(decision)
        
        self.results_by_context[context.value] = results
        
        # 统计分析
        ai_usage_rate = sum(1 for r in results if r['uses_ai']) / len(results)
        avg_satisfaction = np.mean([r['satisfaction'] for r in results])
        avg_adjusted_level = np.mean([r['adjusted_level'] for r in results])
        
        return {
            'context': context.value,
            'ai_usage_rate': ai_usage_rate,
            'avg_satisfaction': avg_satisfaction,
            'avg_adjusted_level': avg_adjusted_level,
            'n_samples': len(results)
        }
    
    def run_all_contexts(self) -> Dict[str, Dict]:
        """运行所有情境实验"""
        all_results = {}
        
        for context in ConsumptionContext:
            print(f"  运行 {context.value} 情境...")
            result = self.run_context_experiment(context)
            all_results[context.value] = result
        
        return all_results
    
    def get_cross_context_analysis(self) -> Dict:
        """获取跨情境分析"""
        analysis = {
            'context_ranking_by_ai_usage': [],
            'context_ranking_by_satisfaction': [],
            'context_sensitivity': {}
        }
        
        # 按AI使用率排名
        ai_usage_ranking = sorted(
            self.results_by_context.items(),
            key=lambda x: sum(1 for r in x[1] if r['uses_ai']) / max(1, len(x[1])),
            reverse=True
        )
        analysis['context_ranking_by_ai_usage'] = [
            (ctx, sum(1 for r in results if r['uses_ai']) / max(1, len(results)))
            for ctx, results in ai_usage_ranking
        ]
        
        # 按满意度排名
        sat_ranking = sorted(
            self.results_by_context.items(),
            key=lambda x: np.mean([r['satisfaction'] for r in x[1]]) if x[1] else 0,
            reverse=True
        )
        analysis['context_ranking_by_satisfaction'] = [
            (ctx, np.mean([r['satisfaction'] for r in results]) if results else 0)
            for ctx, results in sat_ranking
        ]
        
        return analysis
