"""
实验9: 偏见与过滤气泡
AI推荐是否造成选择窄化
"""

import numpy as np
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class ProductCategory:
    """产品类别"""
    category_id: int
    name: str
    popularity: float              # 流行度
    diversity_score: float         # 多样性得分
    related_categories: List[int] = field(default_factory=list)


@dataclass
class ConsumerChoiceHistory:
    """消费者选择历史"""
    consumer_id: int
    chosen_categories: List[int] = field(default_factory=list)
    exposed_categories: Set[int] = field(default_factory=set)
    exploration_events: int = 0
    total_choices: int = 0


class FilterBubbleAnalyzer:
    """
    过滤气泡分析器
    
    分析AI推荐对消费者选择多样性的影响
    """
    
    def __init__(self, n_categories: int = 20):
        """
        初始化分析器
        
        Args:
            n_categories: 产品类别数量
        """
        self.n_categories = n_categories
        self.categories: Dict[int, ProductCategory] = {}
        self.consumer_histories: Dict[int, ConsumerChoiceHistory] = {}
        self._init_categories()
    
    def _init_categories(self):
        """初始化产品类别"""
        category_names = [
            '中餐', '西餐', '日料', '韩餐', '快餐',
            '甜品', '咖啡', '茶饮', '火锅', '烧烤',
            '素食', '海鲜', '面食', '米饭', '小吃',
            '健康餐', '异国料理', '地方特色', '网红店', '传统老店'
        ]
        
        for i in range(self.n_categories):
            # 创建类别关系网络
            related = list(set(np.random.choice(self.n_categories, 3, replace=False)) - {i})
            
            self.categories[i] = ProductCategory(
                category_id=i,
                name=category_names[i] if i < len(category_names) else f'类别{i}',
                popularity=np.random.beta(2, 2),
                diversity_score=np.random.random(),
                related_categories=related
            )
    
    def simulate_ai_recommendation(self, 
                                  consumer_id: int,
                                  ai_dependency_level: int,
                                  personalization_strength: float = 0.7) -> List[int]:
        """
        模拟AI推荐
        
        Args:
            consumer_id: 消费者ID
            ai_dependency_level: AI依赖等级
            personalization_strength: 个性化强度
            
        Returns:
            推荐类别列表
        """
        # 获取或创建消费者历史
        if consumer_id not in self.consumer_histories:
            self.consumer_histories[consumer_id] = ConsumerChoiceHistory(consumer_id)
        
        history = self.consumer_histories[consumer_id]
        
        # 推荐数量
        n_recommendations = 5
        
        # 根据依赖等级调整个性化程度
        if ai_dependency_level <= 2:
            # 低依赖：更多探索性推荐
            personalization_strength *= 0.5
        elif ai_dependency_level >= 4:
            # 高依赖：强个性化
            personalization_strength = min(0.95, personalization_strength * 1.2)
        
        # 基于历史偏好的推荐
        if history.chosen_categories and np.random.random() < personalization_strength:
            # 从历史偏好中选择
            preferred = history.chosen_categories[-10:]
            recommended = list(np.random.choice(preferred, 
                                              min(n_recommendations, len(preferred)), 
                                              replace=False))
            
            # 补充一些流行类别
            while len(recommended) < n_recommendations:
                popular = [c for c in self.categories.keys() 
                          if c not in recommended and self.categories[c].popularity > 0.5]
                if popular:
                    recommended.append(np.random.choice(popular))
                else:
                    break
        else:
            # 探索性推荐
            recommended = list(np.random.choice(self.n_categories, n_recommendations, replace=False))
        
        # 记录暴露的类别
        history.exposed_categories.update(recommended)
        
        return recommended
    
    def simulate_consumer_choice(self,
                                consumer_id: int,
                                recommendations: List[int],
                                exploration_tendency: float = 0.3) -> int:
        """
        模拟消费者选择
        
        Args:
            consumer_id: 消费者ID
            recommendations: 推荐列表
            exploration_tendency: 探索倾向
            
        Returns:
            选择的类别
        """
        history = self.consumer_histories[consumer_id]
        
        # 是否探索
        if np.random.random() < exploration_tendency:
            # 探索：选择推荐之外的类别
            unexplored = [c for c in self.categories.keys() if c not in recommendations]
            if unexplored:
                choice = np.random.choice(unexplored)
                history.exploration_events += 1
            else:
                choice = np.random.choice(recommendations)
        else:
            # 利用：从推荐中选择
            choice = np.random.choice(recommendations)
        
        history.chosen_categories.append(choice)
        history.total_choices += 1
        
        return choice
    
    def calculate_diversity_metrics(self, consumer_id: int) -> Dict:
        """
        计算单个消费者的选择多样性指标
        
        Args:
            consumer_id: 消费者ID
            
        Returns:
            多样性指标
        """
        if consumer_id not in self.consumer_histories:
            return {}
        
        history = self.consumer_histories[consumer_id]
        
        if history.total_choices == 0:
            return {'diversity_score': 0, 'exploration_rate': 0}
        
        # 类别多样性（香农熵）
        category_counts = defaultdict(int)
        for cat in history.chosen_categories:
            category_counts[cat] += 1
        
        total = len(history.chosen_categories)
        entropy = 0
        for count in category_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)
        
        # 归一化熵（最大熵为log2(n_categories)）
        max_entropy = np.log2(self.n_categories)
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        # 探索率
        exploration_rate = history.exploration_events / history.total_choices
        
        # 暴露覆盖率
        coverage = len(history.exposed_categories) / self.n_categories
        
        return {
            'diversity_score': normalized_entropy,
            'exploration_rate': exploration_rate,
            'category_coverage': coverage,
            'n_unique_categories': len(category_counts),
            'total_choices': history.total_choices
        }
    
    def calculate_population_diversity(self, dependency_levels: Dict[int, int]) -> Dict:
        """
        计算群体层面的多样性指标
        
        Args:
            dependency_levels: {消费者ID: 依赖等级}
            
        Returns:
            群体多样性指标
        """
        # 按依赖等级分组
        diversity_by_level = {i: [] for i in range(1, 6)}
        
        for consumer_id, level in dependency_levels.items():
            metrics = self.calculate_diversity_metrics(consumer_id)
            if metrics:
                diversity_by_level[level].append(metrics['diversity_score'])
        
        # 计算各等级的平均多样性
        avg_diversity_by_level = {}
        for level, scores in diversity_by_level.items():
            if scores:
                avg_diversity_by_level[level] = np.mean(scores)
            else:
                avg_diversity_by_level[level] = 0
        
        # 整体多样性
        all_scores = []
        for scores in diversity_by_level.values():
            all_scores.extend(scores)
        
        overall_diversity = np.mean(all_scores) if all_scores else 0
        
        # 过滤气泡强度（高依赖vs低依赖的多样性差异）
        high_dep_diversity = avg_diversity_by_level.get(5, 0) + avg_diversity_by_level.get(4, 0)
        low_dep_diversity = avg_diversity_by_level.get(1, 0) + avg_diversity_by_level.get(2, 0)
        bubble_strength = abs(high_dep_diversity - low_dep_diversity) / 2
        
        return {
            'overall_diversity': overall_diversity,
            'diversity_by_level': avg_diversity_by_level,
            'filter_bubble_strength': bubble_strength,
            'high_vs_low_diff': high_dep_diversity - low_dep_diversity
        }
    
    def run_filter_bubble_experiment(self, 
                                    n_consumers: int = 500,
                                    n_rounds: int = 50) -> Dict:
        """
        运行过滤气泡实验
        
        Args:
            n_consumers: 消费者数量
            n_rounds: 实验轮数
            
        Returns:
            实验结果
        """
        # 初始化消费者依赖等级
        dependency_levels = {}
        for i in range(n_consumers):
            dependency_levels[i] = np.random.choice([1, 2, 3, 4, 5], 
                                                    p=[0.15, 0.20, 0.30, 0.25, 0.10])
        
        # 运行多轮选择
        for round_num in range(n_rounds):
            for consumer_id in range(n_consumers):
                level = dependency_levels[consumer_id]
                
                # AI推荐
                recommendations = self.simulate_ai_recommendation(
                    consumer_id, level
                )
                
                # 消费者选择
                exploration_tendency = 0.5 - (level - 3) * 0.1  # 高依赖者探索倾向低
                self.simulate_consumer_choice(consumer_id, recommendations, exploration_tendency)
        
        # 计算结果
        population_metrics = self.calculate_population_diversity(dependency_levels)
        
        # 个体层面分析
        individual_metrics = []
        for consumer_id in range(n_consumers):
            metrics = self.calculate_diversity_metrics(consumer_id)
            metrics['consumer_id'] = consumer_id
            metrics['dependency_level'] = dependency_levels[consumer_id]
            individual_metrics.append(metrics)
        
        return {
            'population_metrics': population_metrics,
            'individual_metrics': individual_metrics,
            'dependency_levels': dependency_levels
        }


class DiversityIntervention:
    """多样性干预策略"""
    
    def __init__(self, analyzer: FilterBubbleAnalyzer):
        """
        初始化干预器
        
        Args:
            analyzer: 过滤气泡分析器
        """
        self.analyzer = analyzer
    
    def apply_diversity_boost(self, 
                             recommendations: List[int],
                             boost_strength: float = 0.3) -> List[int]:
        """
        应用多样性增强
        
        Args:
            recommendations: 原始推荐
            boost_strength: 增强强度
            
        Returns:
            增强后的推荐
        """
        if np.random.random() > boost_strength:
            return recommendations
        
        # 替换部分推荐为多样性类别
        diverse_categories = [c for c in self.analyzer.categories.keys() 
                             if c not in recommendations and 
                             self.analyzer.categories[c].diversity_score > 0.6]
        
        if diverse_categories:
            n_replace = max(1, int(len(recommendations) * 0.3))
            new_items = np.random.choice(diverse_categories, min(n_replace, len(diverse_categories)), replace=False)
            
            enhanced = recommendations[:-n_replace] + list(new_items)
            return enhanced
        
        return recommendations
    
    def calculate_intervention_effect(self, 
                                     original_diversity: float,
                                     enhanced_diversity: float) -> Dict:
        """计算干预效果"""
        improvement = enhanced_diversity - original_diversity
        
        return {
            'original_diversity': original_diversity,
            'enhanced_diversity': enhanced_diversity,
            'absolute_improvement': improvement,
            'relative_improvement': improvement / max(0.001, original_diversity)
        }
