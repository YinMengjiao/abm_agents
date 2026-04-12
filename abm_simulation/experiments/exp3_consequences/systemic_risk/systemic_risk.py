"""
实验10: 系统性风险与级联失效
AI系统故障的社会传染效应
"""

import numpy as np
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class FailureType(Enum):
    """故障类型"""
    TECHNICAL_OUTAGE = "technical_outage"      # 技术故障停机
    DATA_BREACH = "data_breach"                # 数据泄露
    ALGORITHM_BIAS = "algorithm_bias"          # 算法偏见暴露
    SERVICE_DEGRADATION = "service_degradation"  # 服务质量下降
    COORDINATED_ATTACK = "coordinated_attack"  # 协调攻击


class FailureSeverity(Enum):
    """故障严重程度"""
    MINOR = 1          # 轻微
    MODERATE = 2       # 中等
    MAJOR = 3          # 严重
    CRITICAL = 4       # 致命


@dataclass
class FailureEvent:
    """故障事件"""
    event_id: int
    failure_type: FailureType
    severity: FailureSeverity
    timestamp: int
    affected_consumers: Set[int] = field(default_factory=set)
    propagation_steps: int = 0
    recovery_time: int = 0


class SystemicRiskModel:
    """
    系统性风险模型
    
    模拟AI系统故障的传播和恢复
    """
    
    def __init__(self, 
                 n_consumers: int = 500,
                 network_adjacency: Optional[np.ndarray] = None):
        """
        初始化风险模型
        
        Args:
            n_consumers: 消费者数量
            network_adjacency: 网络邻接矩阵
        """
        self.n_consumers = n_consumers
        self.network = network_adjacency
        
        # 消费者状态
        self.consumer_trust: np.ndarray = np.random.beta(3, 3, n_consumers)
        self.consumer_dependency: np.ndarray = np.random.choice(
            [1, 2, 3, 4, 5], n_consumers, p=[0.15, 0.20, 0.30, 0.25, 0.10]
        )
        
        # 故障历史
        self.failure_history: List[FailureEvent] = []
        self.trust_trajectory: List[np.ndarray] = []
        self.dependency_trajectory: List[np.ndarray] = []
        
        # 系统韧性指标
        self.recovery_metrics = {
            'trust_recovery_time': [],
            'dependency_recovery_time': [],
            'cascade_size': []
        }
    
    def trigger_failure(self,
                       failure_type: FailureType,
                       severity: FailureSeverity,
                       initial_affected: Optional[Set[int]] = None,
                       step: int = 0) -> FailureEvent:
        """
        触发故障事件
        
        Args:
            failure_type: 故障类型
            severity: 严重程度
            initial_affected: 初始受影响消费者
            step: 当前时间步
            
        Returns:
            故障事件
        """
        event_id = len(self.failure_history)
        
        if initial_affected is None:
            # 随机选择初始受影响者
            n_initial = max(1, int(self.n_consumers * 0.05 * severity.value))
            initial_affected = set(np.random.choice(self.n_consumers, n_initial, replace=False))
        
        event = FailureEvent(
            event_id=event_id,
            failure_type=failure_type,
            severity=severity,
            timestamp=step,
            affected_consumers=initial_affected.copy()
        )
        
        # 应用初始冲击
        self._apply_failure_impact(event, initial_affected)
        
        self.failure_history.append(event)
        return event
    
    def _apply_failure_impact(self, event: FailureEvent, affected: Set[int]):
        """应用故障影响"""
        severity_multiplier = event.severity.value * 0.2
        
        for consumer_id in affected:
            # 信任度下降
            trust_drop = np.random.uniform(0.1, 0.3) * severity_multiplier
            self.consumer_trust[consumer_id] = max(0, self.consumer_trust[consumer_id] - trust_drop)
            
            # 依赖等级可能下降
            if np.random.random() < 0.3 * event.severity.value:
                self.consumer_dependency[consumer_id] = max(
                    1, self.consumer_dependency[consumer_id] - 1
                )
    
    def propagate_failure(self, event: FailureEvent, step: int) -> Set[int]:
        """
        传播故障
        
        Args:
            event: 故障事件
            step: 当前时间步
            
        Returns:
            新受影响的消费者
        """
        if event.propagation_steps >= 3:  # 最大传播步数
            return set()
        
        newly_affected = set()
        
        # 社会影响传播
        for affected_id in list(event.affected_consumers):
            # 获取邻居
            if self.network is not None:
                neighbors = np.where(self.network[affected_id] > 0)[0]
            else:
                # 随机邻居
                neighbors = np.random.choice(self.n_consumers, 5, replace=False)
            
            for neighbor in neighbors:
                if neighbor not in event.affected_consumers:
                    # 传播概率取决于依赖等级和信任度
                    dep_factor = self.consumer_dependency[neighbor] / 5.0
                    trust_factor = 1 - self.consumer_trust[neighbor]
                    propagation_prob = 0.1 * event.severity.value * dep_factor * trust_factor
                    
                    if np.random.random() < propagation_prob:
                        newly_affected.add(neighbor)
        
        # 应用新影响
        if newly_affected:
            self._apply_failure_impact(event, newly_affected)
            event.affected_consumers.update(newly_affected)
            event.propagation_steps += 1
        
        return newly_affected
    
    def system_recovery(self, event: FailureEvent, step: int):
        """
        系统恢复
        
        Args:
            event: 故障事件
            step: 当前时间步
        """
        time_since_failure = step - event.timestamp
        
        # 恢复速率
        recovery_rate = 0.05 / event.severity.value
        
        for consumer_id in event.affected_consumers:
            # 信任度缓慢恢复
            self.consumer_trust[consumer_id] = min(
                1.0, self.consumer_trust[consumer_id] + recovery_rate
            )
            
            # 依赖等级可能恢复（较慢）
            if np.random.random() < recovery_rate * 0.1:
                self.consumer_dependency[consumer_id] = min(
                    5, self.consumer_dependency[consumer_id] + 1
                )
        
        # 检查是否完全恢复
        if time_since_failure > 50:  # 假设50步后基本恢复
            avg_trust = np.mean(self.consumer_trust)
            if avg_trust > 0.6:
                event.recovery_time = time_since_failure
    
    def run_crisis_simulation(self,
                             failure_type: FailureType = FailureType.TECHNICAL_OUTAGE,
                             severity: FailureSeverity = FailureSeverity.MAJOR,
                             n_steps: int = 200) -> Dict:
        """
        运行危机仿真
        
        Args:
            failure_type: 故障类型
            severity: 严重程度
            n_steps: 仿真步数
            
        Returns:
            仿真结果
        """
        # 初始状态
        initial_trust = self.consumer_trust.copy()
        initial_dependency = self.consumer_dependency.copy()
        
        # 在50步时触发故障
        failure_step = 50
        event = None
        
        for step in range(n_steps):
            # 记录轨迹
            self.trust_trajectory.append(self.consumer_trust.copy())
            self.dependency_trajectory.append(self.consumer_dependency.copy())
            
            # 触发故障
            if step == failure_step:
                event = self.trigger_failure(failure_type, severity, step=step)
                print(f"  步{step}: 触发{failure_type.value}故障 (严重度: {severity.name})")
            
            # 传播故障
            if event and step > failure_step and step < failure_step + 20:
                new_affected = self.propagate_failure(event, step)
                if new_affected:
                    print(f"  步{step}: 故障传播至{len(new_affected)}个新消费者")
            
            # 恢复
            if event and step > failure_step:
                self.system_recovery(event, step)
        
        # 计算结果
        final_trust = self.consumer_trust
        final_dependency = self.consumer_dependency
        
        return {
            'failure_event': event,
            'initial_avg_trust': np.mean(initial_trust),
            'final_avg_trust': np.mean(final_trust),
            'trust_drop': np.mean(initial_trust) - np.mean(final_trust),
            'initial_avg_dependency': np.mean(initial_dependency),
            'final_avg_dependency': np.mean(final_dependency),
            'max_affected': len(event.affected_consumers) if event else 0,
            'recovery_time': event.recovery_time if event else 0,
            'trust_trajectory': self.trust_trajectory,
            'dependency_trajectory': self.dependency_trajectory
        }
    
    def calculate_systemic_risk_metrics(self) -> Dict:
        """计算系统性风险指标"""
        if not self.failure_history:
            return {}
        
        total_affected = sum(len(e.affected_consumers) for e in self.failure_history)
        avg_cascade_size = total_affected / len(self.failure_history)
        
        # 系统韧性
        if self.trust_trajectory:
            initial_trust = np.mean(self.trust_trajectory[0])
            min_trust = min(np.mean(t) for t in self.trust_trajectory)
            final_trust = np.mean(self.trust_trajectory[-1])
            
            resilience = (final_trust - min_trust) / (initial_trust - min_trust + 0.001)
        else:
            resilience = 0
        
        return {
            'n_failures': len(self.failure_history),
            'avg_cascade_size': avg_cascade_size,
            'max_cascade_size': max(len(e.affected_consumers) for e in self.failure_history),
            'system_resilience': resilience,
            'avg_recovery_time': np.mean([e.recovery_time for e in self.failure_history if e.recovery_time > 0]) if any(e.recovery_time > 0 for e in self.failure_history) else 0
        }


class StressTestScenarios:
    """压力测试场景"""
    
    def __init__(self, risk_model: SystemicRiskModel):
        """
        初始化压力测试
        
        Args:
            risk_model: 风险模型
        """
        self.risk_model = risk_model
    
    def run_all_scenarios(self) -> Dict:
        """运行所有压力测试场景"""
        scenarios = {
            'minor_outage': (FailureType.TECHNICAL_OUTAGE, FailureSeverity.MINOR),
            'major_breach': (FailureType.DATA_BREACH, FailureSeverity.MAJOR),
            'critical_failure': (FailureType.TECHNICAL_OUTAGE, FailureSeverity.CRITICAL),
            'coordinated_attack': (FailureType.COORDINATED_ATTACK, FailureSeverity.CRITICAL),
        }
        
        results = {}
        
        for scenario_name, (failure_type, severity) in scenarios.items():
            print(f"\n  运行场景: {scenario_name}")
            
            # 重置模型状态
            self.risk_model.consumer_trust = np.random.beta(3, 3, self.risk_model.n_consumers)
            self.risk_model.consumer_dependency = np.random.choice(
                [1, 2, 3, 4, 5], self.risk_model.n_consumers, 
                p=[0.15, 0.20, 0.30, 0.25, 0.10]
            )
            self.risk_model.failure_history = []
            self.risk_model.trust_trajectory = []
            self.risk_model.dependency_trajectory = []
            
            # 运行仿真
            result = self.risk_model.run_crisis_simulation(
                failure_type=failure_type,
                severity=severity,
                n_steps=200
            )
            
            results[scenario_name] = result
        
        return results
