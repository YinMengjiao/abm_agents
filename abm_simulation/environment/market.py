"""
市场环境与商家模型
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ProductCategory(Enum):
    """产品类别"""
    FOOD = "food"
    RETAIL = "retail"
    SERVICE = "service"
    ENTERTAINMENT = "entertainment"


@dataclass
class Product:
    """产品/服务"""
    product_id: int
    name: str
    category: ProductCategory
    base_price: float
    quality: float  # 0-1
    popularity: float = 0.5
    
    def get_actual_price(self, market_condition: str = 'normal') -> float:
        """根据市场条件获取实际价格"""
        multipliers = {
            'boom': 1.1,
            'normal': 1.0,
            'recession': 0.9
        }
        return self.base_price * multipliers.get(market_condition, 1.0)


@dataclass
class Merchant:
    """商家"""
    merchant_id: int
    name: str
    quality_level: float = 0.7
    price_level: float = 1.0
    reputation: float = 0.6
    algorithm_bias: str = 'neutral'  # 'neutral', 'promotion', 'quality'
    products: List[Product] = field(default_factory=list)
    
    def __post_init__(self):
        self.quality_level = np.clip(self.quality_level, 0, 1)
        self.reputation = np.clip(self.reputation, 0, 1)
    
    def generate_products(self, n_products: int = 10):
        """生成产品列表"""
        categories = list(ProductCategory)
        
        for i in range(n_products):
            category = np.random.choice(categories)
            
            # 根据商家质量生成产品质量
            quality = np.random.beta(
                2 + self.quality_level * 3,
                2 + (1 - self.quality_level) * 3
            )
            
            product = Product(
                product_id=i,
                name=f"Product_{self.merchant_id}_{i}",
                category=category,
                base_price=np.random.lognormal(3, 0.5) * self.price_level,
                quality=quality,
                popularity=np.random.beta(2, 2)
            )
            self.products.append(product)
    
    def get_offers(self, 
                   ai_agent_present: bool = False,
                   consumer_profile: Optional[Dict] = None) -> List[Product]:
        """
        获取商家提供的商品
        
        Args:
            ai_agent_present: 是否有AI代理参与
            consumer_profile: 消费者画像
        """
        if ai_agent_present:
            # AI代理能更好识别真实质量，商家需更诚实
            return self._transparent_pricing()
        else:
            # 人类消费者更容易受营销影响
            return self._marketing_optimized_pricing(consumer_profile)
    
    def _transparent_pricing(self) -> List[Product]:
        """透明定价（AI存在时）"""
        return sorted(self.products, key=lambda p: p.quality, reverse=True)
    
    def _marketing_optimized_pricing(self, consumer_profile: Optional[Dict]) -> List[Product]:
        """营销优化定价（人类决策时）"""
        if self.algorithm_bias == 'promotion':
            # 推广高利润产品
            return sorted(self.products, key=lambda p: p.base_price * (1 - p.quality * 0.3), reverse=True)
        elif self.algorithm_bias == 'quality':
            return sorted(self.products, key=lambda p: p.quality, reverse=True)
        else:
            return self.products


class MarketEnvironment:
    """
    市场环境
    
    管理商家、产品、市场条件等
    """
    
    def __init__(self, 
                 n_merchants: int = 20,
                 market_condition: str = 'normal'):
        """
        初始化市场环境
        
        Args:
            n_merchants: 商家数量
            market_condition: 市场状况 ('boom', 'normal', 'recession')
        """
        self.n_merchants = n_merchants
        self.market_condition = market_condition
        
        # 创建商家
        self.merchants: List[Merchant] = []
        self._create_merchants()
        
        # 所有可用产品
        self.all_products: List[Product] = []
        for m in self.merchants:
            self.all_products.extend(m.products)
        
        # 市场动态
        self.price_index = 1.0
        self.quality_index = 0.5
        self.competition_intensity = 0.5
        
        # 历史记录
        self.condition_history = [market_condition]
        self.price_history = [self.price_index]
    
    def _create_merchants(self):
        """创建商家群体"""
        bias_types = ['neutral', 'promotion', 'quality']
        
        for i in range(self.n_merchants):
            # 随机生成商家属性
            quality = np.random.beta(2, 2)
            price = np.random.lognormal(0, 0.3)
            reputation = np.random.beta(3, 2)
            bias = np.random.choice(bias_types)
            
            merchant = Merchant(
                merchant_id=i,
                name=f"Merchant_{i}",
                quality_level=quality,
                price_level=price,
                reputation=reputation,
                algorithm_bias=bias
            )
            
            # 生成产品
            merchant.generate_products(n_products=np.random.randint(5, 15))
            self.merchants.append(merchant)
    
    def get_available_options(self, 
                              category: Optional[ProductCategory] = None,
                              n_options: int = 20) -> List[Product]:
        """
        获取可用选项
        
        Args:
            category: 产品类别筛选
            n_options: 返回选项数量
        """
        if category:
            filtered = [p for p in self.all_products if p.category == category]
        else:
            filtered = self.all_products
        
        if len(filtered) <= n_options:
            return filtered
        
        # 随机采样
        indices = np.random.choice(len(filtered), n_options, replace=False)
        return [filtered[i] for i in indices]
    
    def simulate_transaction(self, 
                            product: Product,
                            ai_involved: bool,
                            dependency_level: int) -> Dict:
        """
        模拟交易结果
        
        Args:
            product: 选择的产品
            ai_involved: 是否有AI参与
            dependency_level: 消费者依赖等级
        
        Returns:
            交易结果
        """
        base_price = product.get_actual_price(self.market_condition)
        
        # AI参与可能获得更好价格（比价能力）
        if ai_involved and dependency_level >= 3:
            price_discount = np.random.uniform(0, 0.1)
        else:
            price_discount = 0
        
        final_price = base_price * (1 - price_discount)
        
        # 质量实现（有随机性）
        actual_quality = np.clip(
            product.quality + np.random.normal(0, 0.1),
            0, 1
        )
        
        # 错误概率（与AI参与相关）
        if ai_involved:
            error_prob = 0.05 + (5 - dependency_level) * 0.02
        else:
            error_prob = 0.1  # 人工决策也可能出错
        
        error_occurred = np.random.random() < error_prob
        
        outcome = {
            'product_id': product.product_id,
            'product_name': product.name,
            'category': product.category.value,
            'expected_quality': product.quality,
            'actual_quality': actual_quality,
            'price': final_price,
            'ai_involved': ai_involved,
            'error': error_occurred,
            'error_type': 'delivery' if error_occurred else None,
        }
        
        return outcome
    
    def update_market_condition(self, new_condition: str):
        """更新市场状况"""
        self.market_condition = new_condition
        self.condition_history.append(new_condition)
        
        # 更新价格指数
        multipliers = {'boom': 1.1, 'normal': 1.0, 'recession': 0.9}
        self.price_index = multipliers.get(new_condition, 1.0)
        self.price_history.append(self.price_index)
    
    def get_market_metrics(self) -> Dict:
        """获取市场指标"""
        avg_quality = np.mean([p.quality for p in self.all_products])
        avg_price = np.mean([p.base_price for p in self.all_products])
        
        return {
            'n_merchants': len(self.merchants),
            'n_products': len(self.all_products),
            'avg_quality': avg_quality,
            'avg_price': avg_price,
            'current_condition': self.market_condition,
            'price_index': self.price_index,
        }


@dataclass
class SimulationContext:
    """仿真上下文"""
    step: int = 0
    time_of_day: float = 12.0  # 0-24
    day_of_week: int = 0  # 0-6
    market_condition: str = 'normal'
    social_temperature: float = 1.0
    external_shock: Optional[str] = None
    
    def advance_time(self, hours: float = 1.0):
        """推进时间"""
        self.time_of_day += hours
        if self.time_of_day >= 24:
            self.time_of_day -= 24
            self.day_of_week = (self.day_of_week + 1) % 7
        self.step += 1
    
    def get_consumer_context(self, agent_id: int) -> Dict:
        """获取特定消费者的上下文"""
        return {
            'time_since_last_meal': self._calculate_hunger_factor(),
            'urgency': self._calculate_urgency(),
            'social_influence': 0.0,  # 由Ising网络填充
            'market_condition': self.market_condition,
            'budget': np.random.lognormal(4, 0.5),
            'complexity': np.random.beta(2, 2),
        }
    
    def _calculate_hunger_factor(self) -> float:
        """计算饥饿因子"""
        # 用餐时间附近饥饿度更高
        meal_times = [8, 12, 18]
        min_distance = min(abs(self.time_of_day - mt) for mt in meal_times)
        return 1 - min_distance / 12
    
    def _calculate_urgency(self) -> float:
        """计算紧急程度"""
        # 工作时间更紧急
        if 9 <= self.time_of_day <= 17:
            return np.random.beta(3, 2)
        else:
            return np.random.beta(2, 3)
