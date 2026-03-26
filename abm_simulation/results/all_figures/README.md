# ABM 仿真实验可视化说明

## 📊 图表总览

所有实验的可视化图表已集中到：**`results/all_figures/`** 文件夹

### 收集的图表清单（共 15 张）

#### 基线实验（4 张）
- `baseline_exp1_level_distribution_evolution.png` - 依赖等级分布演化
- `baseline_exp1_ising_dynamics.png` - Ising 动力学
- `baseline_exp1_performance_metrics.png` - 性能指标
- `baseline_exp1_final_distribution.png` - 最终分布

#### 实验 2：消费者记忆（4 张）
- `experiment2_memory_level_distribution_comparison.png` - 等级分布对比
- `experiment2_memory_metrics_comparison.png` - 指标对比
- `experiment2_memory_memory_dynamics.png` - 记忆动态
- `experiment2_memory_summary_radar.png` - 总结雷达图

#### 实验 3：AI 进化（1 张）
- `exp3_ai_evolution_evolution_analysis.png` - AI 进化分析

#### 实验 4：信息干预（3 张）
- `exp4_information_intervention_intervention_analysis.png` - 干预分析（3 种政策）

#### 实验 8：情境敏感性（1 张）
- `exp8_context_sensitivity_context_analysis.png` - 情境分析

#### 实验 9：过滤气泡（1 张）
- `exp9_filter_bubble_filter_bubble_analysis.png` - 过滤气泡分析

#### 实验 10：系统性风险（1 张）
- `exp10_systemic_risk_systemic_risk_analysis.png` - 系统性风险分析

#### 测试图表（1 张）
- `00_中文字体测试.png` - 中文字体显示测试

---

## 🔧 中文字体支持

### 已配置的中文字体
系统已自动检测并使用以下中文字体（按优先级）：
1. **SimHei** (黑体) - Windows 默认
2. **Microsoft YaHei** (微软雅黑)
3. **Microsoft JhengHei** (微软正黑)
4. **Arial Unicode MS**

### 字体配置文件
- **文件位置**: `visualization/chinese_font.py`
- **功能**: 为所有可视化提供统一的中文字体支持
- **使用方法**: 在任何可视化脚本开头添加：
  ```python
  from visualization.chinese_font import setup_chinese_font
  setup_chinese_font()
  ```

---

## 📁 文件夹结构

```
abm_simulation/
├── results/
│   └── all_figures/           # ← 所有图表集中在此
│       ├── 00_中文字体测试.png
│       ├── baseline_exp1_*.png
│       ├── experiment2_memory_*.png
│       ├── exp3_ai_evolution_*.png
│       ├── exp4_information_intervention_*.png
│       ├── exp8_context_sensitivity_*.png
│       ├── exp9_filter_bubble_*.png
│       └── exp10_systemic_risk_*.png
├── experiments/
│   ├── baseline_exp1/results/    # 原始图表（保留）
│   ├── exp2_consumer_memory/results/
│   └── ...
└── visualization/
    ├── chinese_font.py          # 中文字体配置
    ├── collect_all_figures.py   # 图表收集工具
    └── plots.py                 # 基础可视化模块
```

---

## 🎨 图表中文支持验证

运行测试脚本验证中文显示：
```bash
python test_chinese_font.py
```

如果看到 "✓ 测试图表已保存" 且图表中的中文正常显示，说明中文字体配置成功。

---

## 📝 注意事项

1. **字体缺失问题**: 
   - 如果图表中出现方框□代替中文，说明系统缺少中文字体
   - Windows: 确保安装了微软雅黑或黑体
   - Mac: 确保安装了 Arial Unicode MS 或 PingFang
   - Linux: 安装文泉驿字体包

2. **图表重复**: 
   - 某些实验有多个政策的图表（如实验 4 有 3 个政策）
   - 文件名已包含实验名称前缀便于区分

3. **重新生成图表**: 
   - 运行单个实验脚本会重新生成该实验的所有图表
   - 图表会自动更新到 `results/all_figures/` 目录

---

## 🚀 快速查看

在文件浏览器中打开 `results/all_figures/` 文件夹即可查看所有 15 张图表。

或使用以下命令批量预览（Windows）：
```powershell
Get-ChildItem results\all_figures\*.png | ForEach-Object { Invoke-Item $_.FullName }
```
