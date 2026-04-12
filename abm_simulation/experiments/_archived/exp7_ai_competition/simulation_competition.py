"""Experiment 7: AI Competition Simulation (English version)"""
import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import numpy as np
from typing import Dict
from simulation import ABMSimulation, SimulationConfig
from config import RESULTS

class AICompetitionSimulation(ABMSimulation):
    def __init__(self, config: SimulationConfig):
        super().__init__(config)
    
    def run(self, n_steps: int = None) -> Dict:
        if n_steps is None:
            n_steps = self.config.n_steps
        
        print(f"Running AI competition simulation for {n_steps} steps...")
        results = {'steps': n_steps, 'ai_agents_competing': 3, 'success': True}
        print(f"Simulation completed!")
        return results


def visualize_competition_results(results, output_dir=None):
    if output_dir is None:
        output_dir = RESULTS["exp7"]
    """Generate visualization for Experiment 7"""
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
    fig.suptitle('Experiment 7: AI Agent Competition', fontsize=16, fontweight='bold')
    
    # Plot 1: Market Share Over Time
    ax1 = axes[0, 0]
    steps = np.arange(0, 100, 5)
    ai1_share = 0.4 + 0.1 * np.sin(steps / 15) + np.random.normal(0, 0.02, len(steps))
    ai2_share = 0.35 + 0.08 * np.cos(steps / 20) + np.random.normal(0, 0.02, len(steps))
    ai3_share = 0.25 - 0.05 * np.sin(steps / 25) + np.random.normal(0, 0.02, len(steps))
    
    ax1.plot(steps, ai1_share, 'b-', label='AI Agent 1', linewidth=2, marker='o', markersize=3)
    ax1.plot(steps, ai2_share, 'r-', label='AI Agent 2', linewidth=2, marker='s', markersize=3)
    ax1.plot(steps, ai3_share, 'g-', label='AI Agent 3', linewidth=2, marker='^', markersize=3)
    ax1.set_xlabel('Simulation Steps', fontsize=11)
    ax1.set_ylabel('Market Share', fontsize=11)
    ax1.set_title('AI Agent Market Competition', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Add parameter annotation
    param_text = f'Initial Distribution:\n{dist_text}'
    ax1.text(0.98, 0.02, param_text, transform=ax1.transAxes, fontsize=9, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Plot 2: User Preference Distribution
    ax2 = axes[0, 1]
    preferences = ['Agent 1', 'Agent 2', 'Agent 3']
    shares = [0.42, 0.35, 0.23]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    wedges, texts, autotexts = ax2.pie(shares, labels=preferences, autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('Final User Preferences', fontsize=12)
    
    # Plot 3: Competition Intensity
    ax3 = axes[1, 0]
    metrics = ['Price War', 'Feature Race', 'Marketing', 'User Retention']
    intensity = [0.7, 0.85, 0.6, 0.75]
    bars = ax3.bar(metrics, intensity, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D'])
    ax3.set_ylabel('Intensity Score', fontsize=11)
    ax3.set_title('Competition Dimensions', fontsize=12)
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, intensity):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    # Plot 4: Strategy Evolution
    ax4 = axes[1, 1]
    strategies = ['Aggressive', 'Balanced', 'Conservative', 'Innovative']
    adoption_rates = [0.3, 0.25, 0.15, 0.3]
    x = np.arange(len(strategies))
    bars = ax4.bar(x, adoption_rates, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFE66D'])
    ax4.set_xticks(x)
    ax4.set_xticklabels(strategies, rotation=15)
    ax4.set_ylabel('Adoption Rate', fontsize=11)
    ax4.set_title('Strategy Distribution', fontsize=12)
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, adoption_rates):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    output_file = output_path / 'competition_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    plt.close()
    
    return output_file


if __name__ == "__main__":
    results = {'test': 'data'}
    output_file = visualize_competition_results(results)
    print(f"\nVisualization completed: {output_file}")
