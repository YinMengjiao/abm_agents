# -*- coding: utf-8 -*-
"""Experiment 8 Runner - Context Sensitivity"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import SimulationConfig
from experiments.exp8_context_sensitivity.simulation_context import ContextSensitivitySimulation, visualize_context_results

def run_experiment8():
    print("="*70)
    print("Experiment 8: Context Sensitivity")
    print("Research Question: How does context affect AI dependency patterns?")
    print("="*70)
    
    config = SimulationConfig(
        n_consumers=500, n_merchants=20, n_ai_agents=3,
        network_type='small_world', n_steps=150,
        initial_coupling=0.2, initial_temperature=2.0
    )
    
    print(f"\nSimulation Configuration:")
    print(f"  - Consumers: {config.n_consumers}")
    print(f"  - Steps: {config.n_steps}")
    print(f"  - Contexts: Work, Home, Social, Shopping")
    print(f"  - Level Distribution:")
    for level, ratio in config.initial_level_distribution.items():
        print(f"      L{level}: {ratio*100:.0f}%")
    
    sim = ContextSensitivitySimulation(config)
    result = sim.run()
    
    # Add level distribution to results for visualization
    result['level_distribution'] = config.initial_level_distribution
    
    # Generate visualization
    print(f"\nGenerating visualization...")
    output_file = visualize_context_results(result)
    
    print(f"\n{'='*70}")
    print(f"Experiment 8 completed!")
    print(f"{'='*70}")
    print(f"\nVisualization saved to: {output_file}")
    
    return sim, {'test': result}

if __name__ == "__main__":
    sim, results = run_experiment8()
