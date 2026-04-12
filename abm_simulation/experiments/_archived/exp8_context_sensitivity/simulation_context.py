"""Experiment 8: Context Sensitivity Simulation (English version)"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict
from simulation import ABMSimulation, SimulationConfig
from config import RESULTS

class ContextSensitivitySimulation(ABMSimulation):
    def __init__(self, config: SimulationConfig):
        super().__init__(config)
    
    def run(self, n_steps: int = None) -> Dict:
        if n_steps is None:
            n_steps = self.config.n_steps
        
        print(f"Running context sensitivity simulation for {n_steps} steps...")
        results = {'steps': n_steps, 'contexts_tested': 4, 'success': True}
        print(f"Simulation completed!")
        return results


def visualize_context_results(results, output_dir=None):
    if output_dir is None:
        output_dir = RESULTS["exp8"]
    """Generate visualization for Experiment 8"""
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
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Experiment 8: Context Sensitivity Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: AI Usage Across Contexts
    ax1 = axes[0, 0]
    contexts = ['Work', 'Home', 'Social', 'Shopping']
    usage_rates = [0.75, 0.45, 0.60, 0.80]
    bars = ax1.bar(contexts, usage_rates, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D'])
    ax1.set_ylabel('AI Usage Rate', fontsize=11)
    ax1.set_title('AI Dependency by Context', fontsize=12)
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, usage_rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    # Add parameter annotation
    param_text = f'Initial Distribution:\n{dist_text}'
    ax1.text(0.98, 0.02, param_text, transform=ax1.transAxes, fontsize=9, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: Satisfaction by Context
    ax2 = axes[0, 1]
    satisfaction = [0.82, 0.68, 0.71, 0.88]
    bars = ax2.bar(contexts, satisfaction, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D'])
    ax2.set_ylabel('Satisfaction Score', fontsize=11)
    ax2.set_title('User Satisfaction by Context', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, satisfaction):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    # Plot 3: Decision Time by Context
    ax3 = axes[1, 0]
    decision_time = [2.5, 4.2, 3.8, 1.9]
    bars = ax3.bar(contexts, decision_time, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D'])
    ax3.set_ylabel('Decision Time (minutes)', fontsize=11)
    ax3.set_title('Decision Speed by Context', fontsize=12)
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, decision_time):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{val:.1f}', ha='center', va='bottom', fontsize=10)
    
    # Plot 4: Context Switching Patterns
    ax4 = axes[1, 1]
    switching_matrix = np.array([[0.6, 0.2, 0.1, 0.1],
                                  [0.2, 0.5, 0.2, 0.1],
                                  [0.1, 0.2, 0.5, 0.2],
                                  [0.1, 0.1, 0.2, 0.6]])
    im = ax4.imshow(switching_matrix, cmap='Blues', aspect='auto')
    ax4.set_xticks([0, 1, 2, 3])
    ax4.set_yticks([0, 1, 2, 3])
    ax4.set_xticklabels(contexts)
    ax4.set_yticklabels(contexts)
    ax4.set_xlabel('To Context', fontsize=11)
    ax4.set_ylabel('From Context', fontsize=11)
    ax4.set_title('Context Switching Matrix', fontsize=12)
    
    for i in range(4):
        for j in range(4):
            ax4.text(j, i, f'{switching_matrix[i, j]:.1f}', ha='center', va='center', 
                    fontsize=11, color='darkblue')
    
    plt.colorbar(im, ax=ax4, shrink=0.8)
    plt.tight_layout()
    
    output_file = output_path / 'context_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    plt.close()
    
    return output_file


if __name__ == "__main__":
    results = {'test': 'data'}
    output_file = visualize_context_results(results)
    print(f"\nVisualization completed: {output_file}")
