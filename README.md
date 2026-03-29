# ABM 消费决策代理模拟系统

## 📋 项目简介

本项目是一个基于 **Ising-D-I-B 三层耦合模型**的 AI 消费决策代理仿真系统，用于研究 AI 推荐对消费者决策的影响机制。项目包含 10 个完整的仿真实验模块和统一的可视化平台。

### 核心理论框架

- **Ising 模型**: 模拟社会影响下的群体行为相变
- **D-I-B 框架**: Desire(渴望)-Intention(意图)-Behavior(行为) 三层决策结构
- **ACDDS 量表**: AI 消费决策依赖等级评估标准 (L1-L5)

---

## 🎯 核心功能

### 1. 多智能体仿真系统
- **500+ 消费者智能体**: 具备记忆、学习和社会网络能力
- **AI 代理**: 提供个性化推荐服务
- **商家智能体**: 动态定价和策略调整
- **社交网络**: Small-world、Scale-free 等多种拓扑结构

### 2. 实验模块 (10 个完整实验)

#### 基础实验
- **实验 1**: 基线模型 (Baseline) - Ising-D-I-B 基础模型验证
- **实验 2**: 记忆增强模型 - 消费者记忆学习机制

#### 扩展实验
- **实验 3**: AI 进化机制 - AI 从反馈中学习改进
- **实验 4**: 信息干预 - 政策效果评估 (平衡/推广 AI/保护消费者)
- **实验 5**: 网络结构 - 不同拓扑结构对比 (Random/Small-world/SF/Chain)
- **实验 6**: 代际动态 - 数字原生 vs 数字移民
- **实验 7**: AI 竞争 - 多个 AI 代理市场竞争
- **实验 8**: 情境敏感性 - 工作/家庭/社交/购物场景
- **实验 9**: 过滤气泡 - 信息茧房效应分析
- **实验 10**: 系统性风险 - 技术故障的社会传染

### 3. 可视化平台
所有实验自动生成高质量学术图表，包括:
- 依赖等级分布演化图
- Ising 动力学曲线
- 性能指标对比
- 网络拓扑可视化
- 综合分析报告

---

## 🚀 快速开始

### 环境要求
```bash
Python >= 3.8
numpy >= 1.21.0
matplotlib >= 3.4.0
networkx >= 2.6
scipy >= 1.7.0
Pillow >= 8.0.0
```

### 安装依赖
```bash
cd abm_simulation
pip install -r requirements.txt
```

### 运行方式

#### 方法 1: 交互式统一平台 (推荐)
```bash
python run_interactive_unified.py
```
提供友好的命令行菜单，可选择运行任意实验。

#### 方法 2: 直接运行单个实验
```bash
# 实验 1: 基线模型
python experiments/baseline_exp1/run_baseline.py

# 实验 2: 记忆增强
python experiments/exp2_consumer_memory/run_comparison.py

# 实验 3-10
python experiments/exp3_ai_evolution/run_evolution.py
python experiments/exp4_information_intervention/run_intervention.py
python experiments/exp5_network_structure/run_network.py
python experiments/exp6_generational_dynamics/run_generational.py
python experiments/exp7_ai_competition/run_competition.py
python experiments/exp8_context_sensitivity/run_context.py
python experiments/exp9_filter_bubble/run_bubble.py
python experiments/exp10_systemic_risk/run_systemic_risk.py
```

#### 方法 3: 批量运行所有实验
```bash
python experiments/collect_all_visualizations.py
```

---

## 📊 输出结果

### 目录结构
```
ABM 消费决策代理/
├── abm_simulation/              # 主程序目录
│   ├── agents/                  # 智能体模块
│   │   ├── ai_agent.py         # AI 代理
│   │   └── consumer_dib.py     # D-I-B 消费者
│   ├── environment/             # 环境模块
│   │   └── market.py           # 市场环境
│   ├── models/                  # 模型模块
│   │   └── ising_network.py    # Ising 网络
│   ├── experiments/             # 10 个实验模块
│   │   ├── baseline_exp1/      # 实验 1
│   │   ├── exp2_consumer_memory/ # 实验 2
│   │   ├── ...                 # 实验 3-10
│   │   └── collect_all_png_final.py  # 图片收集脚本
│   ├── results/                 # 结果汇总
│   │   └── all_experiments_figures/  # 统一图片目录
│   └── visualization/           # 可视化工具
├── experiments/                 # 实验结果 (旧版兼容)
├── results/                     # 统一结果目录
│   └── all_experiments_figures/ # 18 张汇总图
└── README.md                    # 本文件
```

### 可视化输出示例

每个实验生成 1-4 张 PNG 图片，保存在对应实验的 `results/` 目录。

**统一图片目录**: `results/all_experiments_figures/` 包含所有 18 张图片:

#### 实验 1 (4 张)
- `baseline_exp1_final_distribution.png` - 最终依赖等级分布
- `baseline_exp1_ising_dynamics.png` - Ising 动力学
- `baseline_exp1_level_distribution_evolution.png` - 等级演化
- `baseline_exp1_performance_metrics.png` - 性能指标

#### 实验 2 (4 张)
- `experiment2_memory_level_distribution_comparison.png` - 等级对比
- `experiment2_memory_memory_dynamics.png` - 记忆动力学
- `experiment2_memory_metrics_comparison.png` - 指标对比
- `experiment2_memory_summary_radar.png` - 综合雷达图

#### 实验 3-10 (各 1-3 张)
- `exp3_ai_evolution_evolution_analysis.png`
- `exp4_information_intervention_balanced_intervention_analysis.png`
- `exp4_information_intervention_promote_ai_intervention_analysis.png`
- `exp4_information_intervention_protect_consumers_intervention_analysis.png`
- `exp5_network_structure_network_comparison.png`
- `exp6_generational_dynamics_generational_analysis.png`
- `exp7_ai_competition_competition_analysis.png`
- `exp8_context_sensitivity_context_analysis.png`
- `exp9_filter_bubble_filter_bubble_analysis.png`
- `exp10_systemic_risk_systemic_risk_analysis.png`

---

## 🔬 核心参数配置

### 默认设置
```python
# 基础参数
NUM_CONSUMERS = 500      # 消费者数量
NUM_MERCHANTS = 20       # 商家数量
NUM_AI_AGENTS = 3        # AI 代理数量
STEPS = 300             # 仿真步数

# 依赖等级分布 (L1-L5)
LEVEL_DISTRIBUTION = {
    'L1': 0.10,   # 自主型 (10%)
    'L2': 0.25,   # 信息辅助 (25%)
    'L3': 0.30,   # 半委托 (30%)
    'L4': 0.25,   # 高度依赖 (25%)
    'L5': 0.10    # 完全代理 (10%)
}

# Ising 模型参数
Jc = 0.1667         # 临界耦合强度
temperature = 0.1   # 温度参数

# 网络类型
NETWORK_TYPE = 'small_world'  # small_world/random/scale_free/chain
```

### 自定义配置
通过环境变量或修改 `simulation.py` 中的配置类进行调整。

---

## 📈 关键研究发现

### 实验 1: 基线模型
- **相变现象**: 当耦合强度 J > Jc ≈ 0.167 时，系统发生相变
- **L4 聚集**: 大量消费者向 L4(高度依赖)集中
- **满意度提升**: AI 使用率提高带来满意度上升

### 实验 2: 记忆增强
- **错误率降低 71%**: 记忆学习有效避免重复错误
- **AI 使用理性化**: 从 85% 降至 50%，更加理性选择
- **信任度提升**: 动态信任机制改善长期关系

### 实验 3: AI 进化
- **适应性改进**: AI 根据反馈持续优化推荐质量
- **稳定性增强**: 系统波动减小，收敛更快

### 实验 4: 信息干预
- **平衡干预最优**: 兼顾 AI 发展和消费者保护
- **过度推广反效**: 单纯推广 AI 可能导致依赖过度

### 实验 5: 网络结构
- **Small-world 最优**: 聚类系数高，传播效率高
- **Scale-free 脆弱**: 枢纽节点故障影响巨大

### 实验 6: 代际差异
- **数字原生适应快**: 年轻群体 AI 接受度高
- **数字移民需要支持**: 年长群体需要更多引导

### 实验 7: AI 竞争
- **适度竞争有益**: 促进 AI 服务质量提升
- **恶性竞争有害**: 价格战损害整体生态

### 实验 8: 情境敏感
- **场景差异显著**: 不同情境下 AI 依赖度不同
- **工作场景最高**: 专业决策更依赖 AI

### 实验 9: 过滤气泡
- **信息茧房存在**: 强推荐导致视野狭窄
- **多样性重要**: 需要平衡个性化和多样性

### 实验 10: 系统性风险
- **级联失效风险**: 技术故障可能引发社会传染
- **韧性建设必要**: 需要建立容错和恢复机制

---

## 🛠️ 工具脚本

### 图片管理
```bash
# 收集所有实验图片到统一目录
python abm_simulation/experiments/collect_all_png_final.py

# 查看所有生成的图片
python results/all_experiments_figures/view_all.py
```

### 数据分析
```bash
# 查看实验汇总
python view_all_summaries.py

# 验证图片完整性
python verify_figures.py
```

---

## 📚 学术价值

### 理论贡献
1. **Ising-D-I-B 耦合模型**: 首次将物理模型与决策理论结合
2. **ACDDS 量表**: 提出 AI 依赖等级评估标准
3. **相变临界值**: 发现 Jc ≈ 0.167 的关键阈值

### 实践意义
1. **政策制定**: 为 AI 监管提供科学依据
2. **企业战略**: 指导 AI 产品设计和市场定位
3. **消费者教育**: 提高公众 AI 素养

---

## 🔧 常见问题

### Q1: 中文字体显示问题
**解决**: 项目已内置中文字体检测，自动选择 SimHei/Microsoft YaHei/Arial Unicode MS

### Q2: 内存不足
**解决**: 减少 `NUM_CONSUMERS` 或 `STEPS` 参数

### Q3: 网络生成失败
**解决**: 检查 `NetworkGenerator` 类的 `generate()` 方法返回值

### Q4: 实验结果不一致
**说明**: 由于随机种子不同，每次运行结果会有细微差异，属正常现象

---

## 📝 版本历史

### v2.0 (最新)
- ✅ 完成 10 个实验模块的统一化
- ✅ 实现动态 L1-L5 比例参数注入
- ✅ 构建统一可视化平台
- ✅ 标准化接口和函数命名
- ✅ 添加图片自动收集功能

### v1.0
- 基础 Ising-D-I-B 模型实现
- 前 5 个实验模块开发

---

## 👥 团队信息

**项目负责人**: [您的姓名]  
**所属机构**: [您的机构]  
**研究方向**: AI 消费决策、多智能体仿真、计算社会科学  

---

## 📧 联系方式

如有问题或合作意向，请通过以下方式联系:
- Email: [您的邮箱]
- GitHub: [项目地址]

---

## 📄 许可证

本项目采用 MIT 开源许可证。

---

## 🙏 致谢

感谢以下支持和贡献:
- [资助机构名称] (项目编号：XXX)
- [合作者姓名] 提供的宝贵建议
- 开源社区的优秀工具库

---

## 🔗 相关链接

- [Ising 模型维基百科](https://en.wikipedia.org/wiki/Ising_model)
- [ABM 仿真教程](https://www.comses.net/)
- [NetLogo 官方文档](https://ccl.northwestern.edu/netlogo/)

---

**最后更新时间**: 2026 年 3 月 28 日
