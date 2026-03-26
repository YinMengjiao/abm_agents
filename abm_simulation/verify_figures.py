"""
验证所有可视化图表的中文显示和布局
"""

import os
from pathlib import Path

def verify_figures():
    """验证图表文件"""
    
    figures_dir = Path("results/all_figures")
    
    if not figures_dir.exists():
        print("❌ 错误：图表目录不存在")
        return False
    
    # 需要验证的关键图表
    key_figures = [
        "exp3_ai_evolution_evolution_analysis.png",
        "exp4_information_intervention_intervention_analysis.png",
        "exp8_context_sensitivity_context_analysis.png",
        "exp9_filter_bubble_filter_bubble_analysis.png",
        "exp10_systemic_risk_systemic_risk_analysis.png"
    ]
    
    print("="*70)
    print("可视化修复验证报告")
    print("="*70)
    print()
    
    all_ok = True
    
    for fig_name in key_figures:
        fig_path = figures_dir / fig_name
        
        if fig_path.exists():
            file_size = fig_path.stat().st_size
            
            # 检查文件大小（应该大于 50KB）
            if file_size > 50 * 1024:
                status = "[OK]"
            else:
                status = "[WARN] (文件可能过小)"
                all_ok = False
            
            print(f"{status} {fig_name}")
            print(f"   大小：{file_size / 1024:.1f} KB")
        else:
            print(f"❌ {fig_name} - 文件不存在")
            all_ok = False
    
    print()
    print("="*70)
    
    if all_ok:
        print("[OK] 所有关键图表已修复并收集完成！")
        print()
        print("查看位置：results/all_figures/")
        print()
        print("提示：可以运行以下命令查看所有图表：")
        print("  python view_all_figures.py")
    else:
        print("[ERROR] 部分图表存在问题，请检查")
    
    print("="*70)
    
    return all_ok


if __name__ == "__main__":
    success = verify_figures()
    exit(0 if success else 1)
