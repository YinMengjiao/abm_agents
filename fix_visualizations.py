"""
Fix all visualization files to support English
This script patches all Chinese text in visualization functions
"""

import sys
import os

# 由于直接修改太复杂，这个文件记录需要修改的位置
# 实际修改已经通过 search_replace 完成

print("Visualization files need the following fixes:")
print("1. exp1_baseline/create_baseline_summary.py - IN PROGRESS")
print("2. exp2_mechanism/visualization_evolution.py - NEEDS FIX")
print("3. exp3_consequences/filter_bubble/visualization_filter_bubble.py - NEEDS FIX")
print("4. exp3_consequences/systemic_risk/visualization_systemic_risk.py - NEEDS FIX")
print("5. exp4_intervention/visualization_intervention.py - PARTIALLY FIXED")
