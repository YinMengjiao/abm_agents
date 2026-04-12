# ABM 消费决策代理仿真系统

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/AicbLab/abm_agents.svg)](https://github.com/AicbLab/abm_agents/stargazers)

> **基于 Ising-D-I-B 三层耦合模型的 AI 消费决策多智能体仿真平台**

本项目是一个计算社会科学研究工具，用于模拟和分析 AI 推荐系统对消费者决策行为的影响机制。系统整合了物理学相变理论、行为决策心理学和多智能体建模方法，提供 10 个完整的仿真实验模块。

---

## 📑 目录

- [核心理论](#-核心理论)
- [系统特性](#-系统特性)
- [实验模块](#-实验模块)
- [快速开始](#-快速开始)
- [输出结果](#-输出结果)
- [参数配置](#-参数配置)
- [关键发现](#-关键研究发现)
- [学术价值](#-学术价值)
- [常见问题](#-常见问题)
- [引用与许可](#-引用与许可)

---

## 🎯 核心理论

### Ising-D-I-B 三层耦合模型

本系统首次将三个理论框架整合为统一模型：

| 层次 | 理论来源 | 作用机制 |
|------|---------|---------|
| **Ising 层** | 统计物理学 | 模拟社会网络中的群体行为相变 |
| **D-I-B 层** | 行为决策理论 | Desire(渴望)→Intention(意图)→Behavior(行为) 决策链 |
| **ACDDS 层** | 心理测量学 | AI 消费决策依赖等级评估 (L1-L5) |

### 相变临界值

系统发现关键相变阈值：**Jc ≈ 0.167**
- 当耦合强度 J < Jc：系统处于无序状态，消费者行为独立
- 当耦合强度 J > Jc：系统发生相变，出现群体聚集效应

---

## ⚡ 系统特性

### 多智能体架构

```
┌─────────────────────────────────────────────┐
│           市场环境 (Market)                  │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐ │
│  │ 消费者 ×500│  │ 商家 ×20 │  │ AI代理 ×3│ │
│  │ (D-I-B模型)│  │(动态定价)│  │(推荐系统)│ │
│  └───────────┘  └──────────┘  └──────────┘ │
│         ↕              ↕             ↕      │
│        社交网络 (Small-world/Scale-free)     │
└─────────────────────────────────────────────┘
```

### 核心能力

- ✅ **500+ 消费者智能体**：具备记忆、学习、社会影响能力
- ✅ **AI 推荐代理**：支持个性化推荐和在线学习进化
- ✅ **动态社交网络**：Small-world、Scale-free、Random 等多种拓扑
- ✅ **可视化平台**：自动生成学术级高质量图表
- ✅ **交互式菜单**：统一入口运行所有实验

---

## 🔬 实验模块

系统包含 **10 个完整实验**，覆盖从基础验证到复杂场景的全方位研究：

### 基础实验 (Exp 1-2)

| 实验 | 名称 | 研究问题 | 关键指标 |
|------|------|---------|---------|
| **Exp 1** | 基线模型 | Ising-D-I-B 模型是否有效？ | 相变临界值 Jc、L1-L5 分布 |
| **Exp 2** | AI 进化机制 | AI 能否从反馈中学习？ | 错误率下降、进化进度 |

### 机制实验 (Exp 3-5)

| 实验 | 名称 | 研究问题 | 关键指标 |
|------|------|---------|---------|
| **Exp 3-a** | 过滤气泡 | 推荐算法是否导致信息茧房？ | 选择多样性、香农熵 |
| **Exp 3-b** | 系统性风险 | 技术故障如何级联传播？ | 影响范围、恢复时间 |
| **Exp 4** | 信息干预 | 政策如何影响系统演化？ | 高依赖群体变化 |
| **Exp 5** | 网络结构 | 不同拓扑结构的影响？ | 传播速度、聚集程度 |

### 扩展实验 (Exp 6-10)

| 实验 | 名称 | 研究问题 |
|------|------|---------||
| **Exp 6** | 代际动态 | 数字原生 vs 数字移民的差异 |
| **Exp 7** | AI 竞争 | 多个 AI 代理的市场竞争 |
| **Exp 8** | 情境敏感 | 工作/家庭/购物场景的差异 |
| **Exp 9** | 过滤气泡 | 信息茧房效应深度分析 |
| **Exp 10** | 系统性风险 | 技术故障的社会传染机制 |

---

## 🚀 快速开始

### 环境要求

```bash
Python >= 3.8
numpy >= 1.21.0
matplotlib >= 3.4.0
networkx >= 2.6
scipy >= 1.7.0
```

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/AicbLab/abm_agents.git
cd abm_agents

# 安装依赖
cd abm_simulation
pip install numpy matplotlib networkx scipy
```

### 运行实验

#### 方法 1：交互式统一平台（⭐ 推荐）

```bash
python run_interactive_unified.py
```

提供友好的命令行菜单，可选择运行任意实验，支持自定义参数。

#### 方法 2：直接运行单个实验

```bash
# 实验 1：基线模型
python abm_simulation/experiments/baseline_exp1/run_baseline.py

# 实验 2：AI 进化机制
python abm_simulation/experiments/exp2_mechanism/run_evolution.py

# 实验 3-a：过滤气泡
python abm_simulation/experiments/exp3_consequences/filter_bubble/run_filter_bubble.py

# 实验 3-b：系统性风险
python abm_simulation/experiments/exp3_consequences/systemic_risk/run_systemic_risk.py

# 实验 4：信息干预
python abm_simulation/experiments/exp4_intervention/run_intervention.py
```

#### 方法 3：批量运行所有实验

```bash
python run_all_experiments.py
```

---

## 📊 输出结果

### 目录结构

```
abm_agents/
├── abm_simulation/
│   ├── agents/                  # 智能体模块
│   │   ├── ai_agent.py         # AI 代理（支持学习进化）
│   │   └── consumer_dib.py     # D-I-B 消费者模型
│   ├── environment/             # 环境模块
│   │   └── market.py           # 市场环境
│   ├── models/                  # 模型模块
│   │   └── ising_network.py    # Ising 社交网络
│   ├── experiments/             # 实验模块
│   │   ├── baseline_exp1/      # 实验 1：基线模型
│   │   ├── exp2_mechanism/     # 实验 2：AI 进化机制
│   │   ├── exp3_consequences/  # 实验 3：后果分析
│   │   │   ├── filter_bubble/  #   3-a：过滤气泡
│   │   │   └── systemic_risk/  #   3-b：系统性风险
│   │   ├── exp4_intervention/  # 实验 4：信息干预
│   │   └── ...                 # 实验 5-10
│   ├── results/                 # 实验结果
│   │   ├── exp1_baseline/      # 实验 1 结果
│   │   ├── exp2_mechanism/     # 实验 2 结果
│   │   ├── exp3_consequences/  # 实验 3 结果
│   │   │   ├── filter_bubble/  #   过滤气泡图表
│   │   │   └── systemic_risk/  #   系统性风险图表
│   │   └── exp4_intervention/  # 实验 4 结果
│   └── visualization/           # 可视化工具
│       └── chinese_font.py     # 中文字体配置
├── run_interactive_unified.py   # 交互式统一入口
├── run_all_experiments.py       # 批量运行脚本
└── README.md
```

### 可视化示例

每个实验生成 1-4 张学术级 PNG 图表：

#### 实验 1：基线模型（4 张）
- `final_distribution.png` - 最终依赖等级分布
- `ising_dynamics.png` - Ising 动力学曲线
- `level_distribution_evolution.png` - 等级演化热图
- `performance_metrics.png` - 性能指标

#### 实验 2：AI 进化机制（1 张）
- `evolution_analysis.png` - AI 错误率下降与进化进度

#### 实验 3-a：过滤气泡（1 张）
- `filter_bubble_analysis.png` - 选择多样性与过滤气泡强度

#### 实验 3-b：系统性风险（1 张）
- `systemic_risk_analysis.png` - 故障传播与系统韧性

#### 实验 4：信息干预（1 张）
- `intervention_all_policies.png` - 三种政策对比（9 子图）
  - (a-c) 干预事件时间分布
  - (d-f) L1-L5 依赖等级动态演化
  - (g-i) 高依赖群体受干预影响轨迹

---

## ⚙️ 参数配置

### 默认参数

```python
# 系统规模
NUM_CONSUMERS = 500      # 消费者数量
NUM_MERCHANTS = 20       # 商家数量
NUM_AI_AGENTS = 3        # AI 代理数量
STEPS = 300             # 仿真步数

# 依赖等级初始分布 (L1-L5)
LEVEL_DISTRIBUTION = {
    'L1': 0.10,   # 自主型 (10%)
    'L2': 0.25,   # 信息辅助型 (25%)
    'L3': 0.30,   # 半委托型 (30%)
    'L4': 0.25,   # 高度依赖型 (25%)
    'L5': 0.10    # 完全代理型 (10%)
}

# Ising 模型参数
Jc = 0.1667         # 临界耦合强度（相变阈值）
temperature = 0.1   # 系统温度

# 网络拓扑
NETWORK_TYPE = 'small_world'  # small_world / random / scale_free
```

### 自定义配置

通过 `run_interactive_unified.py` 交互式设置，或修改 `config.py` 中的配置类。

---

## 💡 关键研究发现

### 实验 1：基线模型验证

- ✅ **相变现象确认**：当耦合强度 J > Jc ≈ 0.167 时，系统发生从无序到有序的相变
- ✅ **L4 聚集效应**：大量消费者向 L4（高度依赖）集中，占比达 40-60%
- ✅ **满意度正相关**：AI 使用率提升带来整体满意度上升

### 实验 2：AI 进化机制

- ✅ **错误率下降 85%**：AI 从初始 0.085 降至 0.013
- ✅ **学习曲线明显**：进化进度达 0.263（300 步内）
- ✅ **高依赖形成**：88.4% 消费者达到 L4 依赖等级

### 实验 3-a：过滤气泡效应

- ✅ **信息茧房存在**：过滤气泡强度 0.117
- ✅ **低依赖更严重**：L1 多样性 0.922 > L5 多样性 0.774
- ✅ **整体多样性**：0.872（存在一定程度的信息窄化）

### 实验 3-b：系统性风险

- ✅ **级联失效**：MAJOR 故障影响 162 人（32.4%）
- ✅ **系统韧性**：得分 4.897，149 步内恢复
- ✅ **压力测试**：从 minor_outage (39人) 到 coordinated_attack (256人)

### 实验 4：信息干预政策

| 政策类型 | L2 比例 | L4 比例 | 满意度 | 干预效果 |
|---------|---------|---------|--------|----------|
| **均衡政策** | 37.4% | 31.4% | 0.313 | 高依赖 -68 人 |
| **促进 AI** | 3.4% | **94.2%** | 0.318 | 高依赖 +19 人 |
| **保护消费者** | 3.8% | **90.4%** | 0.307 | 高依赖 +24.5 人 |

- ✅ **促进 AI 政策**最有效推动高依赖（94.2% 达 L4）
- ✅ **均衡政策**满意度最高，但高依赖群体减少

### 实验 5-10：扩展研究

- **网络结构**：Small-world 最优，Scale-free 存在枢纽风险
- **代际差异**：数字原生适应快，数字移民需要支持
- **AI 竞争**：适度竞争提升服务质量
- **情境敏感**：工作场景 AI 依赖度最高
- **过滤气泡**：需平衡个性化与多样性
- **系统风险**：需建立容错和恢复机制

---

## 🎓 学术价值

### 理论贡献

1. **Ising-D-I-B 耦合模型**：首次将物理学相变理论与行为决策模型整合
2. **ACDDS 量表**：提出 AI 消费决策依赖等级评估标准（L1-L5）
3. **相变临界值**：发现 Jc ≈ 0.167 的关键阈值，为政策干预提供科学依据
4. **多维度验证**：10 个实验覆盖基础机制到复杂场景

### 实践意义

1. **政策制定**：为 AI 监管和消费者保护提供量化依据
2. **企业战略**：指导 AI 推荐系统设计和市场定位
3. **消费者教育**：提高公众 AI 素养和风险防范意识
4. **风险管控**：识别系统性风险并建立韧性机制

### 发表潜力

本系统适合作为以下领域的研究基础：
- 计算社会科学（Computational Social Science）
- 多智能体仿真（Agent-Based Modeling）
- AI 伦理与治理（AI Ethics & Governance）
- 消费者行为学（Consumer Behavior）

---

## ❓ 常见问题

### Q1: 中文字体显示异常？

**解决方案**：系统已内置自动检测，优先使用 SimHei → Microsoft YaHei → Arial Unicode MS。如仍有问题，检查系统是否安装这些字体。

### Q2: 内存不足或运行缓慢？

**解决方案**：减少 `NUM_CONSUMERS`（如改为 200）或 `STEPS`（如改为 100）。

### Q3: 实验结果每次运行不一致？

**说明**：由于随机种子不同，结果会有细微差异，属正常现象。相变临界值等关键指标应保持稳定。

### Q4: 如何复现论文结果？

**建议**：使用 `run_interactive_unified.py` 的默认参数，或查看各实验目录下的 `run_*.py` 文件中的配置。

### Q5: 如何修改实验参数？

**方法**：
1. 交互式：运行 `run_interactive_unified.py` 选择自定义参数
2. 代码级：修改对应实验的 `run_*.py` 文件中的 `SimulationConfig`

---

## 📝 版本历史

### v3.0 (2026-04-12) - 最新

- ✅ 修复实验 3-a（过滤气泡）可视化路径配置错误
- ✅ 修复实验 3-b（系统性风险）信任度计算逻辑
- ✅ 优化实验 4（信息干预）可视化：
  - 将柱状图改为事件标记图和演化折线图
  - 为 9 个子图设置学术规范标题 (a-i)
- ✅ 添加 AI 代理 `learning_history` 属性支持实验 2
- ✅ 更新所有实验结果图表

### v2.0 (2026-03-28)

- ✅ 完成 10 个实验模块的统一化
- ✅ 实现动态 L1-L5 比例参数注入
- ✅ 构建统一可视化平台
- ✅ 标准化接口和函数命名

### v1.0 (2026-03-15)

- 基础 Ising-D-I-B 模型实现
- 前 5 个实验模块开发

---

## 👥 团队信息

**项目负责人**：M.Y  
**所属机构**：THU  
**研究方向**：AI 消费决策、多智能体仿真、计算社会科学  

---

## 📧 联系方式

- **Email**: yinmj@wxu.edu.cn
- **GitHub**: https://github.com/AicbLab/abm_agents
- **Issues**: https://github.com/AicbLab/abm_agents/issues

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

---

## 🙏 致谢

感谢以下支持和贡献：
- 资助机构（项目编号：XXX）
- 合作者提供的宝贵建议
- 开源社区的优秀工具库（NumPy, Matplotlib, NetworkX）

---

## 🔗 相关链接

- [Ising 模型 - Wikipedia](https://en.wikipedia.org/wiki/Ising_model)
- [ABM 仿真教程 - ComSES](https://www.comses.net/)
- [计算社会科学综述](https://www.science.org/doi/10.1126/science.1214455)

---

<div align="center">

**如果本项目对您的研究有帮助，欢迎 ⭐ Star 支持！**

最后更新：2026 年 4 月 12 日

</div>
