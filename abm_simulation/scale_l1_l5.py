"""
AI消费决策依赖等级量表 (AI Consumer Decision Delegation Scale, ACDDS)
基于文献开发的L1-L5消费者依赖等级测量工具

理论基础：
- Technology Acceptance Model (Davis, 1989)
- Trust in Automation (Lee & See, 2004)  
- Algorithm Aversion (Dietvorst et al., 2015; Castelo et al., 2019)
- Algorithm Appreciation (Logg et al., 2019)
- The Feeling Economy (Huang et al., 2019)

量表结构：
- 6个维度，22个题项
- 7点Likert量表 (1=非常不同意, 7=非常同意)
- 反向计分题项已标注

作者：ABM消费决策代理研究项目
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np


class DependencyLevel(Enum):
    """AI依赖等级枚举"""
    L1_AUTONOMOUS = 1      # 完全自主型
    L2_INFO_ASSISTED = 2   # 信息辅助型
    L3_SEMI_DELEGATED = 3  # 半委托型
    L4_HIGHLY_DEPENDENT = 4 # 高度依赖型
    L5_FULLY_DELEGATED = 5  # 完全代理型
    
    @classmethod
    def from_index(cls, index: float) -> 'DependencyLevel':
        """从连续指数获取等级"""
        if index < 0.2:
            return cls.L1_AUTONOMOUS
        elif index < 0.4:
            return cls.L2_INFO_ASSISTED
        elif index < 0.6:
            return cls.L3_SEMI_DELEGATED
        elif index < 0.8:
            return cls.L4_HIGHLY_DEPENDENT
        else:
            return cls.L5_FULLY_DELEGATED
    
    @property
    def description(self) -> str:
        """获取等级描述"""
        descriptions = {
            1: "完全自主型 - 完全依靠个人判断，不使用AI推荐",
            2: "信息辅助型 - 主要依靠自己，参考AI建议作为辅助",
            3: "半委托型 - AI和个人判断各占一半权重",
            4: "高度依赖型 - 高度依赖AI推荐，个人判断仅微调",
            5: "完全代理型 - 完全交给AI做决定"
        }
        return descriptions.get(self.value, "未知")
    
    @property
    def description_en(self) -> str:
        """获取英文等级描述"""
        descriptions = {
            1: "Autonomous - Completely rely on personal judgment, do not use AI recommendations",
            2: "Info Assisted - Mainly rely on self, reference AI suggestions as auxiliary",
            3: "Semi Delegated - AI and personal judgment each account for half",
            4: "Highly Dependent - Highly rely on AI recommendations, personal judgment only fine-tunes",
            5: "Fully Delegated - Completely leave decisions to AI"
        }
        return descriptions.get(self.value, "Unknown")


# =============================================================================
# 量表定义
# =============================================================================

SCALE_ITEMS = {
    # =========================================================================
    # 维度A：感知有用性 (Perceived Usefulness, PU)
    # 来源：Davis (1989) - Technology Acceptance Model
    # 理论说明：感知有用性是TAM的核心维度，指用户相信使用某系统能提升其工作绩效的程度
    # =========================================================================
    "PU1": {
        "id": "PU1",
        "text_zh": "使用AI推荐能帮助我做出更好的消费决策",
        "text_en": "Using AI recommendations helps me make better consumption decisions",
        "dimension": "perceived_usefulness",
        "dimension_zh": "感知有用性",
        "dimension_en": "Perceived Usefulness",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PU2": {
        "id": "PU2",
        "text_zh": "AI推荐提高了我的购物效率",
        "text_en": "AI recommendations improve my shopping efficiency",
        "dimension": "perceived_usefulness",
        "dimension_zh": "感知有用性",
        "dimension_en": "Perceived Usefulness",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PU3": {
        "id": "PU3",
        "text_zh": "AI推荐能帮我发现更符合需求的产品",
        "text_en": "AI recommendations help me discover products that better match my needs",
        "dimension": "perceived_usefulness",
        "dimension_zh": "感知有用性",
        "dimension_en": "Perceived Usefulness",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PU4": {
        "id": "PU4",
        "text_zh": "依赖AI推荐能显著节省我的时间和精力",
        "text_en": "Relying on AI recommendations significantly saves my time and effort",
        "dimension": "perceived_usefulness",
        "dimension_zh": "感知有用性",
        "dimension_en": "Perceived Usefulness",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PU5": {
        "id": "PU5",
        "text_zh": "AI推荐提升了我消费决策的整体质量",
        "text_en": "AI recommendations enhance the overall quality of my consumption decisions",
        "dimension": "perceived_usefulness",
        "dimension_zh": "感知有用性",
        "dimension_en": "Perceived Usefulness",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PU6": {
        "id": "PU6",
        "text_zh": "AI推荐增强了我对购买选择的信心",
        "text_en": "AI recommendations increase my confidence in purchase choices",
        "dimension": "perceived_usefulness",
        "dimension_zh": "感知有用性",
        "dimension_en": "Perceived Usefulness",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PU7": {
        "id": "PU7",
        "text_zh": "总体而言，AI推荐系统对我的消费决策非常有用",
        "text_en": "Overall, AI recommendation systems are very useful for my consumption decisions",
        "dimension": "perceived_usefulness",
        "dimension_zh": "感知有用性",
        "dimension_en": "Perceived Usefulness",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    
    # =========================================================================
    # 维度B：感知易用性 (Perceived Ease of Use, PEOU)
    # 来源：Davis (1989) - Technology Acceptance Model
    # 理论说明：感知易用性指用户相信使用某系统将不费力的程度
    # =========================================================================
    "PEOU1": {
        "id": "PEOU1",
        "text_zh": "学习使用AI推荐系统对我来说很容易",
        "text_en": "Learning to use AI recommendation systems is easy for me",
        "dimension": "perceived_ease_of_use",
        "dimension_zh": "感知易用性",
        "dimension_en": "Perceived Ease of Use",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PEOU2": {
        "id": "PEOU2",
        "text_zh": "使用AI推荐进行消费决策无需太多思考",
        "text_en": "Using AI recommendations for consumption decisions requires little mental effort",
        "dimension": "perceived_ease_of_use",
        "dimension_zh": "感知易用性",
        "dimension_en": "Perceived Ease of Use",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PEOU3": {
        "id": "PEOU3",
        "text_zh": "AI推荐系统的交互界面清晰易懂",
        "text_en": "The interaction interface of AI recommendation systems is clear and easy to understand",
        "dimension": "perceived_ease_of_use",
        "dimension_zh": "感知易用性",
        "dimension_en": "Perceived Ease of Use",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PEOU4": {
        "id": "PEOU4",
        "text_zh": "理解AI给出的推荐理由对我来说很容易",
        "text_en": "It is easy for me to understand the reasoning behind AI recommendations",
        "dimension": "perceived_ease_of_use",
        "dimension_zh": "感知易用性",
        "dimension_en": "Perceived Ease of Use",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PEOU5": {
        "id": "PEOU5",
        "text_zh": "使用AI推荐不需要复杂的操作步骤",
        "text_en": "Using AI recommendations does not require complex operational steps",
        "dimension": "perceived_ease_of_use",
        "dimension_zh": "感知易用性",
        "dimension_en": "Perceived Ease of Use",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    "PEOU6": {
        "id": "PEOU6",
        "text_zh": "总体而言，AI推荐系统使用起来很简便",
        "text_en": "Overall, AI recommendation systems are easy to use",
        "dimension": "perceived_ease_of_use",
        "dimension_zh": "感知易用性",
        "dimension_en": "Perceived Ease of Use",
        "source": "Davis (1989) - TAM",
        "reverse": False,
        "weight": 1.0
    },
    
    # =========================================================================
    # 维度C：AI信任 (Trust in AI)
    # 来源：Lee & See (2004) - Trust in Automation
    # 理论说明：Lee & See提出自动化信任的多层次模型，包括能力、可靠性、透明度等维度
    # =========================================================================
    "TR1": {
        "id": "TR1",
        "text_zh": "我相信AI推荐系统具有做出准确推荐的能力",
        "text_en": "I believe AI recommendation systems have the capability to make accurate recommendations",
        "dimension": "trust_in_ai",
        "dimension_zh": "AI信任",
        "dimension_en": "Trust in AI",
        "source": "Lee & See (2004) - Competence Trust",
        "reverse": False,
        "weight": 1.0
    },
    "TR2": {
        "id": "TR2",
        "text_zh": "AI推荐系统的建议通常是可靠的",
        "text_en": "AI recommendation systems' suggestions are usually reliable",
        "dimension": "trust_in_ai",
        "dimension_zh": "AI信任",
        "dimension_en": "Trust in AI",
        "source": "Lee & See (2004) - Reliability",
        "reverse": False,
        "weight": 1.0
    },
    "TR3": {
        "id": "TR3",
        "text_zh": "我能够判断何时应该依赖AI推荐、何时应该自主决策",
        "text_en": "I can judge when to rely on AI recommendations and when to make autonomous decisions",
        "dimension": "trust_in_ai",
        "dimension_zh": "AI信任",
        "dimension_en": "Trust in AI",
        "source": "Lee & See (2004) - Calibration Trust",
        "reverse": False,
        "weight": 1.0
    },
    "TR4": {
        "id": "TR4",
        "text_zh": "AI推荐系统的推荐逻辑是透明可理解的",
        "text_en": "The recommendation logic of AI systems is transparent and understandable",
        "dimension": "trust_in_ai",
        "dimension_zh": "AI信任",
        "dimension_en": "Trust in AI",
        "source": "Lee & See (2004) - Transparency",
        "reverse": False,
        "weight": 1.0
    },
    
    # =========================================================================
    # 维度D：算法态度 (Algorithm Attitude)
    # 来源：
    # - Dietvorst et al. (2015) - Algorithm Aversion
    # - Castelo et al. (2019) - Task Subjectivity
    # - Logg et al. (2019) - Algorithm Appreciation
    # 理论说明：算法厌恶vs算法欣赏的权衡，以及任务类型对算法信任的影响
    # =========================================================================
    "AA1": {
        "id": "AA1",
        "text_zh": "当AI推荐出现错误时，我对它的信任会大幅降低",
        "text_en": "When AI recommendations make errors, my trust in them drops significantly",
        "dimension": "algorithm_attitude",
        "dimension_zh": "算法态度",
        "dimension_en": "Algorithm Attitude",
        "source": "Dietvorst et al. (2015) - Algorithm Aversion",
        "reverse": True,  # 反向计分：算法厌恶越高，依赖度越低
        "weight": 1.0
    },
    "AA2": {
        "id": "AA2",
        "text_zh": "相比人类推荐，我更难以容忍AI推荐的失误",
        "text_en": "Compared to human recommendations, I am less tolerant of AI recommendation errors",
        "dimension": "algorithm_attitude",
        "dimension_zh": "算法态度",
        "dimension_en": "Algorithm Attitude",
        "source": "Dietvorst et al. (2015) - Algorithm Aversion",
        "reverse": True,  # 反向计分
        "weight": 1.0
    },
    "AA3": {
        "id": "AA3",
        "text_zh": "我认为AI比人类更擅长处理消费决策中的信息分析",
        "text_en": "I believe AI is better than humans at processing information analysis in consumption decisions",
        "dimension": "algorithm_attitude",
        "dimension_zh": "算法态度",
        "dimension_en": "Algorithm Attitude",
        "source": "Logg et al. (2019) - Algorithm Appreciation",
        "reverse": False,
        "weight": 1.0
    },
    "AA4": {
        "id": "AA4",
        "text_zh": "在需要客观判断的消费场景中，我更倾向于相信AI",
        "text_en": "In consumption scenarios requiring objective judgment, I am more inclined to trust AI",
        "dimension": "algorithm_attitude",
        "dimension_zh": "算法态度",
        "dimension_en": "Algorithm Attitude",
        "source": "Castelo et al. (2019) - Task Subjectivity",
        "reverse": False,
        "weight": 1.0
    },
    
    # =========================================================================
    # 维度E：自主性与控制 (Autonomy & Control)
    # 来源：Lee & See (2004); Huang et al. (2019) - The Feeling Economy
    # 理论说明：控制需求和对自主性的重视程度影响AI依赖
    # =========================================================================
    "AC1": {
        "id": "AC1",
        "text_zh": "在消费决策中保持个人控制权对我非常重要",
        "text_en": "Maintaining personal control in consumption decisions is very important to me",
        "dimension": "autonomy_control",
        "dimension_zh": "自主性与控制",
        "dimension_en": "Autonomy & Control",
        "source": "Lee & See (2004); Huang et al. (2019)",
        "reverse": True,  # 反向计分：控制需求越高，依赖度越低
        "weight": 1.0
    },
    "AC2": {
        "id": "AC2",
        "text_zh": "我愿意将日常消费决策完全交给AI处理",
        "text_en": "I am willing to completely delegate daily consumption decisions to AI",
        "dimension": "autonomy_control",
        "dimension_zh": "自主性与控制",
        "dimension_en": "Autonomy & Control",
        "source": "Huang et al. (2019) - The Feeling Economy",
        "reverse": False,
        "weight": 1.0
    },
    "AC3": {
        "id": "AC3",
        "text_zh": "即使AI推荐了产品，我仍需要亲自比较和确认",
        "text_en": "Even when AI recommends products, I still need to compare and verify personally",
        "dimension": "autonomy_control",
        "dimension_zh": "自主性与控制",
        "dimension_en": "Autonomy & Control",
        "source": "Lee & See (2004)",
        "reverse": True,  # 反向计分
        "weight": 1.0
    },
    
    # =========================================================================
    # 维度F：社会影响与风险感知 (Social Influence & Risk Perception)
    # 来源：TAM2扩展 (Venkatesh & Davis, 2000); Lee & See (2004)
    # 理论说明：社会影响和风险感知对技术接受的影响
    # =========================================================================
    "SI1": {
        "id": "SI1",
        "text_zh": "我周围的人对AI推荐的使用态度影响了我的选择",
        "text_en": "The attitudes of people around me toward using AI recommendations influence my choices",
        "dimension": "social_influence_risk",
        "dimension_zh": "社会影响与风险感知",
        "dimension_en": "Social Influence & Risk",
        "source": "Venkatesh & Davis (2000) - TAM2 Social Influence",
        "reverse": False,
        "weight": 1.0
    },
    "RP1": {
        "id": "RP1",
        "text_zh": "过度依赖AI推荐可能导致不满意的购买决策",
        "text_en": "Over-reliance on AI recommendations may lead to unsatisfactory purchase decisions",
        "dimension": "social_influence_risk",
        "dimension_zh": "社会影响与风险感知",
        "dimension_en": "Social Influence & Risk",
        "source": "Lee & See (2004) - Risk Perception",
        "reverse": True,  # 反向计分：风险感知越高，依赖度越低
        "weight": 1.0
    },
    "RP2": {
        "id": "RP2",
        "text_zh": "AI推荐可能会限制我接触到的产品多样性",
        "text_en": "AI recommendations may limit the diversity of products I am exposed to",
        "dimension": "social_influence_risk",
        "dimension_zh": "社会影响与风险感知",
        "dimension_en": "Social Influence & Risk",
        "source": "Lee & See (2004) - Risk Perception",
        "reverse": True,  # 反向计分
        "weight": 1.0
    }
}


# =============================================================================
# 维度权重配置
# =============================================================================

DIMENSION_WEIGHTS = {
    "perceived_usefulness": 0.25,      # PU: 核心驱动力
    "perceived_ease_of_use": 0.20,     # PEOU: 使用便利性
    "trust_in_ai": 0.20,               # TR: 信任基础
    "algorithm_attitude": 0.15,        # AA: 算法态度
    "autonomy_control": 0.10,          # AC: 控制需求
    "social_influence_risk": 0.10      # SI/RP: 社会与风险
}

# 维度到中文名称映射
DIMENSION_NAMES_ZH = {
    "perceived_usefulness": "感知有用性",
    "perceived_ease_of_use": "感知易用性",
    "trust_in_ai": "AI信任",
    "algorithm_attitude": "算法态度",
    "autonomy_control": "自主性与控制",
    "social_influence_risk": "社会影响与风险感知"
}

# 维度到英文名称映射
DIMENSION_NAMES_EN = {
    "perceived_usefulness": "Perceived Usefulness",
    "perceived_ease_of_use": "Perceived Ease of Use",
    "trust_in_ai": "Trust in AI",
    "algorithm_attitude": "Algorithm Attitude",
    "autonomy_control": "Autonomy & Control",
    "social_influence_risk": "Social Influence & Risk Perception"
}


# =============================================================================
# 核心计算函数
# =============================================================================

def calculate_dimension_scores(responses: Dict[str, int]) -> Dict[str, float]:
    """
    计算各维度得分
    
    根据问卷回答计算6个维度的标准化得分（1-7分转换为0-1分）
    
    Args:
        responses: 问卷回答字典，键为题项ID，值为1-7的整数
        
    Returns:
        各维度得分字典，键为维度名，值为[0,1]区间的浮点数
        
    Example:
        >>> responses = {
        ...     "PU1": 5, "PU2": 6, "PU3": 5, "PU4": 6, "PU5": 5, "PU6": 6, "PU7": 5,
        ...     "PEOU1": 6, "PEOU2": 5, "PEOU3": 6, "PEOU4": 5, "PEOU5": 6, "PEOU6": 5,
        ...     "TR1": 5, "TR2": 5, "TR3": 4, "TR4": 5,
        ...     "AA1": 3, "AA2": 3, "AA3": 5, "AA4": 5,  # AA1, AA2反向
        ...     "AC1": 3, "AC2": 5, "AC3": 3,  # AC1, AC3反向
        ...     "SI1": 4, "RP1": 3, "RP2": 3  # RP1, RP2反向
        ... }
        >>> scores = calculate_dimension_scores(responses)
    """
    dimension_scores = {dim: [] for dim in DIMENSION_WEIGHTS.keys()}
    
    for item_id, raw_score in responses.items():
        if item_id not in SCALE_ITEMS:
            continue
            
        item = SCALE_ITEMS[item_id]
        dimension = item["dimension"]
        
        # 反向计分处理
        if item["reverse"]:
            adjusted_score = 8 - raw_score  # 7点量表反向: 8 - x
        else:
            adjusted_score = raw_score
            
        dimension_scores[dimension].append(adjusted_score)
    
    # 计算各维度均值并归一化到[0,1]
    result = {}
    for dimension, scores in dimension_scores.items():
        if scores:
            mean_score = np.mean(scores)
            # 从[1,7]归一化到[0,1]
            result[dimension] = (mean_score - 1) / 6
        else:
            result[dimension] = 0.5  # 默认值
            
    return result


def calculate_delegation_index(dimension_scores: Dict[str, float]) -> float:
    """
    计算总依赖度指数
    
    基于各维度加权得分计算连续依赖度指数，范围[0,1]
    
    权重分配依据：
    - 感知有用性 (25%): TAM核心，直接影响使用意愿
    - 感知易用性 (20%): 降低使用门槛
    - AI信任 (20%): 长期依赖的基础
    - 算法态度 (15%): 对算法的心理接受度
    - 自主性与控制 (10%): 控制需求抑制依赖
    - 社会影响与风险 (10%): 外部因素影响
    
    Args:
        dimension_scores: 各维度得分字典
        
    Returns:
        依赖度指数，范围[0,1]
        
    Reference:
        Davis (1989): TAM模型中PU和PEOU是主要预测变量
        Lee & See (2004): 信任是自动化依赖的关键中介变量
    """
    total_weight = sum(DIMENSION_WEIGHTS.values())
    weighted_sum = 0
    
    for dimension, score in dimension_scores.items():
        weight = DIMENSION_WEIGHTS.get(dimension, 0)
        weighted_sum += score * weight
        
    return weighted_sum / total_weight


def classify_level(delegation_index: float) -> int:
    """
    将依赖度指数分类为L1-L5等级
    
    分类阈值：
    - [0.0, 0.2): L1 - 完全自主型
    - [0.2, 0.4): L2 - 信息辅助型
    - [0.4, 0.6): L3 - 半委托型
    - [0.6, 0.8): L4 - 高度依赖型
    - [0.8, 1.0]: L5 - 完全代理型
    
    Args:
        delegation_index: 依赖度指数，范围[0,1]
        
    Returns:
        L级别 (1-5)
        
    Example:
        >>> classify_level(0.15)  # 返回 1
        >>> classify_level(0.55)  # 返回 3
        >>> classify_level(0.85)  # 返回 5
    """
    if delegation_index < 0.2:
        return 1
    elif delegation_index < 0.4:
        return 2
    elif delegation_index < 0.6:
        return 3
    elif delegation_index < 0.8:
        return 4
    else:
        return 5


def scores_to_consumer_traits(dimension_scores: Dict[str, float]) -> Dict[str, float]:
    """
    将量表维度得分映射到仿真系统的7个消费者特质
    
    映射逻辑：
    - tech_acceptance (技术接受度): 综合PU、PEOU和AA
        反映消费者对AI技术的整体接受程度
        
    - trust_tendency (信任倾向): 主要基于TR维度
        反映对AI系统的信任水平
        
    - privacy_concern (隐私关注): 基于AC和RP的反向
        控制需求高、风险感知强的消费者更关注隐私
        
    - control_need (控制需求): 基于AC维度的反向
        自主性需求越高，控制需求越强
        
    - cognitive_laziness (认知惰性): 基于PEOU和AC
        追求便利、不愿自主决策的倾向
        
    - social_conformity (社会遵从性): 基于SI维度
        受周围人影响的程度
        
    - risk_aversion (风险厌恶): 基于RP维度的反向
        风险感知强意味着风险厌恶程度高
    
    Args:
        dimension_scores: 各维度得分字典
        
    Returns:
        消费者特质参数字典，各值范围[0,1]
        
    Reference:
        映射基于理论文献中各构念的关系：
        - Davis (1989): PU和PEOU预测使用行为
        - Lee & See (2004): 信任影响依赖程度
        - Huang et al. (2019): 控制需求与AI依赖负相关
    """
    traits = {}
    
    # 技术接受度：综合有用性、易用性和算法态度
    traits["tech_acceptance"] = np.mean([
        dimension_scores.get("perceived_usefulness", 0.5),
        dimension_scores.get("perceived_ease_of_use", 0.5),
        dimension_scores.get("algorithm_attitude", 0.5)
    ])
    
    # 信任倾向：直接映射AI信任维度
    traits["trust_tendency"] = dimension_scores.get("trust_in_ai", 0.5)
    
    # 隐私关注：基于控制需求和风险感知的反向
    # 控制需求高、风险感知强的消费者更关注隐私
    traits["privacy_concern"] = np.mean([
        1 - dimension_scores.get("autonomy_control", 0.5),
        1 - dimension_scores.get("social_influence_risk", 0.5)
    ])
    
    # 控制需求：自主性维度的反向
    traits["control_need"] = 1 - dimension_scores.get("autonomy_control", 0.5)
    
    # 认知惰性：易用性偏好 + 低控制需求
    traits["cognitive_laziness"] = np.mean([
        dimension_scores.get("perceived_ease_of_use", 0.5),
        dimension_scores.get("autonomy_control", 0.5)
    ])
    
    # 社会遵从性：直接映射社会影响维度
    traits["social_conformity"] = dimension_scores.get("social_influence_risk", 0.5)
    
    # 风险厌恶：风险感知的反向
    traits["risk_aversion"] = 1 - dimension_scores.get("social_influence_risk", 0.5)
    
    # 确保所有值在[0,1]范围内
    for key in traits:
        traits[key] = np.clip(traits[key], 0, 1)
        
    return traits


def generate_scale_report(responses: Dict[str, int]) -> str:
    """
    生成完整的量表分析报告
    
    报告包含：
    1. 基本信息和量表说明
    2. 各维度详细得分
    3. 总依赖度指数
    4. L级别分类结果
    5. 消费者特质参数
    6. 理论解释和建议
    
    Args:
        responses: 问卷回答字典
        
    Returns:
        格式化的分析报告字符串
    """
    # 计算各项得分
    dimension_scores = calculate_dimension_scores(responses)
    delegation_index = calculate_delegation_index(dimension_scores)
    level = classify_level(delegation_index)
    traits = scores_to_consumer_traits(dimension_scores)
    
    # 获取等级描述
    level_enum = DependencyLevel(level)
    
    # 构建报告
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("AI消费决策依赖等级量表 (ACDDS) 分析报告")
    report_lines.append("AI Consumer Decision Delegation Scale Report")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    # 量表说明
    report_lines.append("【量表说明】")
    report_lines.append("本量表基于以下理论文献开发：")
    report_lines.append("  - Davis (1989) - Technology Acceptance Model")
    report_lines.append("  - Lee & See (2004) - Trust in Automation")
    report_lines.append("  - Dietvorst, Simmons & Massey (2015) - Algorithm Aversion")
    report_lines.append("  - Castelo, Bos & Lehmann (2019) - Task Subjectivity")
    report_lines.append("  - Logg, Minson & Moore (2019) - Algorithm Appreciation")
    report_lines.append("  - Huang, Rust & Maksimovic (2019) - The Feeling Economy")
    report_lines.append("")
    
    # 各维度得分
    report_lines.append("【各维度得分】")
    report_lines.append("-" * 50)
    for dim, score in dimension_scores.items():
        dim_zh = DIMENSION_NAMES_ZH.get(dim, dim)
        dim_en = DIMENSION_NAMES_EN.get(dim, dim)
        weight = DIMENSION_WEIGHTS.get(dim, 0)
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        report_lines.append(f"{dim_zh}")
        report_lines.append(f"  {dim_en} (权重: {weight:.0%})")
        report_lines.append(f"  得分: {score:.3f} [{bar}] {score:.1%}")
        report_lines.append("")
    
    # 总依赖度
    report_lines.append("【总依赖度指数】")
    report_lines.append("-" * 50)
    bar = "█" * int(delegation_index * 20) + "░" * (20 - int(delegation_index * 20))
    report_lines.append(f"依赖度指数: {delegation_index:.3f} [{bar}] {delegation_index:.1%}")
    report_lines.append("")
    
    # L级别分类
    report_lines.append("【依赖等级分类】")
    report_lines.append("-" * 50)
    report_lines.append(f"分类结果: L{level} - {level_enum.description}")
    report_lines.append(f"Level: L{level} - {level_enum.description_en}")
    report_lines.append("")
    
    # 等级说明
    report_lines.append("等级划分标准：")
    report_lines.append("  L1 [0.0-0.2): 完全自主型")
    report_lines.append("  L2 [0.2-0.4): 信息辅助型")
    report_lines.append("  L3 [0.4-0.6): 半委托型")
    report_lines.append("  L4 [0.6-0.8): 高度依赖型")
    report_lines.append("  L5 [0.8-1.0]: 完全代理型")
    report_lines.append("")
    
    # 消费者特质参数
    report_lines.append("【消费者特质参数】")
    report_lines.append("-" * 50)
    report_lines.append("(用于ABM仿真系统的参数配置)")
    report_lines.append("")
    for trait, value in traits.items():
        bar = "█" * int(value * 20) + "░" * (20 - int(value * 20))
        trait_names = {
            "tech_acceptance": "技术接受度",
            "trust_tendency": "信任倾向",
            "privacy_concern": "隐私关注",
            "control_need": "控制需求",
            "cognitive_laziness": "认知惰性",
            "social_conformity": "社会遵从性",
            "risk_aversion": "风险厌恶"
        }
        trait_zh = trait_names.get(trait, trait)
        report_lines.append(f"{trait_zh} ({trait}):")
        report_lines.append(f"  {value:.3f} [{bar}] {value:.1%}")
    report_lines.append("")
    
    # 理论解释
    report_lines.append("【理论解释】")
    report_lines.append("-" * 50)
    
    if level == 1:
        report_lines.append("该消费者表现出典型的完全自主型特征：")
        report_lines.append("  - 高度控制需求，重视决策自主权")
        report_lines.append("  - 对AI技术接受度较低")
        report_lines.append("  - 可能表现出算法厌恶倾向")
        report_lines.append("  - 符合Dietvorst et al. (2015)描述的算法厌恶者特征")
    elif level == 2:
        report_lines.append("该消费者表现出信息辅助型特征：")
        report_lines.append("  - 适度使用AI作为信息补充")
        report_lines.append("  - 保持最终决策控制权")
        report_lines.append("  - 对AI能力有合理认知")
        report_lines.append("  - 符合TAM模型中'有用但非必要'的使用模式")
    elif level == 3:
        report_lines.append("该消费者表现出半委托型特征：")
        report_lines.append("  - 在AI建议和个人判断间寻求平衡")
        report_lines.append("  - 信任与控制的折中状态")
        report_lines.append("  - 可能根据情境调整依赖程度")
        report_lines.append("  - 符合Lee & See (2004)的'校准信任'概念")
    elif level == 4:
        report_lines.append("该消费者表现出高度依赖型特征：")
        report_lines.append("  - 高度信任AI推荐能力")
        report_lines.append("  - 个人判断仅作微调")
        report_lines.append("  - 感知AI在信息处理上的优势")
        report_lines.append("  - 符合Logg et al. (2019)的算法欣赏现象")
    else:
        report_lines.append("该消费者表现出完全代理型特征：")
        report_lines.append("  - 完全委托AI进行决策")
        report_lines.append("  - 极低的控制需求")
        report_lines.append("  - 高度认知惰性")
        report_lines.append("  - 符合Huang et al. (2019)描述的'感觉经济'参与者")
    
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("报告生成完成")
    report_lines.append("=" * 70)
    
    return "\n".join(report_lines)


def get_questionnaire_text(language: str = 'zh') -> str:
    """
    输出可直接使用的问卷文本
    
    Args:
        language: 语言代码，'zh'为中文，'en'为英文
        
    Returns:
        格式化的问卷文本
        
    Example:
        >>> print(get_questionnaire_text('zh'))  # 中文问卷
        >>> print(get_questionnaire_text('en'))  # 英文问卷
    """
    lines = []
    
    if language == 'zh':
        lines.append("=" * 70)
        lines.append("AI消费决策依赖等级量表 (ACDDS)")
        lines.append("=" * 70)
        lines.append("")
        lines.append("指导语：")
        lines.append("本问卷旨在了解您对AI推荐系统的态度和使用倾向。")
        lines.append("请根据您的真实想法，在1-7分中选择最符合您情况的分数。")
        lines.append("1 = 非常不同意，7 = 非常同意")
        lines.append("")
        lines.append("-" * 70)
        
        current_dimension = None
        for item_id, item in SCALE_ITEMS.items():
            # 新维度标题
            if item["dimension"] != current_dimension:
                current_dimension = item["dimension"]
                lines.append("")
                lines.append(f"【{item['dimension_zh']}】")
                lines.append(f"({item['dimension_en']})")
                lines.append(f"来源：{item['source']}")
                lines.append("")
            
            # 题项
            reverse_note = " [反向计分]" if item["reverse"] else ""
            lines.append(f"{item_id}. {item['text_zh']}{reverse_note}")
            lines.append("    1    2    3    4    5    6    7")
            lines.append("  非常不同意              非常同意")
            lines.append("")
            
    else:  # English
        lines.append("=" * 70)
        lines.append("AI Consumer Decision Delegation Scale (ACDDS)")
        lines.append("=" * 70)
        lines.append("")
        lines.append("Instructions:")
        lines.append("This questionnaire aims to understand your attitudes toward AI")
        lines.append("recommendation systems. Please select the score (1-7) that best")
        lines.append("reflects your true feelings.")
        lines.append("1 = Strongly Disagree, 7 = Strongly Agree")
        lines.append("")
        lines.append("-" * 70)
        
        current_dimension = None
        for item_id, item in SCALE_ITEMS.items():
            if item["dimension"] != current_dimension:
                current_dimension = item["dimension"]
                lines.append("")
                lines.append(f"[{item['dimension_en']}]")
                lines.append(f"Source: {item['source']}")
                lines.append("")
            
            reverse_note = " [Reverse Scored]" if item["reverse"] else ""
            lines.append(f"{item_id}. {item['text_en']}{reverse_note}")
            lines.append("    1      2      3      4      5      6      7")
            lines.append("  Strongly Disagree              Strongly Agree")
            lines.append("")
    
    return "\n".join(lines)


def validate_responses(responses: Dict[str, int]) -> Tuple[bool, List[str]]:
    """
    验证问卷回答的有效性
    
    检查项：
    - 所有题项是否都已回答
    - 回答值是否在有效范围内(1-7)
    - 是否有异常回答模式
    
    Args:
        responses: 问卷回答字典
        
    Returns:
        (是否有效, 错误信息列表)
    """
    errors = []
    
    # 检查是否包含所有题项
    missing_items = set(SCALE_ITEMS.keys()) - set(responses.keys())
    if missing_items:
        errors.append(f"缺少题项: {', '.join(sorted(missing_items))}")
    
    # 检查回答值范围
    for item_id, score in responses.items():
        if item_id in SCALE_ITEMS:
            if not isinstance(score, (int, float)):
                errors.append(f"{item_id}: 回答必须是数字")
            elif score < 1 or score > 7:
                errors.append(f"{item_id}: 回答值 {score} 超出有效范围[1-7]")
    
    # 检查异常模式：所有回答相同
    if len(set(responses.values())) == 1:
        errors.append("警告：所有回答相同，可能存在敷衍作答")
    
    # 检查异常模式：回答波动过大
    if len(responses) >= 5:
        values = list(responses.values())
        if max(values) - min(values) <= 1:
            errors.append("警告：回答波动过小，可能存在一致性偏差")
    
    return len(errors) == 0, errors


def get_scale_statistics() -> Dict:
    """
    获取量表的统计信息
    
    Returns:
        量表统计信息字典
    """
    return {
        "total_items": len(SCALE_ITEMS),
        "dimensions": list(DIMENSION_WEIGHTS.keys()),
        "n_dimensions": len(DIMENSION_WEIGHTS),
        "items_per_dimension": {
            dim: len([i for i in SCALE_ITEMS.values() if i["dimension"] == dim])
            for dim in DIMENSION_WEIGHTS.keys()
        },
        "reverse_items": [k for k, v in SCALE_ITEMS.items() if v["reverse"]],
        "n_reverse_items": sum(1 for v in SCALE_ITEMS.values() if v["reverse"]),
        "scale_range": "1-7 (Likert)",
        "theoretical_sources": [
            "Davis (1989) - TAM",
            "Lee & See (2004) - Trust in Automation",
            "Dietvorst et al. (2015) - Algorithm Aversion",
            "Castelo et al. (2019) - Task Subjectivity",
            "Logg et al. (2019) - Algorithm Appreciation",
            "Huang et al. (2019) - The Feeling Economy"
        ]
    }


# =============================================================================
# 便捷函数
# =============================================================================

def quick_assess(responses: Dict[str, int]) -> Dict:
    """
    快速评估函数 - 一站式计算所有指标
    
    Args:
        responses: 问卷回答字典
        
    Returns:
        包含所有评估结果的字典
    """
    dimension_scores = calculate_dimension_scores(responses)
    delegation_index = calculate_delegation_index(dimension_scores)
    level = classify_level(delegation_index)
    traits = scores_to_consumer_traits(dimension_scores)
    
    return {
        "dimension_scores": dimension_scores,
        "delegation_index": delegation_index,
        "level": level,
        "level_description": DependencyLevel(level).description,
        "traits": traits,
        "is_valid": validate_responses(responses)[0]
    }


def create_consumer_from_responses(responses: Dict[str, int], agent_id: int = 0) -> Dict:
    """
    从问卷回答创建消费者智能体配置
    
    返回可直接用于ConsumerAgentDIB初始化的参数字典
    
    Args:
        responses: 问卷回答字典
        agent_id: 智能体ID
        
    Returns:
        消费者智能体配置字典
    """
    result = quick_assess(responses)
    
    return {
        "agent_id": agent_id,
        "initial_level": result["level"],
        "traits": result["traits"],
        "delegation_index": result["delegation_index"],
        "dimension_scores": result["dimension_scores"]
    }


# =============================================================================
# 模块测试
# =============================================================================

if __name__ == "__main__":
    # 示例：L3级别消费者的典型回答模式
    example_responses = {
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
    
    print("=" * 70)
    print("ACDDS量表系统测试")
    print("=" * 70)
    print()
    
    # 验证回答
    is_valid, errors = validate_responses(example_responses)
    print(f"回答有效性: {'有效' if is_valid else '无效'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    print()
    
    # 生成报告
    report = generate_scale_report(example_responses)
    print(report)
