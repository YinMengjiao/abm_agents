"""
实验4: 信息干预与政策效果
外部信息冲击影响系统演化
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class InterventionType(Enum):
    """干预类型"""
    POSITIVE_PUBLICITY = "positive_publicity"      # 正面宣传
    NEGATIVE_EXPOSURE = "negative_exposure"        # 负面曝光
    MANDATORY_COOLDOWN = "mandatory_cooldown"      # 强制冷却期
    EDUCATION_CAMPAIGN = "education_campaign"      # 教育活动
    REGULATION_ENFORCEMENT = "regulation"          # 监管执法


class InterventionTiming(Enum):
    """干预时机"""
    EARLY = "early"          # 早期干预 (步数 < 30%)
    MIDDLE = "middle"        # 中期干预 (30% < 步数 < 70%)
    LATE = "late"            # 晚期干预 (步数 > 70%)
    MULTIPLE = "multiple"    # 多次干预


@dataclass
class InterventionEvent:
    """干预事件"""
    intervention_type: InterventionType
    timing: int                    # 发生时间步
    intensity: float               # 干预强度 (0-1)
    duration: int                  # 持续步数
    target_group: Optional[str]    # 目标群体 ('all', 'high_dependency', 'low_dependency')


class InformationIntervention:
    """
    信息干预系统
    
    模拟外部信息冲击对消费者行为的影响
    """
    
    def __init__(self):
        """初始化干预系统"""
        self.intervention_history: List[InterventionEvent] = []
        self.active_interventions: List[InterventionEvent] = []
        self.intervention_effects: Dict[int, Dict] = {}
        
        # 干预效果参数
        self.effect_params = {
            InterventionType.POSITIVE_PUBLICITY: {
                'trust_boost': 0.15,
                'satisfaction_boost': 0.10,
                'adoption_boost': 0.08,
                'decay_rate': 0.95,
            },
            InterventionType.NEGATIVE_EXPOSURE: {
                'trust_drop': -0.25,
                'satisfaction_drop': -0.15,
                'abandonment_boost': 0.12,
                'decay_rate': 0.90,
            },
            InterventionType.MANDATORY_COOLDOWN: {
                'forced_level_reduction': 1,  # 强制降低1级
                'satisfaction_penalty': -0.05,
                'decay_rate': 1.0,  # 立即生效，无衰减
            },
            InterventionType.EDUCATION_CAMPAIGN: {
                'informed_decision_boost': 0.20,
                'trust_calibration': 0.10,
                'decay_rate': 0.98,
            },
            InterventionType.REGULATION_ENFORCEMENT: {
                'safety_perception_boost': 0.15,
                'trust_floor': 0.30,  # 设置信任下限
                'decay_rate': 0.97,
            }
        }
    
    def schedule_intervention(self, 
                             intervention_type: InterventionType,
                             timing: int,
                             intensity: float = 0.5,
                             duration: int = 20,
                             target_group: str = 'all') -> InterventionEvent:
        """
        调度干预事件
        
        Args:
            intervention_type: 干预类型
            timing: 发生时间步
            intensity: 干预强度
            duration: 持续步数
            target_group: 目标群体
            
        Returns:
            干预事件
        """
        event = InterventionEvent(
            intervention_type=intervention_type,
            timing=timing,
            intensity=intensity,
            duration=duration,
            target_group=target_group
        )
        self.intervention_history.append(event)
        return event
    
    def apply_intervention(self, 
                          step: int,
                          consumers: List,
                          network) -> Dict:
        """
        在指定时间步应用干预
        
        Args:
            step: 当前时间步
            consumers: 消费者列表
            network: 社交网络
            
        Returns:
            干预效果统计
        """
        effects = {
            'interventions_applied': 0,
            'consumers_affected': 0,
            'level_changes': [],
            'trust_changes': [],
        }
        
        # 检查是否有干预需要应用
        for event in self.intervention_history:
            if event.timing == step:
                self.active_interventions.append(event)
                effect = self._execute_intervention(event, consumers, network)
                effects['interventions_applied'] += 1
                effects['consumers_affected'] += effect['n_affected']
                effects['level_changes'].extend(effect['level_changes'])
                effects['trust_changes'].extend(effect['trust_changes'])
        
        # 更新活跃干预的效果
        self._update_active_interventions(step, consumers)
        
        self.intervention_effects[step] = effects
        return effects
    
    def _execute_intervention(self,
                             event: InterventionEvent,
                             consumers: List,
                             network) -> Dict:
        """执行具体干预"""
        effect = {'n_affected': 0, 'level_changes': [], 'trust_changes': []}
        params = self.effect_params[event.intervention_type]
        
        # 确定目标消费者
        target_consumers = self._select_target_consumers(consumers, event.target_group)
        
        if event.intervention_type == InterventionType.POSITIVE_PUBLICITY:
            # 正面宣传：提升信任和满意度
            for consumer in target_consumers:
                if np.random.random() < event.intensity:
                    # 提升依赖等级（向更高等级移动）
                    current_spin = network.get_node_spin(consumer.id)
                    if current_spin < 2 and np.random.random() < 0.3:
                        new_spin = min(2, current_spin + 1)
                        network.set_node_spin(consumer.id, new_spin)
                        effect['level_changes'].append((consumer.id, current_spin, new_spin))
                    effect['n_affected'] += 1
                    
        elif event.intervention_type == InterventionType.NEGATIVE_EXPOSURE:
            # 负面曝光：降低信任和满意度
            for consumer in target_consumers:
                if np.random.random() < event.intensity:
                    # 降低依赖等级
                    current_spin = network.get_node_spin(consumer.id)
                    if current_spin > -2 and np.random.random() < 0.4:
                        new_spin = max(-2, current_spin - 1)
                        network.set_node_spin(consumer.id, new_spin)
                        effect['level_changes'].append((consumer.id, current_spin, new_spin))
                    effect['n_affected'] += 1
                    
        elif event.intervention_type == InterventionType.MANDATORY_COOLDOWN:
            # 强制冷却期：高依赖用户强制降级
            for consumer in target_consumers:
                current_spin = network.get_node_spin(consumer.id)
                if current_spin >= 1:  # L4-L5用户
                    new_spin = max(-1, current_spin - params['forced_level_reduction'])
                    network.set_node_spin(consumer.id, new_spin)
                    effect['level_changes'].append((consumer.id, current_spin, new_spin))
                    effect['n_affected'] += 1
                    
        elif event.intervention_type == InterventionType.EDUCATION_CAMPAIGN:
            # 教育活动：提升决策质量，校准信任
            for consumer in target_consumers:
                if np.random.random() < event.intensity * 0.5:
                    # 向中间等级（L3）靠拢
                    current_spin = network.get_node_spin(consumer.id)
                    if current_spin > 0:
                        new_spin = max(0, current_spin - 1)
                    elif current_spin < 0:
                        new_spin = min(0, current_spin + 1)
                    else:
                        new_spin = current_spin
                    if new_spin != current_spin:
                        network.set_node_spin(consumer.id, new_spin)
                        effect['level_changes'].append((consumer.id, current_spin, new_spin))
                    effect['n_affected'] += 1
                    
        elif event.intervention_type == InterventionType.REGULATION_ENFORCEMENT:
            # 监管执法：设置信任下限
            for consumer in target_consumers:
                current_spin = network.get_node_spin(consumer.id)
                # 防止过度依赖（限制在L4以内）
                if current_spin == 2:  # L5
                    new_spin = 1  # 降到L4
                    network.set_node_spin(consumer.id, new_spin)
                    effect['level_changes'].append((consumer.id, current_spin, new_spin))
                    effect['n_affected'] += 1
        
        return effect
    
    def _select_target_consumers(self, consumers: List, target_group: str) -> List:
        """选择目标消费者群体"""
        if target_group == 'all':
            return consumers
        elif target_group == 'high_dependency':
            return [c for c in consumers if c.dependency_level >= 4]
        elif target_group == 'low_dependency':
            return [c for c in consumers if c.dependency_level <= 2]
        else:
            return consumers
    
    def _update_active_interventions(self, step: int, consumers: List):
        """更新活跃干预的效果（衰减）"""
        expired = []
        for event in self.active_interventions:
            if step > event.timing + event.duration:
                expired.append(event)
        
        for event in expired:
            self.active_interventions.remove(event)
    
    def get_intervention_summary(self) -> Dict:
        """获取干预效果汇总"""
        return {
            'total_interventions': len(self.intervention_history),
            'intervention_breakdown': {
                itype.value: sum(1 for e in self.intervention_history if e.intervention_type == itype)
                for itype in InterventionType
            },
            'total_consumers_affected': sum(
                e.get('consumers_affected', 0) for e in self.intervention_effects.values()
            ),
            'intervention_history': [
                {
                    'type': e.intervention_type.value,
                    'timing': e.timing,
                    'intensity': e.intensity,
                    'target': e.target_group
                }
                for e in self.intervention_history
            ]
        }


class InterventionPolicyOptimizer:
    """干预政策优化器"""
    
    def __init__(self):
        """初始化优化器"""
        self.scenarios = []
        
    def generate_optimal_schedule(self, 
                                  n_steps: int,
                                  target_outcome: str = 'balanced') -> List[InterventionEvent]:
        """
        生成最优干预时间表
        
        Args:
            n_steps: 总仿真步数
            target_outcome: 目标结果 ('balanced', 'promote_ai', 'protect_consumers')
            
        Returns:
            干预事件列表
        """
        schedule = []
        
        if target_outcome == 'balanced':
            # 平衡策略：早期教育 + 中期监管 + 晚期灵活
            schedule.append(InterventionEvent(
                intervention_type=InterventionType.EDUCATION_CAMPAIGN,
                timing=int(n_steps * 0.1),
                intensity=0.6,
                duration=30,
                target_group='all'
            ))
            schedule.append(InterventionEvent(
                intervention_type=InterventionType.REGULATION_ENFORCEMENT,
                timing=int(n_steps * 0.5),
                intensity=0.5,
                duration=50,
                target_group='high_dependency'
            ))
            
        elif target_outcome == 'promote_ai':
            # 促进AI采用
            schedule.append(InterventionEvent(
                intervention_type=InterventionType.POSITIVE_PUBLICITY,
                timing=int(n_steps * 0.15),
                intensity=0.7,
                duration=40,
                target_group='all'
            ))
            
        elif target_outcome == 'protect_consumers':
            # 保护消费者
            schedule.append(InterventionEvent(
                intervention_type=InterventionType.MANDATORY_COOLDOWN,
                timing=int(n_steps * 0.3),
                intensity=0.8,
                duration=20,
                target_group='high_dependency'
            ))
            schedule.append(InterventionEvent(
                intervention_type=InterventionType.NEGATIVE_EXPOSURE,
                timing=int(n_steps * 0.6),
                intensity=0.5,
                duration=25,
                target_group='all'
            ))
        
        return schedule
