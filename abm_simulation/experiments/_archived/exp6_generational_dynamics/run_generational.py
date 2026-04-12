# -*- coding: utf-8 -*-
"""Experiment 6 Runner - Generational Dynamics"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import SimulationConfig
from experiments.exp6_generational_dynamics.simulation_generational import GenerationalDynamicsSimulation, visualize_generational_results

def run_experiment6():
    print("="*70)
    print("Experiment 6: Generational Dynamics")
    print("Research Question: How does generational replacement change AI dependency culture?")
    print("="*70)
    
    # Get level distribution from config
    config = SimulationConfig(
        n_consumers=500, n_merchants=20, n_ai_agents=3,
        network_type='small_world', n_steps=150,
        initial_coupling=0.2, initial_temperature=2.0
    )
    
    print(f"\nSimulation Configuration:")
    print(f"  - Consumers: {config.n_consumers}")
    print(f"  - Steps: {config.n_steps}")
    print(f"  - Initial coupling: {config.initial_coupling}")
    print(f"  - Level Distribution:")
    for level, ratio in config.initial_level_distribution.items():
        print(f"      L{level}: {ratio*100:.0f}%")
    
    sim = GenerationalDynamicsSimulation(config)
    result = sim.run()
    
    # Add level distribution to results for visualization
    result['level_distribution'] = config.initial_level_distribution
    
    # Generate visualization
    print(f"\nGenerating visualization...")
    output_file = visualize_generational_results(result)
    
    print(f"\n{'='*70}")
    print(f"Experiment 6 completed!")
    print(f"{'='*70}")
    print(f"\nVisualization saved to: {output_file}")
    
    return sim, {'test': result}

if __name__ == "__main__":
    sim, results = run_experiment6()
