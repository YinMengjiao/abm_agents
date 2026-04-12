"""
ABM仿真主引擎
整合Ising-D-I-B模型的完整仿真系统
"""

import numpy as np
import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.ising_network import IsingSocialNetwork, AdaptiveIsingNetwork
from agents.consumer_dib import ConsumerAgentDIB, ConsumerTraits
from agents.ai_agent import AIAgentPopulation, AIAgent
from environment.market import MarketEnvironment, SimulationContext, ProductCategory


@dataclass
class SimulationConfig:
    """仿真配置"""
    # 规模参数
    n_consumers: int = 1000
    n_merchants: int = 20
    n_ai_agents: int = 3
    
    # 网络参数
    network_type: str = 'small_world'
    initial_coupling: float = 0.5
    initial_temperature: float = 1.0
    
    # 仿真参数
    n_steps: int = 500
    burn_in_steps: int = 50
    
    # 初始分布
    initial_level_distribution: Dict[int, float] = field(default_factory=lambda: {
        1: 0.10,  # L1: 10%
        2: 0.25,  # L2: 25%
        3: 0.30,  # L3: 30%
        4: 0.25,  # L4: 25%
        5: 0.10,  # L5: 10%
    })
    
    # 动态参数
    enable_adaptive_coupling: bool = True
    coupling_trend: float = 0.001  # 每步社会耦合增长
    shock_probability: float = 0.01  # 外部冲击概率
    
    # AI学习控制(基准实验应禁用)
    enable_ai_learning: bool = True  # 是否允许AI从反馈学习
    
        
    @staticmethod
    def load_survey_distribution(csv_path: str = None, with_demographics: bool = False) -> Dict[int, float]:
        """
        从ACDDS调查数据加载真实的L1-L5分布（数据驱动初始化）
            
        Args:
            csv_path: CSV文件路径，默认自动查找
            with_demographics: 是否使用带人口统计信息的数据文件
                
        Returns:
            等级分布字典 {1: 比例, 2: 比例, ..., 5: 比例}
        """
        import pandas as pd
            
        if csv_path is None:
            _here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if with_demographics:
                csv_path = os.path.join(_here, 'data_survey', 'acdds_with_demographics.csv')
            else:
                csv_path = os.path.join(_here, 'data_survey', 'acdds_results.csv')
            
        if not os.path.exists(csv_path):
            print(f"⚠ 警告: 调查数据文件不存在: {csv_path}")
            print("  使用默认理论分布")
            return {1: 0.10, 2: 0.25, 3: 0.30, 4: 0.25, 5: 0.10}
            
        df = pd.read_csv(csv_path)
        
        # 检查是否包含人口统计信息
        has_demographics = '性别' in df.columns or '性别' in df.columns or 'gender' in df.columns.lower()
        
        # 计算L1-L5分布
        if 'Dependency_Level' in df.columns:
            # 原始格式：使用Dependency_Level列
            level_counts = df['Dependency_Level'].value_counts().sort_index()
            total = len(df)
            level_map = {'L1': 1, 'L2': 2, 'L3': 3, 'L4': 4, 'L5': 5}
            distribution = {}
            
            for level_name, count in level_counts.items():
                level_num = level_map.get(level_name, 3)
                distribution[level_num] = count / total
        else:
            # 新格式：需要根据ACDDS题目计算依赖等级
            # 这里简化处理：使用前几个题目的平均值作为代理
            # 实际应该根据完整的评分逻辑计算
            # 为简单起见，我们使用一个合理的假设分布
            print(f"ℹ️  使用带人口统计信息的数据，基于题目计算依赖等级...")
            total = len(df)
            # 使用简化的启发式方法：基于PU（感知有用性）和TR（信任）的平均值
            pu_cols = [col for col in df.columns if col.startswith('PU')]
            tr_cols = [col for col in df.columns if col.startswith('TR')]
            
            if pu_cols and tr_cols:
                df['_pu_avg'] = df[pu_cols].mean(axis=1)
                df['_tr_avg'] = df[tr_cols].mean(axis=1)
                df['_dependency_score'] = (df['_pu_avg'] + df['_tr_avg']) / 2
                
                # 根据得分划分等级（1-7分量表）
                # L1: 1-2.5, L2: 2.5-3.5, L3: 3.5-4.5, L4: 4.5-5.5, L5: 5.5-7
                bins = [0, 2.5, 3.5, 4.5, 5.5, 8]
                labels = [1, 2, 3, 4, 5]
                df['_level'] = pd.cut(df['_dependency_score'], bins=bins, labels=labels, include_lowest=True)
                level_counts = df['_level'].value_counts().sort_index()
                distribution = {}
                for level_num in range(1, 6):
                    distribution[level_num] = level_counts.get(level_num, 0) / total
            else:
                # 如果无法计算，使用默认分布
                distribution = {1: 0.10, 2: 0.25, 3: 0.30, 4: 0.25, 5: 0.10}
        
        for i in range(1, 6):
            if i not in distribution:
                distribution[i] = 0.0
        
        print("="*70)
        if has_demographics:
            print("📊 已加载ACDDS调查数据（含人口统计信息 - 数据驱动的仿真初始化）")
        else:
            print("📊 已加载ACDDS调查数据（数据驱动的仿真初始化）")
        print("="*70)
        print(f"样本总量: N={total}")
        if has_demographics:
            # 显示人口统计信息摘要
            if '性别' in df.columns:
                gender_dist = df['性别'].value_counts()
                print(f"\n性别分布:")
                for gender, count in gender_dist.items():
                    print(f"  {gender}: {count} ({count/total*100:.1f}%)")
            if '年龄' in df.columns:
                print(f"\n年龄分布:")
                print(f"  平均年龄: {df['年龄'].mean():.1f}岁")
                print(f"  年龄范围: {df['年龄'].min()}-{df['年龄'].max()}岁")
            if '受教育程度' in df.columns:
                edu_dist = df['受教育程度'].value_counts()
                print(f"\n受教育程度分布:")
                for edu, count in edu_dist.items():
                    print(f"  {edu}: {count} ({count/total*100:.1f}%)")
        print(f"\n依赖等级分布:")
        level_names = {1: 'L1完全自主', 2: 'L2信息辅助', 3: 'L3半委托', 
                      4: 'L4高度依赖', 5: 'L5完全代理'}
        for level in range(1, 6):
            count = int(distribution[level] * total)
            pct = distribution[level] * 100
            bar = '█' * int(pct / 2)
            print(f"  {level_names[level]:<12}: {count:>4} ({pct:5.1f}%) {bar}")
        print("="*70)
            
        return distribution
        
    @staticmethod
    def get_user_input_distribution() -> Dict[int, float]:
        """从用户输入获取初始人群比例分布"""
        print("\n" + "="*60)
        print("请输入初始人群依赖等级分布 (L1-L5)")
        print("="*60)
        print("\n说明:")
        print("  L1: 极低 AI 依赖群体")
        print("  L2: 低 AI 依赖群体")
        print("  L3: 中等 AI 依赖群体")
        print("  L4: 高 AI 依赖群体")
        print("  L5: 极高 AI 依赖群体")
        print("\n要求:")
        print("  1. 每个等级的比例用小数表示 (如 0.2 表示 20%)")
        print("  2. 所有比例之和必须等于 1.0")
        print("  3. 直接回车使用默认值")
        print("="*60)
        
        default_dist = {1: 0.10, 2: 0.25, 3: 0.30, 4: 0.25, 5: 0.10}
        
        try:
            print("\n默认分布:")
            for level, ratio in default_dist.items():
                print(f"  L{level}: {ratio*100:.0f}%")
            
            print("\n是否使用默认分布？(Y/n): ", end='')
            use_default = input().strip().lower()
            
            if use_default == '' or use_default == 'y':
                print("\n 使用默认分布")
                return default_dist
            
            print("\n请依次输入各等级比例:")
            user_dist = {}
            for level in range(1, 6):
                prompt = f"  L{level} 比例 (默认{default_dist[level]*100:.0f}%): "
                user_input = input(prompt).strip()
                
                if user_input == '':
                    user_dist[level] = default_dist[level]
                else:
                    user_dist[level] = float(user_input)
            
            total = sum(user_dist.values())
            print(f"\n输入汇总：总和 = {total:.4f}")
            
            if abs(total - 1.0) > 0.001:
                print(f"警告：比例之和 ({total:.4f}) 不等于 1.0")
                print("是否自动归一化？(Y/n): ", end='')
                normalize = input().strip().lower()
                
                if normalize == '' or normalize == 'y':
                    user_dist = {k: v/total for k, v in user_dist.items()}
                    print(f"已归一化到总和为 1.0")
                else:
                    print("请重新调整比例后再次运行程序")
                    return default_dist
            
            print("\n最终使用的分布:")
            for level, ratio in sorted(user_dist.items()):
                print(f"  L{level}: {ratio*100:.2f}%")
            
            return user_dist
            
        except KeyboardInterrupt:
            print("\n\n用户中断，使用默认分布")
            return default_dist
        except Exception as e:
            print(f"\n输入错误：{e}，使用默认分布")
            return default_dist

@dataclass
class SimulationMetrics:
    """仿真指标记录"""
    step: int = 0
    
    # 依赖等级分布
    level_distribution: Dict[int, int] = field(default_factory=dict)
    magnetization: float = 0.0
    
    # 系统指标
    avg_satisfaction: float = 0.0
    avg_decision_time: float = 0.0
    ai_usage_rate: float = 0.0
    error_rate: float = 0.0
    
    # Ising指标
    coupling_strength: float = 0.0
    temperature: float = 0.0
    susceptibility: float = 0.0
    
    # AI指标
    ai_error_rate: float = 0.0
    ai_satisfaction_impact: float = 0.0


class ABMSimulation:
    """
    ABM仿真主类
    
    整合Ising社交网络、D-I-B消费者、AI代理和市场环境
    """
    
    def __init__(self, config: Optional[SimulationConfig] = None, interactive: bool = False):
        """
        初始化仿真
        
        Args:
            config: 仿真配置对象
            interactive: 是否启用交互式配置（手动输入初始分布）
        """
        if config is None:
            if interactive:
                # 交互式获取用户输入
                dist = SimulationConfig.get_user_input_distribution()
                self.config = SimulationConfig(initial_level_distribution=dist)
            else:
                self.config = SimulationConfig()
        else:
            self.config = config
        
        # 初始化组件
        self.network: Optional[AdaptiveIsingNetwork] = None
        self.consumers: List[ConsumerAgentDIB] = []
        self.ai_population: Optional[AIAgentPopulation] = None
        self.market: Optional[MarketEnvironment] = None
        self.context: Optional[SimulationContext] = None
        
        # 历史记录
        self.metrics_history: List[SimulationMetrics] = []
        self.step_count = 0
        
        # 是否已初始化
        self._initialized = False
    
    def initialize(self):
        """初始化仿真组件"""
        print("初始化仿真...")
        
        # 1. 创建Ising社交网络
        self.network = AdaptiveIsingNetwork(
            n_agents=self.config.n_consumers,
            network_type=self.config.network_type,
            coupling_strength=self.config.initial_coupling,
            temperature=self.config.initial_temperature
        )
        
        # 2. 初始化自旋（依赖等级）
        levels = self._sample_initial_levels()
        self.network.initialize_spins(levels)
        
        # 3. 设置外场（个体倾向）
        external_fields = self._generate_external_fields()
        self.network.set_external_fields(external_fields)
        
        # 4. 创建消费者智能体
        self.consumers = []
        for i in range(self.config.n_consumers):
            traits = ConsumerTraits(
                tech_acceptance=np.random.beta(2, 2),
                trust_tendency=np.random.beta(2, 2),
                privacy_concern=np.random.beta(2, 2),
                control_need=np.random.beta(2, 2),
                cognitive_laziness=np.random.beta(2, 2),
                social_conformity=np.random.beta(2, 2),
                risk_aversion=np.random.beta(2, 2),
            )
            
            consumer = ConsumerAgentDIB(
                agent_id=i,
                initial_level=levels[i],
                traits=traits
            )
            self.consumers.append(consumer)
        
        # 5. 创建AI代理群体(根据配置决定是否启用学习)
        self.ai_population = AIAgentPopulation(
            n_agents=self.config.n_ai_agents,
            enable_learning=self.config.enable_ai_learning
        )
        
        # 6. 创建市场环境
        self.market = MarketEnvironment(
            n_merchants=self.config.n_merchants,
            market_condition='normal'
        )
        
        # 7. 创建仿真上下文
        self.context = SimulationContext()
        
        self._initialized = True
        print(f"初始化完成: {self.config.n_consumers}消费者, {self.config.n_merchants}商家, {self.config.n_ai_agents}AI代理")
        
        # 记录初始状态
        self._record_metrics()
    
    def _sample_initial_levels(self) -> List[int]:
        """根据分布采样初始依赖等级"""
        levels = []
        dist = self.config.initial_level_distribution
        for level, prob in dist.items():
            n = int(prob * self.config.n_consumers)
            levels.extend([level] * n)
        
        # 补齐或截断
        while len(levels) < self.config.n_consumers:
            levels.append(3)
        levels = levels[:self.config.n_consumers]
        
        np.random.shuffle(levels)
        return levels
    
    def _generate_external_fields(self) -> np.ndarray:
        """生成外场（个体固有倾向）"""
        # 外场保持中性，让Ising动力学和社会影响主导演化
        # 个体差异为主，避免强偏向导致极化
        fields = np.random.normal(0, 0.5, self.config.n_consumers)
        return fields
    
    def step(self) -> SimulationMetrics:
        """
        执行单步仿真
        
        流程：
        1. Ising网络更新（社会影响）
        2. 消费者D-I-B决策
        3. AI代理交互
        4. 市场交易
        5. 反馈与更新
        """
        if not self._initialized:
            raise RuntimeError("仿真未初始化，请先调用initialize()")
        
        self.step_count += 1
        self.context.step = self.step_count
        
        # 1. Ising网络更新（社会影响传播）
        self._update_ising_network()
        
        # 2. 消费者决策循环（随机打乱顺序避免位置偏差）
        consumer_indices = np.random.permutation(len(self.consumers))
        for idx in consumer_indices:
            consumer = self.consumers[idx]
            self._consumer_decision_cycle(consumer, idx)
        
        # 3. 更新环境
        self.context.advance_time(hours=0.5)
        
        # 4. 动态调整系统参数
        if self.config.enable_adaptive_coupling:
            self._update_system_parameters()
        
        # 5. 记录指标
        metrics = self._record_metrics()
        
        return metrics
    
    def _update_ising_network(self):
        """更新Ising网络"""
        # Monte Carlo更新
        self.network.monte_carlo_step(update_type='random')
        
        # 无条件将网络自旋同步到消费者，确保两者状态一致
        for i, consumer in enumerate(self.consumers):
            new_spin = self.network.spins[i]
            social_field = self.network.calculate_local_field(i)
            consumer.update_from_ising(new_spin, social_field, self.network.T)
    
    def _consumer_decision_cycle(self, consumer: ConsumerAgentDIB, agent_idx: int):
        """
        消费者D-I-B决策循环
        """
        # 获取上下文
        context = self.context.get_consumer_context(consumer.id)
        
        # 添加社交影响
        neighbor_spins = self.network.get_neighbor_levels(agent_idx)
        avg_neighbor_level = np.mean(neighbor_spins) if neighbor_spins else 3
        context['social_influence'] = (avg_neighbor_level - 3) / 2  # 归一化到[-1, 1]
        
        # D层：欲望形成
        desire = consumer.desire_formation(context)
        
        # I层：意图形成
        intention = consumer.intention_formation(desire, context)
        
        # 获取AI推荐
        ai_recommendation = None
        if intention.use_ai_probability > 0.5:
            ai_agent = self.ai_population.select_agent_for_consumer(consumer.id)
            available = self.market.get_available_options(n_options=20)
            ai_recommendation = ai_agent.make_recommendation(
                consumer.id, desire, available, consumer.dependency_level
            )
        
        # B层：行为执行
        alternatives = self.market.get_available_options(n_options=20)
        behavior = consumer.behavior_execution(intention, ai_recommendation, alternatives)
        
        # 市场交易
        if behavior.actual_choice:
            outcome = self.market.simulate_transaction(
                behavior.actual_choice,
                behavior.ai_involvement_level > 0,
                consumer.dependency_level
            )
            
            # 评估结果
            consumer.evaluate_outcome(outcome)
            
            # 记录经验
            consumer.record_experience(self.step_count, context)
            
            # AI学习更新
            if behavior.ai_involvement_level > 0 and ai_recommendation:
                ai_agent = self.ai_population.select_agent_for_consumer(consumer.id)
                ai_agent.update_from_interaction(consumer.id, {
                    'satisfaction': consumer.behavior.satisfaction,
                    'preferences': desire.__dict__,
                })
    
    def _update_system_parameters(self):
        """动态更新系统参数"""
        # 缓慢增加社会耦合（模拟AI技术扩散）
        shock = 0
        if np.random.random() < self.config.shock_probability:
            shock = np.random.normal(0, 0.1)
        
        self.network.update_parameters(
            J_trend=self.config.coupling_trend,
            shock_magnitude=shock
        )
    
    def _record_metrics(self) -> SimulationMetrics:
        """记录当前指标"""
        metrics = SimulationMetrics(step=self.step_count)
        
        # 依赖等级分布
        metrics.level_distribution = self.network.get_level_distribution()
        metrics.magnetization = self.network.get_magnetization()
        
        # 消费者统计
        satisfactions = [c.behavior.satisfaction for c in self.consumers]
        decision_times = [c.behavior.decision_time for c in self.consumers]
        ai_usage = [c.ai_usage_count for c in self.consumers]
        errors = [c.error_count for c in self.consumers]
        total_decisions = sum(c.total_decisions for c in self.consumers)
        
        metrics.avg_satisfaction = np.mean(satisfactions) if satisfactions else 0
        metrics.avg_decision_time = np.mean(decision_times) if decision_times else 0
        metrics.ai_usage_rate = sum(ai_usage) / max(1, total_decisions)
        metrics.error_rate = sum(errors) / max(1, total_decisions)
        
        # Ising指标
        metrics.coupling_strength = self.network.J
        metrics.temperature = self.network.T
        metrics.susceptibility = self.network.calculate_susceptibility()
        
        # AI指标
        ai_metrics = self.ai_population.get_collective_metrics()
        metrics.ai_error_rate = ai_metrics['collective_error_rate']
        
        self.metrics_history.append(metrics)
        return metrics
    
    def run(self, n_steps: Optional[int] = None) -> List[SimulationMetrics]:
        """
        运行完整仿真
        
        Args:
            n_steps: 仿真步数，None则使用配置值
        
        Returns:
            指标历史
        """
        if not self._initialized:
            self.initialize()
        
        steps = n_steps or self.config.n_steps
        
        print(f"\n开始仿真: {steps}步")
        print("-" * 50)
        
        for i in range(steps):
            self.step()
            
            # 进度输出
            if (i + 1) % 50 == 0:
                metrics = self.metrics_history[-1]
                print(f"Step {i+1}/{steps}: "
                      f"M={metrics.magnetization:.3f}, "
                      f"Sat={metrics.avg_satisfaction:.3f}, "
                      f"AI_use={metrics.ai_usage_rate:.3f}")
        
        print("-" * 50)
        print("仿真完成!")
        
        return self.metrics_history
    
    def get_summary_statistics(self) -> Dict:
        """获取汇总统计"""
        if not self.metrics_history:
            return {}
        
        final_metrics = self.metrics_history[-1]
        
        # 演化趋势
        magnetizations = [m.magnetization for m in self.metrics_history]
        satisfaction_trend = [m.avg_satisfaction for m in self.metrics_history]
        
        return {
            'final_level_distribution': final_metrics.level_distribution,
            'final_magnetization': final_metrics.magnetization,
            'magnetization_trend': {
                'initial': magnetizations[0],
                'final': magnetizations[-1],
                'change': magnetizations[-1] - magnetizations[0],
            },
            'satisfaction': {
                'mean': np.mean(satisfaction_trend),
                'final': satisfaction_trend[-1],
            },
            'ai_usage': final_metrics.ai_usage_rate,
            'error_rate': final_metrics.error_rate,
            'network_metrics': self.network.get_network_metrics() if self.network else {},
        }


def run_simulation_example():
    """运行示例仿真"""
    config = SimulationConfig(
        n_consumers=500,  # 小规模测试
        n_steps=200,
        initial_coupling=0.3,
        enable_adaptive_coupling=True,
        coupling_trend=0.002,
    )
    
    sim = ABMSimulation(config)
    sim.run()
    
    # 输出结果
    summary = sim.get_summary_statistics()
    print("\n=== 仿真结果汇总 ===")
    print(f"最终依赖等级分布: {summary['final_level_distribution']}")
    print(f"磁化强度变化: {summary['magnetization_trend']['initial']:.3f} -> {summary['magnetization_trend']['final']:.3f}")
    print(f"平均满意度: {summary['satisfaction']['mean']:.3f}")
    print(f"AI使用率: {summary['ai_usage']:.3f}")
    print(f"错误率: {summary['error_rate']:.3f}")
    
    return sim


if __name__ == "__main__":
    sim = run_simulation_example()
