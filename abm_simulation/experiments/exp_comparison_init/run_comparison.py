"""
实验对比：调查数据驱动 vs 理论假设初始化
研究问题：使用真实调查数据初始化仿真，是否会显著改变系统演化轨迹？

实验设计：
- 实验组：使用ACDDS问卷得到的L1-L5真实分布
- 对照组：使用理论对称分布（L1=10%, L2=25%, L3=30%, L4=25%, L5=10%）
- 保持其他所有参数一致，运行多次取平均
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from simulation import ABMSimulation, SimulationConfig
import json
from datetime import datetime


class InitializationComparisonExperiment:
    """初始化方式对比实验"""
    
    def __init__(self, n_runs: int = 10, n_steps: int = 200, n_consumers: int = 500):
        """
        初始化对比实验
        
        Args:
            n_runs: 每组重复实验次数
            n_steps: 每次仿真步数
            n_consumers: 消费者数量
        """
        self.n_runs = n_runs
        self.n_steps = n_steps
        self.n_consumers = n_consumers
        
        # 加载两种分布
        # 实验组：使用带人口统计信息的真实调查数据
        self.survey_dist = SimulationConfig.load_survey_distribution(with_demographics=True)
        # 对照组：使用理论对称分布
        self.theoretical_dist = {1: 0.10, 2: 0.25, 3: 0.30, 4: 0.25, 5: 0.10}
        
        # 存储结果
        self.results_survey = []
        self.results_theoretical = []
        
    def run_single_simulation(self, dist: dict, seed: int) -> dict:
        """
        运行单次仿真
        
        Args:
            dist: 初始等级分布
            seed: 随机种子
            
        Returns:
            仿真结果字典
        """
        np.random.seed(seed)
        
        config = SimulationConfig(
            n_consumers=self.n_consumers,
            n_merchants=20,
            n_ai_agents=3,
            network_type='small_world',
            n_steps=self.n_steps,
            initial_coupling=0.25,
            initial_temperature=1.5,
            enable_adaptive_coupling=True,
            coupling_trend=0.0008,
            shock_probability=0.03,
            initial_level_distribution=dist,
            enable_ai_learning=False  # 基准实验禁用AI学习
        )
        
        sim = ABMSimulation(config)
        sim.run()
        summary = sim.get_summary_statistics()
        
        # 提取关键指标
        result = {
            'seed': seed,
            'initial_distribution': dist,
            'final_distribution': summary['final_level_distribution'],
            'magnetization_initial': summary['magnetization_trend']['initial'],
            'magnetization_final': summary['magnetization_trend']['final'],
            'magnetization_change': summary['magnetization_trend']['change'],
            'avg_satisfaction': summary['satisfaction']['mean'],
            'ai_usage_rate': summary['ai_usage'],
            'error_rate': summary['error_rate'],
            'avg_clustering': summary['network_metrics'].get('avg_clustering', 0),
            'avg_path_length': summary['network_metrics'].get('avg_path_length', 0),
        }
        
        # 提取演化历史（每10步采样）
        if sim.metrics_history:
            result['level_evolution'] = {
                level: [m.level_distribution.get(level, 0) 
                       for m in sim.metrics_history[::10]]
                for level in range(1, 6)
            }
            result['magnetization_evolution'] = [
                m.magnetization for m in sim.metrics_history[::10]
            ]
            result['satisfaction_evolution'] = [
                m.avg_satisfaction for m in sim.metrics_history[::10]
            ]
        
        return result
    
    def run_comparison(self):
        """运行完整对比实验"""
        print("="*70)
        print("实验对比：调查数据驱动 vs 理论假设初始化")
        print("="*70)
        
        print(f"\n【实验参数】")
        print(f"  重复次数: {self.n_runs}")
        print(f"  仿真步数: {self.n_steps}")
        print(f"  消费者数: {self.n_consumers}")
        
        print(f"\n【实验组 - 调查数据分布】")
        for level in range(1, 6):
            print(f"    L{level}: {self.survey_dist[level]*100:.1f}%")
        
        print(f"\n【对照组 - 理论假设分布】")
        for level in range(1, 6):
            print(f"    L{level}: {self.theoretical_dist[level]*100:.1f}%")
        
        # 运行实验组
        print(f"\n{'='*70}")
        print(f"运行实验组（调查数据）")
        print(f"{'='*70}")
        
        for i in range(self.n_runs):
            seed = i * 42 + 7
            print(f"  [{i+1}/{self.n_runs}] seed={seed}...", end=' ')
            result = self.run_single_simulation(self.survey_dist, seed)
            self.results_survey.append(result)
            print(f"M={result['magnetization_final']:.3f}, Sat={result['avg_satisfaction']:.3f}")
        
        # 运行对照组
        print(f"\n{'='*70}")
        print(f"运行对照组（理论假设）")
        print(f"{'='*70}")
        
        for i in range(self.n_runs):
            seed = i * 42 + 7  # 使用相同种子确保可比性
            print(f"  [{i+1}/{self.n_runs}] seed={seed}...", end=' ')
            result = self.run_single_simulation(self.theoretical_dist, seed)
            self.results_theoretical.append(result)
            print(f"M={result['magnetization_final']:.3f}, Sat={result['avg_satisfaction']:.3f}")
        
        # 统计分析
        self.analyze_results()
        
        return {
            'survey': self.results_survey,
            'theoretical': self.results_theoretical
        }
    
    def analyze_results(self):
        """统计分析结果"""
        print(f"\n{'='*70}")
        print(f"统计分析")
        print(f"{'='*70}")
        
        # 提取关键指标
        metrics = ['magnetization_final', 'avg_satisfaction', 'ai_usage_rate', 'error_rate']
        metric_names = {
            'magnetization_final': '最终磁化强度',
            'avg_satisfaction': '平均满意度',
            'ai_usage_rate': 'AI使用率',
            'error_rate': '错误率'
        }
        
        print(f"\n{'指标':<15} {'调查数据':<20} {'理论假设':<20} {'差异':<15}")
        print("-"*70)
        
        for metric in metrics:
            survey_vals = [r[metric] for r in self.results_survey]
            theoretical_vals = [r[metric] for r in self.results_theoretical]
            
            survey_mean = np.mean(survey_vals)
            survey_std = np.std(survey_vals)
            theoretical_mean = np.mean(theoretical_vals)
            theoretical_std = np.std(theoretical_vals)
            diff = survey_mean - theoretical_mean
            
            print(f"{metric_names[metric]:<15} "
                  f"{survey_mean:.4f}±{survey_std:.4f}  "
                  f"{theoretical_mean:.4f}±{theoretical_std:.4f}  "
                  f"{diff:+.4f}")
        
        # 等级分布对比
        print(f"\n【最终等级分布对比】")
        print(f"{'等级':<10} {'调查数据':<15} {'理论假设':<15} {'差异':<10}")
        print("-"*50)
        
        for level in range(1, 6):
            survey_counts = [r['final_distribution'].get(level, 0) for r in self.results_survey]
            theoretical_counts = [r['final_distribution'].get(level, 0) for r in self.results_theoretical]
            
            survey_mean = np.mean(survey_counts)
            theoretical_mean = np.mean(theoretical_counts)
            diff = survey_mean - theoretical_mean
            
            print(f"L{level:<9} {survey_mean:.1f}  "
                  f"{theoretical_mean:.1f}  "
                  f"{diff:+.1f}")
    
    def save_results(self, output_dir: str = None):
        """保存实验结果"""
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'results')
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 转换numpy类型为Python原生类型
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {str(k): convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif isinstance(obj, (np.integer,)):
                return int(obj)
            elif isinstance(obj, (np.floating,)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj
        
        # 保存JSON结果
        results = {
            'experiment': 'initialization_comparison',
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'n_runs': self.n_runs,
                'n_steps': self.n_steps,
                'n_consumers': self.n_consumers,
                'survey_distribution': self.survey_dist,
                'theoretical_distribution': self.theoretical_dist
            },
            'results_survey': convert_numpy_types(self.results_survey),
            'results_theoretical': convert_numpy_types(self.results_theoretical)
        }
        
        json_path = os.path.join(output_dir, 'comparison_results.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 结果已保存: {json_path}")
        return output_dir


def main():
    """主函数"""
    # 创建实验
    exp = InitializationComparisonExperiment(
        n_runs=10,        # 10次重复
        n_steps=200,      # 200步
        n_consumers=500   # 500个消费者
    )
    
    # 运行对比实验
    results = exp.run_comparison()
    
    # 保存结果
    output_dir = exp.save_results()
    
    print(f"\n{'='*70}")
    print(f"对比实验完成！")
    print(f"{'='*70}")
    print(f"下一步: 运行 visualization_comparison.py 生成对比图表")
    
    return results


if __name__ == "__main__":
    main()
