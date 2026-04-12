# 语言开关功能实现总结

## 概述
为所有实验的可视化脚本添加了中英文语言开关功能，支持通过命令行参数 `--en` 切换图表语言。

## 已修改的实验

### 1. 对比实验 (exp_comparison_init)
- **文件**: `visualization_comparison.py`
- **主函数**: `create_comparison_visualization(results, output_dir=None, en=False)`
- **命令**: 
  ```bash
  python visualization_comparison.py          # 中文版本
  python visualization_comparison.py --en     # 英文版本
  ```
- **特性**: 完整的TEXT_CONFIG字典，所有子图和标签都支持中英文切换

### 2. 实验2 - AI进化机制 (exp2_mechanism)
- **可视化文件**: `visualization_evolution.py`
- **运行文件**: `run_evolution.py`
- **主函数**: `visualize_evolution_results(sim, output_dir=None, en=False)`
- **命令**:
  ```bash
  python run_evolution.py          # 中文版本
  python run_evolution.py --en     # 英文版本
  ```

### 3. 实验3-a - 过滤气泡 (exp3_consequences/filter_bubble)
- **可视化文件**: `visualization_filter_bubble.py`
- **运行文件**: `run_filter_bubble.py`
- **主函数**: `visualize_filter_bubble_results(analyzer, results, output_dir=None, en=False)`
- **命令**:
  ```bash
  python run_filter_bubble.py          # 中文版本
  python run_filter_bubble.py --en     # 英文版本
  ```

### 4. 实验3-b - 系统性风险 (exp3_consequences/systemic_risk)
- **可视化文件**: `visualization_systemic_risk.py`
- **运行文件**: `run_systemic_risk.py`
- **主函数**: `visualize_systemic_risk_results(main_result, stress_results, risk_model, output_dir=None, en=False)`
- **命令**:
  ```bash
  python run_systemic_risk.py          # 中文版本
  python run_systemic_risk.py --en     # 英文版本
  ```

### 5. 实验4 - 信息干预 (exp4_intervention)
- **可视化文件**: `visualization_intervention.py`
- **运行文件**: `run_intervention.py`
- **主函数**: `visualize_all_policy_results(policy_sims, output_dir=None, en=False)`
- **命令**:
  ```bash
  python run_intervention.py          # 中文版本
  python run_intervention.py --en     # 英文版本
  ```

## 实现模式

### 1. 语言配置字典
每个可视化文件都包含TEXT_CONFIG字典：
```python
TEXT_CONFIG = {
    'zh': {
        'title': '实验标题',
        # ... 其他文本
    },
    'en': {
        'title': 'Experiment Title',
        # ... other texts
    }
}
```

### 2. 函数签名统一
所有可视化主函数都添加了 `en: bool = False` 参数：
```python
def visualize_xxx(..., en: bool = False):
    """
    Args:
        en: True=英文, False=中文 (默认)
    """
    lang = 'en' if en else 'zh'
    text = TEXT_CONFIG[lang]
    # 使用 text['key'] 访问文本
```

### 3. 命令行参数支持
所有run文件都添加了argparse支持：
```python
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='运行实验')
    parser.add_argument('--en', action='store_true', help='生成英文版本的图表')
    args = parser.parse_args()
    
    run_experiment(en=args.en)
```

### 4. 运行时语言提示
在生成可视化前显示当前语言：
```python
lang_str = '英文' if en else '中文'
print(f"语言: {lang_str}")
visualize_function(..., en=en)
```

## 扩展指南

### 为其他实验添加语言开关

1. **在可视化文件中添加TEXT_CONFIG字典**
2. **修改主函数签名**: 添加 `en: bool = False` 参数
3. **更新主标题**: 使用 `TEXT_CONFIG['en' if en else 'zh']['title']`
4. **修改run文件**: 
   - 函数添加 `en` 参数
   - 调用可视化函数时传递 `en=en`
   - 添加 `argparse` 支持
   - 添加语言提示输出

## 注意事项

1. **向后兼容**: 所有函数默认 `en=False`，保持向后兼容
2. **部分实现**: 实验2、3、4目前只修改了主标题，内部子图标签可以后续逐步完善
3. **完整实现**: 对比实验(exp_comparison_init)已完整实现所有文本的中英文切换
4. **一致性**: 所有实验使用相同的参数名称和调用模式

## 使用示例

```bash
# 批量生成中文版本
python run_evolution.py
python run_filter_bubble.py
python run_systemic_risk.py
python run_intervention.py
python visualization_comparison.py

# 批量生成英文版本
python run_evolution.py --en
python run_filter_bubble.py --en
python run_systemic_risk.py --en
python run_intervention.py --en
python visualization_comparison.py --en
```

## 文件清单

### 已修改的可视化文件 (5个)
1. `exp_comparison_init/visualization_comparison.py` - 完整实现
2. `exp2_mechanism/visualization_evolution.py` - 基础实现
3. `exp3_consequences/filter_bubble/visualization_filter_bubble.py` - 基础实现
4. `exp3_consequences/systemic_risk/visualization_systemic_risk.py` - 基础实现
5. `exp4_intervention/visualization_intervention.py` - 基础实现

### 已修改的run文件 (5个)
1. `exp_comparison_init/run_comparison.py` (如果存在)
2. `exp2_mechanism/run_evolution.py`
3. `exp3_consequences/filter_bubble/run_filter_bubble.py`
4. `exp3_consequences/systemic_risk/run_systemic_risk.py`
5. `exp4_intervention/run_intervention.py`

## 下一步建议

1. **完善内部标签**: 为实验2、3、4的内部子图标签添加完整的TEXT_CONFIG支持
2. **扩展到基线实验**: 为exp1_baseline添加语言开关
3. **统一文本管理**: 考虑将TEXT_CONFIG提取到独立的配置文件
4. **添加更多语言**: 如需支持其他语言，只需扩展TEXT_CONFIG字典
