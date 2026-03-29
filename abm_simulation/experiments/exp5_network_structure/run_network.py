# -*- coding: utf-8 -*-
"""Experiment 5 Runner - Network Structure Comparison"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from simulation import SimulationConfig
from experiments.exp5_network_structure.simulation_network import NetworkStructureSimulation
from experiments.exp5_network_structure.visualization_network import visualize_network_results

def run_experiment5():
    print("="*70)
    print("Experiment 5: Network Structure Comparison")
    print("Research Question: How do different network topologies affect dependency diffusion?")
    print("="*70)
    
    config = SimulationConfig(
        n_consumers=500, n_merchants=20, n_ai_agents=3,
        network_type='small_world', n_steps=200,
        initial_coupling=0.2, initial_temperature=2.0
    )
    
    print(f"\nSimulation Configuration:")
    print(f"  - Consumers: {config.n_consumers}")
    print(f"  - Steps: {config.n_steps}")
    print(f"  - Initial coupling: {config.initial_coupling}")
    print(f"  - Temperature: {config.initial_temperature}")
    
    sim = NetworkStructureSimulation(config)
    result = sim.run()
    
    # Generate visualization
    print(f"\nGenerating visualization...")
    results = {'test': result}
    output_file = visualize_network_results(results)
    
    print(f"\n{'='*70}")
    print(f"Experiment 5 completed!")
    print(f"{'='*70}")
    print(f"\nVisualization saved to: {output_file}")
    
    return sim, results

if __name__ == "__main__":
    sim, results = run_experiment5()
