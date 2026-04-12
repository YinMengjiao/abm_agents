"""
实验6: 多代际演化
长期代际更替对AI依赖文化的影响
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class GenerationType(Enum):
    """代际类型"""
    IMMIGRANT = "immigrant"          # 技术移民代（较晚接触AI）
    NATIVE = "native"                # 技术原生代（从小接触AI）
    TRANSITIONAL = "transitional"    # 过渡代


@dataclass
class GenerationTraits:
    """代际特征"""
    generation_type: GenerationType
    birth_step: int                  # 出生时间步
    tech_comfort: float              # 技术舒适度 (0-1)
    trust_baseline: float            # 基线信任度
    social_influence_susceptibility: float  # 社会影响易感性
    learning_speed: float            # 学习速度
    risk_tolerance: float            # 风险容忍度


class GenerationalConsumer:
    """
    代际消费者
    
    具有代际特征的消费者
    """
    
    def __init__(self, 
                 consumer_id: int,
                 generation_traits: GenerationTraits,
                 parent_influence: Optional[Dict] = None):
        """
        初始化代际消费者
        
        Args:
            consumer_id: 消费者ID
            generation_traits: 代际特征
            parent_influence: 父母影响（代际传递）
        """
        self.id = consumer_id
        self.generation = generation_traits
        
        # 初始依赖等级受代际特征影响
        self.dependency_level = self._initialize_dependency_level()
        
        # 个人历史
        self.interaction_history = []
        self.satisfaction_history = []
        
        # 代际传递的影响
        if parent_influence:
            self._apply_parent_influence(parent_influence)
    
    def _initialize_dependency_level(self) -> int:
        """根据代际特征初始化依赖等级"""
        if self.generation.generation_type == GenerationType.NATIVE:
            # 原生代更倾向于使用AI
            base_prob = [0.1, 0.15, 0.25, 0.30, 0.20]  # L1-L5概率
        elif self.generation.generation_type == GenerationType.IMMIGRANT:
            # 移民代更保守
            base_prob = [0.25, 0.30, 0.25, 0.15, 0.05]
        else:
            # 过渡代居中
            base_prob = [0.15, 0.20, 0.30, 0.25, 0.10]
        
        # 根据技术舒适度调整
        tech_factor = self.generation.tech_comfort
        adjusted_prob = [
            base_prob[0] * (1 - tech_factor * 0.5),
            base_prob[1] * (1 - tech_factor * 0.3),
            base_prob[2],
            base_prob[3] * (1 + tech_factor * 0.3),
            base_prob[4] * (1 + tech_factor * 0.5)
        ]
        
        # 归一化
        total = sum(adjusted_prob)
        adjusted_prob = [p / total for p in adjusted_prob]
        
        return np.random.choice([1, 2, 3, 4, 5], p=adjusted_prob)
    
    def _apply_parent_influence(self, parent_influence: Dict):
        """应用父母影响（代际传递）"""
        parent_level = parent_influence.get('dependency_level', 3)
        influence_strength = parent_influence.get('influence_strength', 0.3)
        
        # 父母影响以一定概率改变初始等级
        if np.random.random() < influence_strength:
            # 向父母等级靠拢
            if self.dependency_level < parent_level:
                self.dependency_level = min(5, self.dependency_level + 1)
            elif self.dependency_level > parent_level:
                self.dependency_level = max(1, self.dependency_level - 1)
    
    def update_from_experience(self, satisfaction: float, used_ai: bool):
        """从经验中更新"""
        self.satisfaction_history.append(satisfaction)
        self.interaction_history.append({'satisfaction': satisfaction, 'used_ai': used_ai})
        
        # 根据满意度调整依赖等级
        if len(self.satisfaction_history) >= 5:
            recent_sat = np.mean(self.satisfaction_history[-5:])
            
            if recent_sat > 0.7 and self.dependency_level < 5:
                if np.random.random() < self.generation.learning_speed * 0.1:
                    self.dependency_level += 1
            elif recent_sat < 0.3 and self.dependency_level > 1:
                if np.random.random() < self.generation.risk_tolerance * 0.1:
                    self.dependency_level -= 1


class GenerationalDynamics:
    """
    代际动力学
    
    管理代际更替过程
    """
    
    def __init__(self,
                 initial_population: int = 500,
                 generation_duration: int = 100,  # 每代持续时间
                 n_generations: int = 5):
        """
        初始化代际动力学
        
        Args:
            initial_population: 初始人口
            generation_duration: 每代持续时间（步数）
            n_generations: 总代数
        """
        self.initial_population = initial_population
        self.generation_duration = generation_duration
        self.n_generations = n_generations
        
        self.current_generation = 0
        self.consumers: Dict[int, GenerationalConsumer] = {}
        self.generation_history: List[Dict] = []
        
        # 初始化第一代
        self._initialize_first_generation()
    
    def _initialize_first_generation(self):
        """初始化第一代（技术移民代）"""
        for i in range(self.initial_population):
            traits = GenerationTraits(
                generation_type=GenerationType.IMMIGRANT,
                birth_step=0,
                tech_comfort=np.random.beta(2, 5),  # 较低的技术舒适度
                trust_baseline=np.random.beta(3, 4),  # 中等信任基线
                social_influence_susceptibility=np.random.beta(4, 3),
                learning_speed=np.random.beta(2, 4),  # 学习较慢
                risk_tolerance=np.random.beta(2, 5)  # 风险厌恶
            )
            
            self.consumers[i] = GenerationalConsumer(
                consumer_id=i,
                generation_traits=traits
            )
    
    def step(self, current_step: int) -> Dict:
        """
        执行代际步骤
        
        Args:
            current_step: 当前时间步
            
        Returns:
            代际事件统计
        """
        events = {
            'new_generation': False,
            'births': 0,
            'deaths': 0,
            'generation_transitions': []
        }
        
        # 检查是否进入新一代
        if current_step > 0 and current_step % self.generation_duration == 0:
            if self.current_generation < self.n_generations - 1:
                events['new_generation'] = True
                self.current_generation += 1
                
                # 代际更替
                transition = self._generation_turnover(current_step)
                events.update(transition)
        
        return events
    
    def _generation_turnover(self, current_step: int) -> Dict:
        """执行代际更替"""
        # 确定新一代类型
        if self.current_generation == 1:
            new_gen_type = GenerationType.TRANSITIONAL
        else:
            new_gen_type = GenerationType.NATIVE
        
        # 选择退出的人口（最老的）
        exit_ratio = 0.2  # 20%退出
        n_exit = int(len(self.consumers) * exit_ratio)
        
        # 按年龄排序（这里用ID模拟，ID小的更老）
        sorted_consumers = sorted(self.consumers.items(), key=lambda x: x[0])
        exiting_ids = [cid for cid, _ in sorted_consumers[:n_exit]]
        
        # 记录父母影响
        parent_influences = {}
        for cid in exiting_ids:
            parent_influences[cid] = {
                'dependency_level': self.consumers[cid].dependency_level,
                'influence_strength': 0.3
            }
        
        # 移除退出者
        for cid in exiting_ids:
            del self.consumers[cid]
        
        # 添加新一代
        new_ids = range(max(self.consumers.keys()) + 1, 
                       max(self.consumers.keys()) + 1 + n_exit)
        
        for new_id in new_ids:
            # 随机选择一个父母影响
            parent_inf = np.random.choice(list(parent_influences.values()))
            
            if new_gen_type == GenerationType.NATIVE:
                traits = GenerationTraits(
                    generation_type=new_gen_type,
                    birth_step=current_step,
                    tech_comfort=np.random.beta(5, 2),  # 高技术舒适度
                    trust_baseline=np.random.beta(4, 3),
                    social_influence_susceptibility=np.random.beta(5, 2),
                    learning_speed=np.random.beta(5, 2),  # 学习快
                    risk_tolerance=np.random.beta(4, 3)  # 风险容忍
                )
            else:  # TRANSITIONAL
                traits = GenerationTraits(
                    generation_type=new_gen_type,
                    birth_step=current_step,
                    tech_comfort=np.random.beta(3, 3),
                    trust_baseline=np.random.beta(3, 3),
                    social_influence_susceptibility=np.random.beta(4, 3),
                    learning_speed=np.random.beta(3, 3),
                    risk_tolerance=np.random.beta(3, 3)
                )
            
            self.consumers[new_id] = GenerationalConsumer(
                consumer_id=new_id,
                generation_traits=traits,
                parent_influence=parent_inf
            )
        
        # 记录历史
        self.generation_history.append({
            'step': current_step,
            'generation': self.current_generation,
            'type': new_gen_type.value,
            'exits': len(exiting_ids),
            'entries': len(new_ids)
        })
        
        return {
            'births': len(new_ids),
            'deaths': len(exiting_ids),
            'generation_transitions': [self.current_generation]
        }
    
    def get_generation_composition(self) -> Dict:
        """获取当前代际构成"""
        composition = {gen_type.value: 0 for gen_type in GenerationType}
        
        for consumer in self.consumers.values():
            gen_type = consumer.generation.generation_type.value
            composition[gen_type] += 1
        
        return composition
    
    def get_dependency_by_generation(self) -> Dict:
        """获取各代际的依赖分布"""
        by_gen = {gen_type.value: {i: 0 for i in range(1, 6)} 
                 for gen_type in GenerationType}
        
        for consumer in self.consumers.values():
            gen_type = consumer.generation.generation_type.value
            level = consumer.dependency_level
            by_gen[gen_type][level] += 1
        
        return by_gen
    
    def get_summary(self) -> Dict:
        """获取代际动力学汇总"""
        return {
            'current_generation': self.current_generation,
            'total_consumers': len(self.consumers),
            'generation_composition': self.get_generation_composition(),
            'dependency_by_generation': self.get_dependency_by_generation(),
            'generation_history': self.generation_history
        }
