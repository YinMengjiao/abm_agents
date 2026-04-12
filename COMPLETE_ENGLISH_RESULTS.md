# ABM Simulation - Complete English Results Summary

## Execution Date
Generated on: 2026-04-12

## Data Source
- **File**: `data_survey/acdds_with_demographics.csv`
- **Sample Size**: 577 cases
- **Demographics**:
  - Gender: Male 293 (50.8%), Female 284 (49.2%)
  - Age: 14-52 years (Mean: 32.4 years)
  - Education: Low 112 (19.4%), Medium 285 (49.4%), High 180 (31.2%)

## Initial Dependency Level Distribution (Survey-Driven)
- L1 (Autonomous): 39 (6.8%)
- L2 (Information Assist): 149 (25.8%)
- L3 (Semi-delegated): 228 (39.5%)
- L4 (High Dependency): 134 (23.2%)
- L5 (Full Agency): 27 (4.7%)

## Simulation Configuration
- Consumers: 500
- Merchants: 20
- AI Agents: 3
- Simulation Steps: 300 (200 for comparison)
- Network Type: small_world
- Language: **English**

---

## Experiment Results

### ✅ Experiment 1: Baseline Dynamics
- **Status**: Completed
- **Output**: `results/exp1_baseline/baseline_summary.png` (529.2 KB)
- **Description**: Ising-D-I-B baseline model with adaptive coupling
- **Content**: 3×3 comprehensive analysis grid including:
  - Initial/Final level distribution
  - Level evolution
  - Magnetization dynamics
  - Coupling strength evolution
  - Phase transition analysis
  - Satisfaction evolution
  - AI usage & error rate
  - Network topology features

### ✅ Experiment 2: AI Agent Evolution
- **Status**: Completed
- **Output**: `results/exp2_mechanism/evolution_analysis.png` (227.5 KB)
- **Key Findings**:
  - Error rate reduction: 0.078 → 0.016
  - Evolution progress: 0.001 → 0.257
  - Consumer trust recovery: 0.360
  - Total learning events: 115,662

### ✅ Experiment 3-a: Filter Bubble
- **Status**: Completed
- **Output**: `results/exp3_consequences/filter_bubble/filter_bubble_analysis.png` (223 KB)
- **Key Findings**:
  - Overall diversity score: 0.872
  - Filter bubble strength: 0.115
  - High vs Low dependency difference: -0.230
  - Intervention improvement: +14.6%

### ✅ Experiment 3-b: Systemic Risk
- **Status**: Completed
- **Output**: `results/exp3_consequences/systemic_risk/systemic_risk_analysis.png` (202.4 KB)
- **Key Findings**:
  - Major breach max impact: 174 consumers
  - Critical failure max impact: 243 consumers
  - Coordinated attack max impact: 245 consumers
  - System resilience score: 4.977

### ✅ Experiment 4: Information Intervention
- **Status**: Completed
- **Output**: `results/exp4_intervention/intervention_all_policies.png` (793.3 KB)
- **Policy Comparison**:
  - **Balanced**: L2=39.2%, L3=27.4%, L4=33.4%, Satisfaction=0.310
  - **Pro-AI**: L2=40.0%, L3=21.6%, L4=38.4%, Satisfaction=0.310
  - **Consumer Protection**: L2=50.8%, L3=22.4%, L4=26.8%, Satisfaction=0.281

### ✅ Comparison Experiment: Survey vs Theoretical Initialization
- **Status**: Completed
- **Output**: `results/exp_comparison_init/initialization_comparison.png` (378.9 KB)
- **Description**: Comparison between survey-driven and theoretical initialization
- **Content**: 6-panel visualization including:
  - Sankey diagrams (Survey & Theoretical flows)
  - Initial distribution comparison
  - Final distribution comparison
  - Level evolution comparison
  - Magnetization evolution comparison
  - Satisfaction evolution comparison
  - Key metrics boxplot comparison
- **Runs**: 10 repetitions per group (20 total simulations)

---

## Generated Figures (English Version)

All figures are generated in **English** and stored in the unified output directory:

| # | Figure | Size | Path |
|---|--------|------|------|
| 1 | Baseline Summary | 529.2 KB | `results/exp1_baseline/baseline_summary.png` |
| 2 | Evolution Analysis | 227.5 KB | `results/exp2_mechanism/evolution_analysis.png` |
| 3 | Filter Bubble Analysis | 223 KB | `results/exp3_consequences/filter_bubble/filter_bubble_analysis.png` |
| 4 | Systemic Risk Analysis | 202.4 KB | `results/exp3_consequences/systemic_risk/systemic_risk_analysis.png` |
| 5 | Intervention Policies | 793.3 KB | `results/exp4_intervention/intervention_all_policies.png` |
| 6 | Initialization Comparison | 378.9 KB | `results/exp_comparison_init/initialization_comparison.png` |

## Total Output
- **Total Experiments**: 6 (all successful)
- **Total Figures**: 6 PNG files
- **Total Size**: ~2.35 MB
- **Language**: English (complete localization)

## Code Modifications

### Files Modified for English Support:
1. ✅ `exp1_baseline/create_baseline_summary.py` - Complete rewrite with full English support
2. ✅ `exp1_baseline/run_baseline.py` - Added `en` parameter
3. ✅ `exp2_mechanism/visualization_evolution.py` - Batch replaced 15 Chinese texts
4. ✅ `exp3_consequences/filter_bubble/visualization_filter_bubble.py` - Batch replaced 16 Chinese texts
5. ✅ `exp3_consequences/systemic_risk/visualization_systemic_risk.py` - Batch replaced 15 Chinese texts
6. ✅ `exp4_intervention/visualization_intervention.py` - Already had partial English support
7. ✅ `exp_comparison_init/visualization_comparison.py` - Modified to use unified output path
8. ✅ `config.py` - Added `exp_comparison` output path

### Output Path Unification:
All experiments now output to the unified `abm_simulation/results/` directory structure:
```
results/
├── exp1_baseline/
├── exp2_mechanism/
├── exp3_consequences/
│   ├── filter_bubble/
│   └── systemic_risk/
├── exp4_intervention/
└── exp_comparison_init/  ← NEW
```

## Notes
- All visualizations use **English** labels, titles, and legends
- Data initialization based on ACDDS survey with demographics
- Dependency levels calculated using PU (Perceived Usefulness) and TR (Trust) scores
- All simulations successfully completed without errors
- Comparison experiment uses existing results from previous runs (10 runs per group)
- Batch replacement script (`batch_fix_visualizations.py`) used for efficient localization

## How to Run
```bash
# Run all experiments with English output
python run_all_experiments_english.py

# Or run comparison experiment visualization only
cd abm_simulation/experiments/exp_comparison_init
python visualization_comparison.py --en
```
