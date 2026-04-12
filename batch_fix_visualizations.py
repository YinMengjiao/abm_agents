#!/usr/bin/env python3
"""
批量修复所有可视化文件，将中文替换为英文
"""
import re
import os

# 定义替换规则（中文 -> 英文）
REPLACEMENTS = {
    # 实验2
    'exp2_mechanism/visualization_evolution.py': {
        '无进化数据': 'No Evolution Data',
        '仿真步数': 'Simulation Step',
        '进化进度': 'Evolution Progress',
        'AI 进化轨迹': 'AI Evolution Trajectory',
        '无数据': 'No Data',
        '错误率': 'Error Rate',
        'AI错误率进化': 'AI Error Rate Evolution',
        '消费者数量': 'Consumer Count',
        '(a) 依赖等级分布演化': '(a) Dependency Level Distribution Evolution',
        '单步学习事件数': 'Learning Events per Step',
        '学习事件统计': 'Learning Events Statistics',
        '(b) AI能力进化热力图': '(b) AI Capability Evolution Heatmap',
        'AI代理ID': 'AI Agent ID',
        '信任度': 'Trust Level',
        '信任恢复轨迹': 'Trust Recovery Trajectory',
        '消费者信任度': 'Consumer Trust',
    },
    # 实验3-a
    'exp3_consequences/filter_bubble/visualization_filter_bubble.py': {
        '多样性得分': 'Diversity Score',
        '(a) 各依赖等级选择多样性': '(a) Choice Diversity by Dependency Level',
        '(b) 多样性分布': '(b) Diversity Distribution',
        '消费者数量': 'Consumer Count',
        '平均探索率': 'Average Exploration Rate',
        '(c) 各等级探索行为': '(c) Exploration Behavior by Level',
        '产品类别': 'Product Category',
        '消费者样本': 'Consumer Sample',
        '(d) 类别选择热力图': '(d) Category Selection Heatmap',
        '(e) 过滤气泡效应': '(e) Filter Bubble Effect',
        '依赖等级': 'Dependency Level',
        '(f) 个体多样性特征': '(f) Individual Diversity Profile',
        '类别覆盖率': 'Category Coverage',
        '多样性干预效果': 'Diversity Intervention Effect',
        '干预前': 'Before Intervention',
        '干预后': 'After Intervention',
    },
    # 实验3-b
    'exp3_consequences/systemic_risk/visualization_systemic_risk.py': {
        '无数据': 'No Data',
        '数据不足': 'Insufficient Data',
        '仿真步数': 'Simulation Step',
        '信任度': 'Trust Level',
        '(a) 信任度演化轨迹': '(a) Trust Evolution Trajectory',
        '平均依赖等级': 'Average Dependency Level',
        '(b) 依赖等级演化': '(b) Dependency Level Evolution',
        '传播速度': 'Propagation Speed',
        '(c) 故障传播过程': '(c) Failure Propagation Process',
        '影响程度': 'Impact Severity',
        '(d) 压力测试场景对比': '(d) Stress Test Scenario Comparison',
        '场景': 'Scenario',
        '信任下降': 'Trust Drop',
        '最大影响': 'Max Impact',
        '恢复时间': 'Recovery Time',
        '(e) 系统韧性雷达图': '(e) System Resilience Radar',
        '级联规模': 'Cascade Size',
        '韧性得分': 'Resilience Score',
    },
}

def fix_file(file_path, replacements):
    """修复单个文件"""
    if not os.path.exists(file_path):
        print(f"⚠ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for chinese, english in replacements.items():
        content = content.replace(chinese, english)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {file_path}")
        return True
    else:
        print(f"- No changes: {file_path}")
        return False

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(base_path, 'abm_simulation', 'experiments')
    
    print("="*70)
    print("批量修复可视化文件 - 中文转英文")
    print("="*70)
    
    total_fixed = 0
    for rel_path, replacements in REPLACEMENTS.items():
        full_path = os.path.join(base_path, rel_path)
        if fix_file(full_path, replacements):
            total_fixed += 1
    
    print("\n" + "="*70)
    print(f"✅ 完成！共修复 {total_fixed} 个文件")
    print("="*70)

if __name__ == '__main__':
    main()
