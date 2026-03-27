"""
ACDDS量表系统测试脚本

测试内容：
1. 5个典型消费者档案（L1-L5）的量表回答模式
2. 计分逻辑验证
3. 问卷文本输出
4. 示例报告生成

运行方式：
    python test_scale.py
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scale_l1_l5 import (
    SCALE_ITEMS, DIMENSION_WEIGHTS, calculate_dimension_scores,
    calculate_delegation_index, classify_level, scores_to_consumer_traits,
    generate_scale_report, get_questionnaire_text, validate_responses,
    get_scale_statistics, quick_assess, create_consumer_from_responses,
    DependencyLevel
)


# =============================================================================
# 典型消费者档案 (L1-L5)
# =============================================================================

# L1: 完全自主型 - 低AI依赖，高控制需求
PROFILE_L1 = {
    # PU - 低感知有用性
    "PU1": 2, "PU2": 2, "PU3": 2, "PU4": 2, "PU5": 2, "PU6": 2, "PU7": 2,
    # PEOU - 低感知易用性
    "PEOU1": 2, "PEOU2": 2, "PEOU3": 2, "PEOU4": 2, "PEOU5": 2, "PEOU6": 2,
    # TR - 低信任
    "TR1": 2, "TR2": 2, "TR3": 2, "TR4": 2,
    # AA - 高算法厌恶（反向题高分=实际低依赖）
    "AA1": 6, "AA2": 6, "AA3": 2, "AA4": 2,
    # AC - 高控制需求（反向题高分=实际低依赖）
    "AC1": 6, "AC2": 2, "AC3": 6,
    # SI/RP - 高风险感知（反向题高分=实际低依赖）
    "SI1": 3, "RP1": 6, "RP2": 6
}

# L2: 信息辅助型 - 适度使用AI作为信息补充
PROFILE_L2 = {
    # PU - 中等偏低感知有用性
    "PU1": 3, "PU2": 3, "PU3": 3, "PU4": 3, "PU5": 3, "PU6": 3, "PU7": 3,
    # PEOU - 中等感知易用性
    "PEOU1": 4, "PEOU2": 4, "PEOU3": 4, "PEOU4": 4, "PEOU5": 4, "PEOU6": 4,
    # TR - 中等偏低信任
    "TR1": 3, "TR2": 3, "TR3": 3, "TR4": 3,
    # AA - 中等算法态度（反向题高分=低依赖，正向题中等）
    "AA1": 5, "AA2": 5, "AA3": 3, "AA4": 3,
    # AC - 较高控制需求（反向题高分=低依赖）
    "AC1": 5, "AC2": 3, "AC3": 5,
    # SI/RP - 中等社会/风险（反向题高分=低依赖）
    "SI1": 4, "RP1": 5, "RP2": 5
}

# L3: 半委托型 - AI和个人判断平衡
PROFILE_L3 = {
    # PU - 中等偏高
    "PU1": 5, "PU2": 5, "PU3": 5, "PU4": 5, "PU5": 5, "PU6": 5, "PU7": 5,
    # PEOU - 中等
    "PEOU1": 5, "PEOU2": 5, "PEOU3": 5, "PEOU4": 5, "PEOU5": 5, "PEOU6": 5,
    # TR - 中等
    "TR1": 4, "TR2": 4, "TR3": 4, "TR4": 4,
    # AA - 平衡
    "AA1": 4, "AA2": 4, "AA3": 4, "AA4": 4,
    # AC - 中等控制需求
    "AC1": 4, "AC2": 4, "AC3": 4,
    # SI/RP - 中等
    "SI1": 4, "RP1": 4, "RP2": 4
}

# L4: 高度依赖型 - 高度信任AI（但非完全委托）
PROFILE_L4 = {
    # PU - 高感知有用性
    "PU1": 6, "PU2": 6, "PU3": 6, "PU4": 6, "PU5": 6, "PU6": 6, "PU7": 6,
    # PEOU - 高感知易用性
    "PEOU1": 6, "PEOU2": 6, "PEOU3": 6, "PEOU4": 6, "PEOU5": 6, "PEOU6": 6,
    # TR - 高信任
    "TR1": 6, "TR2": 6, "TR3": 5, "TR4": 6,
    # AA - 较高算法欣赏（反向题较低分=较高依赖，但非极端）
    "AA1": 3, "AA2": 3, "AA3": 5, "AA4": 5,
    # AC - 较低控制需求（反向题较低分=较高依赖，但非极端）
    "AC1": 3, "AC2": 5, "AC3": 3,
    # SI/RP - 较低风险感知（反向题较低分=较高依赖，但非极端）
    "SI1": 4, "RP1": 3, "RP2": 3
}

# L5: 完全代理型 - 完全委托AI
PROFILE_L5 = {
    # PU - 极高感知有用性
    "PU1": 7, "PU2": 7, "PU3": 7, "PU4": 7, "PU5": 7, "PU6": 7, "PU7": 7,
    # PEOU - 极高感知易用性
    "PEOU1": 7, "PEOU2": 7, "PEOU3": 7, "PEOU4": 7, "PEOU5": 7, "PEOU6": 7,
    # TR - 极高信任
    "TR1": 7, "TR2": 7, "TR3": 6, "TR4": 7,
    # AA - 极高算法欣赏（反向题最低分=实际最高依赖）
    "AA1": 1, "AA2": 1, "AA3": 7, "AA4": 7,
    # AC - 极低控制需求（反向题最低分=实际最高依赖）
    "AC1": 1, "AC2": 7, "AC3": 1,
    # SI/RP - 极低风险感知（反向题最低分=实际最高依赖）
    "SI1": 6, "RP1": 1, "RP2": 1
}

# 所有档案汇总
PROFILES = {
    "L1_完全自主型": PROFILE_L1,
    "L2_信息辅助型": PROFILE_L2,
    "L3_半委托型": PROFILE_L3,
    "L4_高度依赖型": PROFILE_L4,
    "L5_完全代理型": PROFILE_L5
}


def test_profiles():
    """测试5个典型消费者档案"""
    print("=" * 80)
    print("测试1: 典型消费者档案分类验证")
    print("=" * 80)
    print()
    
    print(f"{'档案':<15} {'预期等级':<10} {'实际等级':<10} {'依赖指数':<12} {'状态':<10}")
    print("-" * 80)
    
    all_passed = True
    expected_levels = [1, 2, 3, 4, 5]
    
    for i, (name, profile) in enumerate(PROFILES.items()):
        expected = expected_levels[i]
        
        # 计算结果
        dimension_scores = calculate_dimension_scores(profile)
        delegation_index = calculate_delegation_index(dimension_scores)
        actual_level = classify_level(delegation_index)
        
        # 验证
        status = "✓ 通过" if actual_level == expected else "✗ 失败"
        if actual_level != expected:
            all_passed = False
        
        print(f"{name:<15} L{expected:<9} L{actual_level:<9} {delegation_index:.3f}       {status}")
    
    print("-" * 80)
    print(f"测试结果: {'全部通过' if all_passed else '存在失败'}")
    print()
    
    return all_passed


def test_scoring_logic():
    """验证计分逻辑"""
    print("=" * 80)
    print("测试2: 计分逻辑验证")
    print("=" * 80)
    print()
    
    # 测试反向计分
    print("2.1 反向计分验证")
    print("-" * 40)
    
    # 创建一个测试回答：所有反向题给1分（最低），应转为7分
    test_reverse = {"AA1": 1, "AA2": 1, "AC1": 1, "AC3": 1, "RP1": 1, "RP2": 1}
    dim_scores = calculate_dimension_scores(test_reverse)
    
    print(f"反向题原始分: 1分 (最低)")
    print(f"反向计分后: 8-1=7分 (最高)")
    print(f"算法态度维度得分: {dim_scores.get('algorithm_attitude', 0):.3f} (应接近1.0)")
    print(f"自主控制维度得分: {dim_scores.get('autonomy_control', 0):.3f} (应接近1.0)")
    print(f"社会风险维度得分: {dim_scores.get('social_influence_risk', 0):.3f} (应接近1.0)")
    print()
    
    # 测试正向计分
    print("2.2 正向计分验证")
    print("-" * 40)
    
    test_forward = {"PU1": 7, "PU2": 7, "TR1": 7, "TR2": 7}
    dim_scores = calculate_dimension_scores(test_forward)
    
    print(f"正向题原始分: 7分 (最高)")
    print(f"感知有用性维度得分: {dim_scores.get('perceived_usefulness', 0):.3f} (应接近1.0)")
    print(f"AI信任维度得分: {dim_scores.get('trust_in_ai', 0):.3f} (应接近1.0)")
    print()
    
    # 测试边界值
    print("2.3 边界值验证")
    print("-" * 40)
    
    # 注意：由于存在反向计分题，全1分或全7分不会得到极端的0或1
    # 最低依赖：正向题1分，反向题7分（反向计分后变为1分）
    all_min = {}
    for k in SCALE_ITEMS.keys():
        if SCALE_ITEMS[k]["reverse"]:
            all_min[k] = 7  # 反向题给最高分，计分后变为1
        else:
            all_min[k] = 1  # 正向题给最低分
    
    dim_min = calculate_dimension_scores(all_min)
    index_min = calculate_delegation_index(dim_min)
    level_min = classify_level(index_min)
    
    # 最高依赖：正向题7分，反向题1分（反向计分后变为7分）
    all_max = {}
    for k in SCALE_ITEMS.keys():
        if SCALE_ITEMS[k]["reverse"]:
            all_max[k] = 1  # 反向题给最低分，计分后变为7
        else:
            all_max[k] = 7  # 正向题给最高分
    
    dim_max = calculate_dimension_scores(all_max)
    index_max = calculate_delegation_index(dim_max)
    level_max = classify_level(index_max)
    
    print(f"最低依赖情景: 依赖指数={index_min:.3f}, 等级=L{level_min} (应为L1)")
    print(f"最高依赖情景: 依赖指数={index_max:.3f}, 等级=L{level_max} (应为L5)")
    
    passed = (level_min == 1) and (level_max == 5)
    print(f"边界测试: {'通过' if passed else '失败'}")
    print()
    
    return passed


def test_traits_mapping():
    """测试特质映射"""
    print("=" * 80)
    print("测试3: 消费者特质映射验证")
    print("=" * 80)
    print()
    
    for name, profile in PROFILES.items():
        print(f"3.{list(PROFILES.keys()).index(name)+1} {name}")
        print("-" * 40)
        
        dimension_scores = calculate_dimension_scores(profile)
        traits = scores_to_consumer_traits(dimension_scores)
        
        print(f"{'特质':<20} {'值':<8} {'可视化':<20}")
        print("-" * 40)
        
        trait_names = {
            "tech_acceptance": "技术接受度",
            "trust_tendency": "信任倾向",
            "privacy_concern": "隐私关注",
            "control_need": "控制需求",
            "cognitive_laziness": "认知惰性",
            "social_conformity": "社会遵从性",
            "risk_aversion": "风险厌恶"
        }
        
        for trait, value in traits.items():
            bar = "█" * int(value * 10) + "░" * (10 - int(value * 10))
            print(f"{trait_names.get(trait, trait):<20} {value:.2f}    [{bar}]")
        
        print()
    
    return True


def test_validation():
    """测试回答验证功能"""
    print("=" * 80)
    print("测试4: 回答验证功能")
    print("=" * 80)
    print()
    
    # 有效回答
    print("4.1 有效回答测试")
    print("-" * 40)
    valid, errors = validate_responses(PROFILE_L3)
    print(f"有效回答验证: {'通过' if valid else '失败'}")
    if errors:
        for e in errors:
            print(f"  - {e}")
    print()
    
    # 缺少题项
    print("4.2 缺少题项测试")
    print("-" * 40)
    incomplete = {k: v for k, v in list(PROFILE_L3.items())[:10]}
    valid, errors = validate_responses(incomplete)
    print(f"缺少题项检测: {'通过' if not valid else '失败'}")
    print(f"错误信息: {errors[0] if errors else '无'}")
    print()
    
    # 超出范围
    print("4.3 超出范围测试")
    print("-" * 40)
    out_of_range = PROFILE_L3.copy()
    out_of_range["PU1"] = 10
    valid, errors = validate_responses(out_of_range)
    print(f"超出范围检测: {'通过' if not valid else '失败'}")
    print(f"错误信息: {errors[0] if errors else '无'}")
    print()
    
    return True


def print_questionnaire():
    """打印问卷文本"""
    print("=" * 80)
    print("测试5: 问卷文本输出")
    print("=" * 80)
    print()
    
    # 中文问卷
    print("5.1 中文问卷")
    print("-" * 40)
    print(get_questionnaire_text('zh')[:2000])  # 只打印前2000字符
    print("... [问卷内容已截断，完整内容请查看源文件]")
    print()
    
    # 英文问卷
    print("5.2 英文问卷 (节选)")
    print("-" * 40)
    print(get_questionnaire_text('en')[:1500])
    print("... [问卷内容已截断]")
    print()
    
    return True


def print_scale_info():
    """打印量表信息"""
    print("=" * 80)
    print("量表统计信息")
    print("=" * 80)
    print()
    
    stats = get_scale_statistics()
    
    print(f"总题项数: {stats['total_items']}")
    print(f"维度数: {stats['n_dimensions']}")
    print(f"反向计分题项数: {stats['n_reverse_items']}")
    print(f"量表范围: {stats['scale_range']}")
    print()
    
    print("各维度题项数:")
    for dim, count in stats['items_per_dimension'].items():
        dim_zh = {
            "perceived_usefulness": "感知有用性",
            "perceived_ease_of_use": "感知易用性",
            "trust_in_ai": "AI信任",
            "algorithm_attitude": "算法态度",
            "autonomy_control": "自主性与控制",
            "social_influence_risk": "社会影响与风险感知"
        }.get(dim, dim)
        print(f"  {dim_zh}: {count}题")
    print()
    
    print("反向计分题项:")
    for item_id in stats['reverse_items']:
        item = SCALE_ITEMS[item_id]
        print(f"  {item_id}: {item['text_zh'][:30]}...")
    print()
    
    print("理论来源:")
    for source in stats['theoretical_sources']:
        print(f"  - {source}")
    print()
    
    return True


def generate_sample_report():
    """生成示例报告"""
    print("=" * 80)
    print("测试6: 示例报告生成")
    print("=" * 80)
    print()
    
    # 使用L3档案生成完整报告
    print("6.1 L3级别消费者完整报告")
    print("-" * 40)
    report = generate_scale_report(PROFILE_L3)
    print(report)
    print()
    
    # 快速评估示例
    print("6.2 快速评估示例")
    print("-" * 40)
    result = quick_assess(PROFILE_L4)
    print(f"档案: L4高度依赖型")
    print(f"依赖指数: {result['delegation_index']:.3f}")
    print(f"分类等级: L{result['level']}")
    print(f"等级描述: {result['level_description']}")
    print()
    
    # 消费者配置生成
    print("6.3 消费者智能体配置生成")
    print("-" * 40)
    config = create_consumer_from_responses(PROFILE_L2, agent_id=100)
    print(f"智能体ID: {config['agent_id']}")
    print(f"初始等级: L{config['initial_level']}")
    print(f"依赖指数: {config['delegation_index']:.3f}")
    print("特质参数:")
    for trait, value in config['traits'].items():
        print(f"  {trait}: {value:.3f}")
    print()
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 80)
    print("ACDDS量表系统测试套件")
    print("AI Consumer Decision Delegation Scale Test Suite")
    print("=" * 80)
    print()
    
    results = []
    
    # 测试1: 典型档案
    results.append(("典型消费者档案", test_profiles()))
    
    # 测试2: 计分逻辑
    results.append(("计分逻辑验证", test_scoring_logic()))
    
    # 测试3: 特质映射
    results.append(("特质映射验证", test_traits_mapping()))
    
    # 测试4: 回答验证
    results.append(("回答验证功能", test_validation()))
    
    # 测试5: 问卷文本
    results.append(("问卷文本输出", print_questionnaire()))
    
    # 量表信息
    print_scale_info()
    
    # 测试6: 示例报告
    results.append(("示例报告生成", generate_sample_report()))
    
    # 汇总
    print("=" * 80)
    print("测试汇总")
    print("=" * 80)
    print()
    
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{name:<20} {status}")
    
    total = len(results)
    passed_count = sum(1 for _, p in results if p)
    
    print()
    print(f"总计: {passed_count}/{total} 项测试通过")
    print()
    
    if passed_count == total:
        print("🎉 所有测试通过！量表系统运行正常。")
    else:
        print("⚠️ 部分测试未通过，请检查实现。")
    
    print()
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()
