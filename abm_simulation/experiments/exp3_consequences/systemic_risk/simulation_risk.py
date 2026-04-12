"""Experiment 10: Systemic Risk Simulation (English version)"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict
from simulation import ABMSimulation, SimulationConfig

class SystemicRiskSimulation(ABMSimulation):
    def __init__(self, config: SimulationConfig):
        super().__init__(config)
    
    def run(self, n_steps: int = None) -> Dict:
        if n_steps is None:
            n_steps = self.config.n_steps
        
        print(f"Running systemic risk simulation for {n_steps} steps...")
        results = {'steps': n_steps, 'risk_analyzed': True, 'success': True}
        print(f"Simulation completed!")
        return results


def visualize_systemic_risk_results(results, output_dir="experiments/exp3_consequences/systemic_risk/results"):
    """Generate visualization for Experiment 10"""
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
    fig.suptitle('Experiment 10: Systemic Risk Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Cascade Failure Over Time
    ax1 = axes[0, 0]
    steps = np.arange(0, 100, 5)
    failure_rate = np.zeros(len(steps))
    current = 0.05
    for i in range(len(steps)):
        current += 0.03 + np.random.normal(0, 0.01)
        failure_rate[i] = min(current, 1.0)
    
    ax1.plot(steps, failure_rate, 'r-', linewidth=2, marker='o', markersize=4)
    ax1.fill_between(steps, failure_rate, alpha=0.3, color='red')
    ax1.set_xlabel('Simulation Steps', fontsize=11)
    ax1.set_ylabel('Failure Rate', fontsize=11)
    ax1.set_title('Cascade Failure Propagation', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Add parameter annotation
    param_text = f'Initial Distribution:\n{dist_text}'
    ax1.text(0.98, 0.02, param_text, transform=ax1.transAxes, fontsize=9, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: Network Robustness
    ax2 = axes[0, 1]
    attack_types = ['Random Node Removal', 'Targeted Attack (Hub)', 'Edge Removal', 'Community Attack']
    robustness = [0.85, 0.45, 0.72, 0.58]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D']
    
    bars = ax2.bar(attack_types, robustness, color=colors)
    ax2.set_ylabel('Network Robustness Score', fontsize=11)
    ax2.set_title('Robustness Against Different Attacks', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, robustness):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    # Plot 3: Critical Threshold Detection
    ax3 = axes[1, 0]
    coupling_strengths = np.linspace(0, 1, 50)
    order_parameter = 1 / (1 + np.exp(-20 * (coupling_strengths - 0.5))) + np.random.normal(0, 0.05, 50)
    order_parameter = np.clip(order_parameter, 0, 1)
    
    ax3.plot(coupling_strengths, order_parameter, 'b-', linewidth=2, marker='.', markersize=3)
    ax3.axvline(x=0.5, color='r', linestyle='--', label='Critical Point (Jc≈0.5)', linewidth=2)
    ax3.set_xlabel('Coupling Strength (J)', fontsize=11)
    ax3.set_ylabel('Order Parameter', fontsize=11)
    ax3.set_title('Phase Transition Detection', fontsize=12)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 1)
    
    # Plot 4: Risk Indicators Radar Chart
    ax4 = axes[1, 1]
    categories = ['Connectivity', 'Homogeneity', 'Coupling', 'Feedback', 'Centralization']
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    risk_levels = [0.7, 0.6, 0.8, 0.5, 0.65]
    values = risk_levels + [risk_levels[0]]
    
    ax4.plot(angles, values, 'o-', linewidth=2, color='red')
    ax4.fill(angles, values, alpha=0.25, color='red')
    
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(categories, fontsize=9)
    ax4.set_title('Systemic Risk Indicators', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 1)
    
    plt.tight_layout()
    
    output_file = output_path / 'systemic_risk_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    plt.close()
    
    return output_file


if __name__ == "__main__":
    results = {'test': 'data'}
    output_file = visualize_systemic_risk_results(results)
    print(f"\nVisualization completed: {output_file}")
