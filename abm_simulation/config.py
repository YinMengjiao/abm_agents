"""
统一输出路径配置
所有实验结果集中存储到 abm_simulation/results/ 下各自子目录
"""
import os

# 项目根目录（即本文件所在的 abm_simulation/ 目录）
_HERE = os.path.dirname(os.path.abspath(__file__))

# 所有实验结果的统一输出根目录
RESULTS_ROOT = os.path.join(_HERE, "results")

# 各实验的输出目录（由 run_*.py 引用，不要在 visualization_*.py 里硬编码路径）
RESULTS = {
    "exp1":        os.path.join(RESULTS_ROOT, "exp1_baseline"),
    "exp2":        os.path.join(RESULTS_ROOT, "exp2_mechanism"),
    "exp3_bubble": os.path.join(RESULTS_ROOT, "exp3_consequences", "filter_bubble"),
    "exp3_risk":   os.path.join(RESULTS_ROOT, "exp3_consequences", "systemic_risk"),
    "exp4":        os.path.join(RESULTS_ROOT, "exp4_intervention"),
}
