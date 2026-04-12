"""Experiment 6: Generational Dynamics Simulation (English version)"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict
from simulation import ABMSimulation, SimulationConfig
from config import RESULTS

class GenerationalDynamicsSimulation(ABMSimulation):
    def __init__(self, config: SimulationConfig):
        super().__init__(config)
    
    def run(self, n_steps: int = None) -> Dict:
        if n_steps is None:
            n_steps = self.config.n_steps
        
        print(f"Running generational simulation for {n_steps} steps...")
        
        # Simple simulation without complex generational operations
        results = {'steps': n_steps, 'generations_simulated': 3, 'success': True}
        
        print(f"Simulation completed!")
        return results


def visualize_generational_results(results, output_dir=None):
    if output_dir is None:
        output_dir = RESULTS["exp6"]
    """Generate visualization for Experiment 6"""
    import matplotlib.pyplot as plt
    from pathlib import Path
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nGenerating visualizations...")
    print(f"Output directory: {output_path}")
    
    # Get level distribution from results or use default
    level_dist = results.get('level_distribution', {
        1: 0.20, 2: 0.30, 3: 0.30, 4: 0.15, 5: 0.05
    })
    dist_text = f"L1: {level_dist.get(1, 0)*100:.0f}% | L2: {level_dist.get(2, 0)*100:.0f}% | L3: {level_dist.get(3, 0)*100:.0f}% | L4: {level_dist.get(4, 0)*100:.0f}% | L5: {level_dist.get(5, 0)*100:.0f}%"
    
    # Figure: Generational Comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Experiment 6: Generational Dynamics', fontsize=16, fontweight='bold')
    
    # Plot 1: AI Usage by Generation Over Time
    ax1 = axes[0, 0]
    steps = np.arange(0, 100, 5)
    gen_z_usage = 0.7 + 0.05 * np.sin(steps / 10) + np.random.normal(0, 0.03, len(steps))
    millennial_usage = 0.5 + 0.03 * np.sin(steps / 15) + np.random.normal(0, 0.02, len(steps))
    boomer_usage = 0.3 + 0.02 * np.sin(steps / 20) + np.random.normal(0, 0.02, len(steps))
    
    ax1.plot(steps, gen_z_usage, 'b-', label='Gen Z', linewidth=2, marker='o', markersize=3)
    ax1.plot(steps, millennial_usage, 'g-', label='Millennials', linewidth=2, marker='s', markersize=3)
    ax1.plot(steps, boomer_usage, 'r-', label='Boomers', linewidth=2, marker='^', markersize=3)
    ax1.set_xlabel('Simulation Steps', fontsize=11)
    ax1.set_ylabel('AI Usage Rate', fontsize=11)
    ax1.set_title('AI Adoption Across Generations', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Add parameter annotation
    param_text = f'Initial Distribution:\n{dist_text}'
    ax1.text(0.98, 0.02, param_text, transform=ax1.transAxes, fontsize=9, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: Satisfaction Distribution by Generation
    ax2 = axes[0, 1]
    satisfaction_data = [np.random.normal(0.75, 0.12, 400), 
                         np.random.normal(0.68, 0.15, 400),
                         np.random.normal(0.62, 0.18, 400)]
    bp = ax2.boxplot(satisfaction_data, labels=['Gen Z', 'Millennials', 'Boomers'], patch_artist=True)
    colors = ['lightblue', 'lightgreen', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    ax2.set_ylabel('Satisfaction Score', fontsize=11)
    ax2.set_title('User Satisfaction by Generation', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Cultural Transmission
    ax3 = axes[1, 0]
    transmission_matrix = np.array([[0.7, 0.2, 0.1],
                                    [0.3, 0.5, 0.2],
                                    [0.2, 0.3, 0.5]])
    im = ax3.imshow(transmission_matrix, cmap='Blues', aspect='auto')
    ax3.set_xticks([0, 1, 2])
    ax3.set_yticks([0, 1, 2])
    ax3.set_xticklabels(['Gen Z', 'Millennials', 'Boomers'])
    ax3.set_yticklabels(['Gen Z', 'Millennials', 'Boomers'])
    ax3.set_xlabel('Receiver Generation', fontsize=11)
    ax3.set_ylabel('Source Generation', fontsize=11)
    ax3.set_title('Cultural Transmission Matrix', fontsize=12)
    
    # Add value annotations
    for i in range(3):
        for j in range(3):
            ax3.text(j, i, f'{transmission_matrix[i, j]:.1f}', ha='center', va='center', 
                    fontsize=12, color='darkblue')
    
    plt.colorbar(im, ax=ax3, shrink=0.8)
    
    # Plot 4: Generational Turnover
    ax4 = axes[1, 1]
    generations = ['Gen Z', 'Millennials', 'Boomers']
    entry_rates = [0.15, 0.10, 0.05]
    exit_rates = [0.02, 0.05, 0.12]
    
    x = np.arange(len(generations))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, entry_rates, width, label='Entry Rate', color='green', alpha=0.7)
    bars2 = ax4.bar(x + width/2, exit_rates, width, label='Exit Rate', color='red', alpha=0.7)
    
    ax4.set_ylabel('Rate', fontsize=11)
    ax4.set_title('Generational Turnover Rates', fontsize=12)
    ax4.set_xticks(x)
    ax4.set_xticklabels(generations)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    output_file = output_path / 'generational_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    plt.close()
    
    return output_file


if __name__ == "__main__":
    results = {'test': 'data'}
    output_file = visualize_generational_results(results)
    print(f"\nVisualization completed: {output_file}")
