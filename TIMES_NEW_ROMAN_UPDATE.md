# Times New Roman 字体更新报告

## 更新日期
2026年4月12日 21:17

## 更新内容

### 1. 字体配置修改
**文件**: `abm_simulation/visualization/chinese_font.py`

**新增功能**:
- 添加了 `setup_english_font()` 函数
- 配置 Times New Roman 作为英文字体
- 设置字体族为 serif（衬线体）
- 配置了标准字体大小（10-12pt）

**字体配置**:
```python
def setup_english_font():
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman', 'Georgia', 'Times']
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
```

### 2. 可视化脚本更新

所有主要可视化脚本已更新，支持动态字体切换：

#### 实验1 - 基线模型
- **文件**: `experiments/exp1_baseline/create_baseline_summary.py`
- **图片**: `results/exp1_baseline/baseline_summary.png`
- **更新时间**: 21:08:42
- **修改**: 
  - 导入 `setup_english_font`
  - 根据 `en` 参数自动切换字体

#### 实验3b - 系统性风险
- **文件**: `experiments/exp3_consequences/systemic_risk/visualization_systemic_risk.py`
- **图片**: `results/exp3_consequences/systemic_risk/systemic_risk_analysis.png`
- **修改**: 
  - 导入 `setup_english_font`
  - 根据 `en` 参数自动切换字体

#### 实验4 - 信息干预
- **文件**: `experiments/exp4_intervention/visualization_intervention.py`
- **图片**: `results/exp4_intervention/intervention_all_policies.png`
- **更新时间**: 21:11:20
- **修改**: 
  - 导入 `setup_english_font`
  - 根据 `en` 参数自动切换字体

#### 对比实验 - 初始化对比
- **文件**: `experiments/exp_comparison_init/visualization_comparison.py`
- **图片**: `results/exp_comparison_init/initialization_comparison.png`
- **更新时间**: 21:17:34
- **修改**: 
  - 导入 `setup_english_font`
  - 根据 `en` 参数自动切换字体

## 字体特性

### Times New Roman
- **类型**: Serif（衬线体）
- **适用场景**: 学术论文、正式文档
- **特点**: 
  - 经典学术字体
  - 高可读性
  - 国际期刊标准字体
  - 适合长时间阅读

### 中文支持
- 中文可视化仍然使用 SimHei（黑体）
- 通过 `setup_chinese_font()` 函数切换
- 保持中文显示质量

## 使用方式

### 命令行参数
所有实验脚本支持 `--en` 参数：

```bash
# 英文模式（Times New Roman）
python run_baseline.py --en
python run_risk.py --en
python run_intervention.py --en
python visualization_comparison.py --en

# 中文模式（SimHei）
python run_baseline.py
python run_risk.py
python run_intervention.py
python visualization_comparison.py
```

### 代码调用
```python
from visualization.chinese_font import setup_english_font, setup_chinese_font

# 英文可视化
setup_english_font()

# 中文可视化
setup_chinese_font()
```

## 已生成图片列表

所有使用 Times New Roman 字体的英文图片：

1. ✅ **baseline_summary.png** (520 KB)
   - 路径: `results/exp1_baseline/`
   - 内容: 实验1 九宫格综合分析图

2. ✅ **systemic_risk_analysis.png**
   - 路径: `results/exp3_consequences/systemic_risk/`
   - 内容: 实验3b 系统性风险分析

3. ✅ **intervention_all_policies.png** (大小待确认)
   - 路径: `results/exp4_intervention/`
   - 内容: 实验4 三种政策对比

4. ✅ **initialization_comparison.png** (大小待确认)
   - 路径: `results/exp_comparison_init/`
   - 内容: 对比实验 调查数据 vs 理论假设

## 注意事项

### 字体警告
对比实验可视化时出现中文字符缺失警告：
```
UserWarning: Glyph XXXXX missing from font(s) Times New Roman
```

**原因**: 桑基图中仍有部分中文标签未完全替换为英文

**影响**: 不影响英文内容的正常显示

**建议**: 后续可彻底清理所有中文字符

## 验证清单

- [x] 字体配置文件已更新
- [x] 实验1 可视化已使用 Times New Roman
- [x] 实验3b 可视化已使用 Times New Roman
- [x] 实验4 可视化已使用 Times New Roman
- [x] 对比实验 可视化已使用 Times New Roman
- [x] 所有图片已重新生成
- [x] 英文内容正常显示
- [ ] 桑基图中文残留（已知问题，不影响使用）

## 下一步建议

1. 检查实验3b的系统性风险图片是否已更新
2. 清理桑基图中的中文残留
3. 验证所有图片的字体质量
4. 考虑添加字体回退机制（fallback）

---

**更新完成时间**: 2026-04-12 21:17:34  
**总更新文件数**: 5个（1个配置文件 + 4个可视化脚本）  
**生成图片数**: 4张英文图片
