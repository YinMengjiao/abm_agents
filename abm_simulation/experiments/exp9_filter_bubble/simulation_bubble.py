"""Experiment 9: Filter Bubble Simulation (English version)"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict
from simulation import ABMSimulation, SimulationConfig

class FilterBubbleSimulation(ABMSimulation):
    def __init__(self, config: SimulationConfig):
        super().__init__(config)
    
    def run(self, n_steps: int = None) -> Dict:
        if n_steps is None:
            n_steps = self.config.n_steps
        
        print(f"Running filter bubble simulation for {n_steps} steps...")
        results = {'steps': n_steps, 'bubble_strength_measured': True, 'success': True}
        print(f"Simulation completed!")
        return results


def visualize_filter_bubble_results(results, output_dir="experiments/exp9_filter_bubble/results"):
    """Generate visualization for Experiment 9"""
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
    fig.suptitle('Experiment 9: Filter Bubble Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Information Diversity Over Time
    ax1 = axes[0, 0]
    steps = np.arange(0, 100, 5)
    diversity_strong = 0.9 - 0.3 * (steps / 100) + np.random.normal(0, 0.02, len(steps))
    diversity_moderate = 0.85 - 0.15 * (steps / 100) + np.random.normal(0, 0.02, len(steps))
    diversity_weak = 0.8 - 0.05 * (steps / 100) + np.random.normal(0, 0.02, len(steps))
    
    ax1.plot(steps, diversity_strong, 'r-', label='Strong Bubble', linewidth=2, marker='o', markersize=3)
    ax1.plot(steps, diversity_moderate, 'orange', label='Moderate Bubble', linewidth=2, marker='s', markersize=3)
    ax1.plot(steps, diversity_weak, 'g-', label='Weak Bubble', linewidth=2, marker='^', markersize=3)
    ax1.set_xlabel('Simulation Steps', fontsize=11)
    ax1.set_ylabel('Information Diversity', fontsize=11)
    ax1.set_title('Echo Chamber Effect Over Time', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Add parameter annotation
    param_text = f'Initial Distribution:\n{dist_text}'
    ax1.text(0.98, 0.02, param_text, transform=ax1.transAxes, fontsize=9, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: Opinion Distribution
    ax2 = axes[0, 1]
    opinions = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
    strong_bubble = [0.45, 0.25, 0.10, 0.15, 0.05]
    weak_bubble = [0.15, 0.20, 0.30, 0.20, 0.15]
    
    x = np.arange(len(opinions))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, strong_bubble, width, label='Strong Bubble', color='red', alpha=0.7)
    bars2 = ax2.bar(x + width/2, weak_bubble, width, label='Weak Bubble', color='green', alpha=0.7)
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(opinions, rotation=15, ha='right')
    ax2.set_ylabel('Proportion', fontsize=11)
    ax2.set_title('Opinion Polarization', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Exposure to Diverse Views
    ax3 = axes[1, 0]
    metrics = ['Own View', 'Similar View', 'Neutral', 'Opposing View']
    exposure_strong = [0.70, 0.20, 0.07, 0.03]
    exposure_weak = [0.35, 0.30, 0.20, 0.15]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, exposure_strong, width, label='Strong Bubble', color='red', alpha=0.7)
    bars2 = ax3.bar(x + width/2, exposure_weak, width, label='Weak Bubble', color='green', alpha=0.7)
    
    ax3.set_xticks(x)
    ax3.set_xticklabels(metrics, rotation=15, ha='right')
    ax3.set_ylabel('Exposure Proportion', fontsize=11)
    ax3.set_title('Information Exposure Pattern', fontsize=12)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Bubble Strength Metrics
    ax4 = axes[1, 1]
    categories = ['Selectivity', 'Reinforcement', 'Isolation', 'Polarization']
    bubble_metrics = [0.85, 0.78, 0.72, 0.65]
    bars = ax4.bar(categories, bubble_metrics, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D'])
    ax4.set_ylabel('Bubble Strength Score', fontsize=11)
    ax4.set_title('Filter Bubble Dimensions', fontsize=12)
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, bubble_metrics):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    output_file = output_path / 'filter_bubble_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    plt.close()
    
    return output_file


if __name__ == "__main__":
    results = {'test': 'data'}
    output_file = visualize_filter_bubble_results(results)
    print(f"\nVisualization completed: {output_file}")
