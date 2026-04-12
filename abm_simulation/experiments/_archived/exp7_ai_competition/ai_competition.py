"""
实验7: 竞争AI代理市场
多AI竞争对消费者选择的影响
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class AIStrategy(Enum):
    """AI竞争策略"""
    PRICE_COMPETITION = "price"          # 价格竞争
    QUALITY_PREMIUM = "quality"          # 质量溢价
    DIFFERENTIATION = "differentiation"  # 差异化
    COLLABORATION = "collaboration"      # 协作策略


@dataclass
class AICompetitorProfile:
    """AI竞争者画像"""
    agent_id: int
    strategy: AIStrategy
    market_share: float = 0.0
    reputation: float = 0.5
    price_level: float = 1.0           # 价格水平（相对基准）
    quality_level: float = 0.7         # 质量水平
    innovation_rate: float = 0.1       # 创新速率
    customer_base: List[int] = field(default_factory=list)
    revenue_history: List[float] = field(default_factory=list)


class CompetitiveAIAgent:
    """
    竞争性AI代理
    
    在多AI市场中竞争消费者
    """
    
    def __init__(self,
                 agent_id: int,
                 strategy: AIStrategy = AIStrategy.QUALITY_PREMIUM,
                 initial_quality: float = 0.7):
        """
        初始化竞争性AI代理
        
        Args:
            agent_id: 代理ID
            strategy: 竞争策略
            initial_quality: 初始质量水平
        """
        self.id = agent_id
        self.strategy = strategy
        self.profile = AICompetitorProfile(
            agent_id=agent_id,
            strategy=strategy,
            quality_level=initial_quality
        )
        
        # 根据策略设置参数
        self._apply_strategy()
        
        # 性能指标
        self.total_recommendations = 0
        self.successful_recommendations = 0
        self.customer_satisfaction = []
        
    def _apply_strategy(self):
        """应用竞争策略"""
        if self.strategy == AIStrategy.PRICE_COMPETITION:
            self.profile.price_level = 0.8
            self.profile.quality_level = 0.6
            self.profile.innovation_rate = 0.05
        elif self.strategy == AIStrategy.QUALITY_PREMIUM:
            self.profile.price_level = 1.2
            self.profile.quality_level = 0.9
            self.profile.innovation_rate = 0.15
        elif self.strategy == AIStrategy.DIFFERENTIATION:
            self.profile.price_level = 1.0
            self.profile.quality_level = 0.75
            self.profile.innovation_rate = 0.2
        elif self.strategy == AIStrategy.COLLABORATION:
            self.profile.price_level = 1.0
            self.profile.quality_level = 0.7
            self.profile.innovation_rate = 0.1
    
    def make_competitive_offer(self, 
                              consumer_id: int,
                              consumer_level: int,
                              competitors: List) -> Dict:
        """
        生成竞争性报价
        
        Args:
            consumer_id: 消费者ID
            consumer_level: 消费者依赖等级
            competitors: 竞争对手列表
            
        Returns:
            报价信息
        """
        # 根据策略调整报价
        base_quality = self.profile.quality_level
        base_price = self.profile.price_level
        
        # 针对高依赖消费者调整
        if consumer_level >= 4:
            if self.strategy == AIStrategy.QUALITY_PREMIUM:
                base_quality *= 1.1  # 质量溢价
            elif self.strategy == AIStrategy.PRICE_COMPETITION:
                base_price *= 0.9    # 价格优惠
        
        # 根据声誉调整
        reputation_boost = self.profile.reputation * 0.1
        
        # 计算推荐质量
        effective_quality = base_quality * (1 + reputation_boost)
        error_prob = max(0.02, 0.3 - effective_quality * 0.25)
        
        self.total_recommendations += 1
        
        return {
            'agent_id': self.id,
            'quality': effective_quality,
            'price': base_price,
            'error_prob': error_prob,
            'strategy': self.strategy.value
        }
    
    def update_from_outcome(self, 
                           consumer_id: int,
                           won: bool,
                           satisfaction: float):
        """
        根据竞争结果更新
        
        Args:
            consumer_id: 消费者ID
            won: 是否赢得该消费者
            satisfaction: 消费者满意度
        """
        if won:
            self.successful_recommendations += 1
            if consumer_id not in self.profile.customer_base:
                self.profile.customer_base.append(consumer_id)
        
        self.customer_satisfaction.append(satisfaction)
        
        # 更新声誉
        recent_satisfaction = np.mean(self.customer_satisfaction[-20:]) if self.customer_satisfaction else 0.5
        self.profile.reputation = 0.8 * self.profile.reputation + 0.2 * recent_satisfaction
        
        # 策略调整（进化）
        self._evolve_strategy()
    
    def _evolve_strategy(self):
        """根据市场表现进化策略"""
        success_rate = self.successful_recommendations / max(1, self.total_recommendations)
        
        # 如果表现不佳，小幅调整
        if success_rate < 0.3 and np.random.random() < 0.1:
            if self.strategy == AIStrategy.PRICE_COMPETITION:
                self.profile.quality_level = min(0.95, self.profile.quality_level + 0.05)
            elif self.strategy == AIStrategy.QUALITY_PREMIUM:
                self.profile.price_level = max(0.8, self.profile.price_level - 0.05)
    
    def get_competitive_metrics(self) -> Dict:
        """获取竞争指标"""
        success_rate = self.successful_recommendations / max(1, self.total_recommendations)
        
        return {
            'agent_id': self.id,
            'strategy': self.strategy.value,
            'market_share': self.profile.market_share,
            'reputation': self.profile.reputation,
            'success_rate': success_rate,
            'customer_count': len(self.profile.customer_base),
            'quality_level': self.profile.quality_level,
            'price_level': self.profile.price_level,
        }


class CompetitiveAIMarket:
    """
    竞争性AI市场
    
    管理多个AI代理的竞争
    """
    
    def __init__(self, n_agents: int = 4):
        """
        初始化竞争市场
        
        Args:
            n_agents: AI代理数量
        """
        self.agents: List[CompetitiveAIAgent] = []
        
        # 创建不同策略的AI
        strategies = [
            AIStrategy.PRICE_COMPETITION,
            AIStrategy.QUALITY_PREMIUM,
            AIStrategy.DIFFERENTIATION,
            AIStrategy.COLLABORATION
        ]
        
        for i in range(n_agents):
            strategy = strategies[i % len(strategies)]
            agent = CompetitiveAIAgent(
                agent_id=i,
                strategy=strategy,
                initial_quality=0.6 + np.random.random() * 0.3
            )
            self.agents.append(agent)
        
        self.competition_history = []
        self.market_concentration_history = []
    
    def compete_for_consumer(self, 
                            consumer_id: int,
                            consumer_level: int,
                            consumer_traits: Dict) -> Tuple[CompetitiveAIAgent, Dict]:
        """
        为竞争消费者
        
        Args:
            consumer_id: 消费者ID
            consumer_level: 消费者依赖等级
            consumer_traits: 消费者特征
            
        Returns:
            (获胜AI, 竞争详情)
        """
        # 所有AI提交报价
        offers = []
        for agent in self.agents:
            offer = agent.make_competitive_offer(
                consumer_id=consumer_id,
                consumer_level=consumer_level,
                competitors=[a for a in self.agents if a != agent]
            )
            offers.append((agent, offer))
        
        # 消费者选择（基于效用函数）
        winner, choice_details = self._consumer_choice(
            consumer_id, offers, consumer_traits
        )
        
        # 记录竞争结果
        self.competition_history.append({
            'consumer_id': consumer_id,
            'winner_id': winner.id,
            'offers': [o[1] for o in offers]
        })
        
        return winner, choice_details
    
    def _consumer_choice(self, 
                        consumer_id: int,
                        offers: List[Tuple],
                        consumer_traits: Dict) -> Tuple[CompetitiveAIAgent, Dict]:
        """
        模拟消费者选择
        
        基于多属性效用理论
        """
        # 消费者偏好权重
        quality_weight = consumer_traits.get('quality_preference', 0.5)
        price_weight = consumer_traits.get('price_sensitivity', 0.3)
        reputation_weight = consumer_traits.get('reputation_preference', 0.2)
        
        utilities = []
        for agent, offer in offers:
            utility = (
                quality_weight * offer['quality'] +
                price_weight * (1 - offer['price'] + 1) +  # 价格越低越好
                reputation_weight * agent.profile.reputation
            )
            utilities.append((agent, offer, utility))
        
        # softmax选择
        exp_utils = np.exp([u[2] for u in utilities] - np.max([u[2] for u in utilities]))
        probs = exp_utils / np.sum(exp_utils)
        
        winner_idx = np.random.choice(len(utilities), p=probs)
        winner, offer, _ = utilities[winner_idx]
        
        return winner, {
            'chosen_agent_id': winner.id,
            'utility_scores': {f'agent_{u[0].id}': u[2] for u in utilities},
            'selection_probability': probs[winner_idx]
        }
    
    def update_market_shares(self, total_consumers: int):
        """更新市场份额"""
        for agent in self.agents:
            agent.profile.market_share = len(agent.profile.customer_base) / max(1, total_consumers)
        
        # 计算市场集中度（赫芬达尔指数）
        shares = [a.profile.market_share for a in self.agents]
        hhi = sum(s**2 for s in shares)
        self.market_concentration_history.append(hhi)
    
    def get_market_metrics(self) -> Dict:
        """获取市场指标"""
        agent_metrics = [a.get_competitive_metrics() for a in self.agents]
        
        # 计算竞争强度
        market_shares = [m['market_share'] for m in agent_metrics]
        competition_intensity = 1 - max(market_shares) if market_shares else 0
        
        return {
            'n_agents': len(self.agents),
            'agent_metrics': agent_metrics,
            'market_concentration': self.market_concentration_history[-1] if self.market_concentration_history else 0,
            'competition_intensity': competition_intensity,
            'total_competitions': len(self.competition_history)
        }
