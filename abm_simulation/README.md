# ABM 消费决策代理模拟系统

## 项目简介

本项目是一个基于 Agent-Based Modeling (ABM) 的消费决策代理模拟系统，用于研究消费者行为、AI 智能体与市场环境的交互作用。

## 核心模块

### 1. 智能体模块 (gents/)
- i_agent.py: AI 智能体实现
- consumer_dib.py: 基于 D-I-B 框架的消费者智能体

### 2. 环境模块 (environment/)
- market.py: 市场环境模拟

### 3. 模型模块 (models/)
- ising_network.py: Ising 网络模型

### 4. 实验模块 (experiments/)
包含多个子实验：
- aseline_exp1: 基线实验
- exp2_consumer_memory: 消费者记忆机制研究
- exp3_ai_evolution: AI 进化机制研究
- exp4_information_intervention: 信息干预研究
- exp5_network_structure: 网络结构影响研究
- exp6_generational_dynamics: 代际动态研究
- exp7_ai_competition: AI 竞争研究
- exp8_context_sensitivity: 情境敏感性研究
- exp9_filter_bubble: 信息茧房研究
- exp10_systemic_risk: 系统性风险研究

### 5. 可视化模块 (isualization/)
- 中文支持
- 绘图工具

### 6. 前端交互平台 (rontend/)
- Web 界面交互

## 安装说明

`ash
# 克隆仓库
git clone https://github.com/YinMengjiao/abm_agents.git

# 进入目录
cd abm_simulation

# 创建虚拟环境（可选）
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
`

## 使用方法

### 运行基线实验
`ash
python abm_simulation/experiments/baseline_exp1/run_baseline.py
`

### 运行其他实验
`ash
# 消费者记忆实验
python abm_simulation/experiments/exp2_consumer_memory/run_comparison.py

# AI 进化实验
python abm_simulation/experiments/exp3_ai_evolution/run_evolution.py

# 信息干预实验
python abm_simulation/experiments/exp4_information_intervention/run_intervention.py
`

### 启动前端界面
`ash
python abm_simulation/frontend/start_server.py
`

然后在浏览器中打开 http://localhost:8000

## 项目结构

`
abm_simulation/
 agents/              # 智能体模块
 environment/         # 环境模块
 models/             # 模型模块
 experiments/        # 实验模块
    baseline_exp1/
    exp2_consumer_memory/
    exp3_ai_evolution/
    ...
 visualization/      # 可视化模块
 frontend/           # 前端界面
 results/            # 结果输出目录
 latex_report/       # LaTeX 报告
`

## 技术栈

- Python 3.x
- NumPy
- Matplotlib
- NetworkX
- HTML/CSS/JavaScript (前端)

## 注意事项

- 实验结果图片已添加到 .gitignore，不会提交到仓库
- Python 缓存文件已忽略
- LaTeX 编译产物已忽略

## 许可证

本项目仅供学术研究使用。

## 联系方式

如有问题，请通过 GitHub Issues 联系。
