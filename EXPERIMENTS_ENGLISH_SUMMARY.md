# ABM Simulation Experiments - English Results Summary

## Execution Date
Generated on: 2026-04-12

## Data Source
- **File**: `data_survey/acdds_with_demographics.csv`
- **Sample Size**: 577 cases
- **Demographics**:
  - Gender: Male 293 (50.8%), Female 284 (49.2%)
  - Age: 14-52 years (Mean: 32.4 years)
  - Education: Low 112 (19.4%), Medium 285 (49.4%), High 180 (31.2%)

## Initial Dependency Level Distribution
- L1 (Autonomous): 39 (6.8%)
- L2 (Information Assist): 149 (25.8%)
- L3 (Semi-delegated): 228 (39.5%)
- L4 (High Dependency): 134 (23.2%)
- L5 (Full Agency): 27 (4.7%)

## Simulation Configuration
- Consumers: 500
- Merchants: 20
- AI Agents: 3
- Simulation Steps: 300
- Network Type: small_world
- Language: **English**

## Experiment Results

### ✅ Experiment 1: Baseline Dynamics
- **Status**: Completed
- **Output**: `results/exp1_baseline/baseline_summary.png` (529.2 KB)
- **Description**: Ising-D-I-B baseline model with adaptive coupling

### ✅ Experiment 2: AI Agent Evolution
- **Status**: Completed
- **Output**: `results/exp2_mechanism/evolution_analysis.png` (225.4 KB)
- **Key Findings**:
  - Error rate reduction: 0.095 → 0.015
  - Evolution progress: 0.001 → 0.256
  - Consumer trust recovery: 0.270
  - Total learning events: 115,271

### ✅ Experiment 3-a: Filter Bubble
- **Status**: Completed
- **Output**: `results/exp3_consequences/filter_bubble/filter_bubble_analysis.png` (231.4 KB)
- **Key Findings**:
  - Overall diversity score: 0.876
  - Filter bubble strength: 0.119
  - High vs Low dependency difference: -0.237
  - Intervention improvement: +14.2%

### ✅ Experiment 3-b: Systemic Risk
- **Status**: Completed
- **Output**: `results/exp3_consequences/systemic_risk/systemic_risk_analysis.png` (204.8 KB)
- **Key Findings**:
  - Major breach max impact: 177 consumers
  - Critical failure max impact: 271 consumers
  - Coordinated attack max impact: 260 consumers
  - System resilience score: 5.180

### ✅ Experiment 4: Information Intervention
- **Status**: Completed
- **Output**: `results/exp4_intervention/intervention_all_policies.png` (774.7 KB)
- **Policy Comparison**:
  - **Balanced**: L2=75.4%, L3=12.0%, L4=12.6%, Satisfaction=0.301
  - **Pro-AI**: L2=17.4%, L3=20.2%, L4=62.4%, Satisfaction=0.301
  - **Consumer Protection**: L2=15.4%, L3=13.8%, L4=70.8%, Satisfaction=0.306

## Generated Figures (English Version)

All figures are generated in English and stored in the following locations:

1. **Baseline Summary** (529.2 KB)
   - Path: `abm_simulation/results/exp1_baseline/baseline_summary.png`
   - Content: 3×3 comprehensive analysis grid

2. **Evolution Analysis** (225.4 KB)
   - Path: `abm_simulation/results/exp2_mechanism/evolution_analysis.png`
   - Content: AI capability evolution and dependency dynamics

3. **Filter Bubble Analysis** (231.4 KB)
   - Path: `abm_simulation/results/exp3_consequences/filter_bubble/filter_bubble_analysis.png`
   - Content: Diversity metrics and intervention effects

4. **Systemic Risk Analysis** (204.8 KB)
   - Path: `abm_simulation/results/exp3_consequences/systemic_risk/systemic_risk_analysis.png`
   - Content: Crisis simulation and stress test scenarios

5. **Intervention Policies** (774.7 KB)
   - Path: `abm_simulation/results/exp4_intervention/intervention_all_policies.png`
   - Content: Three policy comparison (3×3 grid)

## Total Output
- **Total Experiments**: 5 (all successful)
- **Total Figures**: 5 PNG files
- **Total Size**: ~1.97 MB
- **Language**: English

## Notes
- All visualizations use English labels, titles, and legends
- Data initialization based on ACDDS survey with demographics
- Dependency levels calculated using PU (Perceived Usefulness) and TR (Trust) scores
- Simulation successfully completed without errors
