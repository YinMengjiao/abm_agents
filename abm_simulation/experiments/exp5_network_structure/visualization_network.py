"""Experiment 5 Visualization: Network Structure Comparison"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def visualize_network_results(results, output_dir="experiments/exp5_network_structure/results"):
    """Generate visualization for Experiment 5"""
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nGenerating visualizations...")
    print(f"Output directory: {output_path}")
    
    # Figure 1: Network Topology Comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Experiment 5: Network Structure Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: AI Usage Rate Over Time (placeholder)
    ax1 = axes[0, 0]
    steps = np.arange(0, 200, 10)
    ai_usage = 0.3 + 0.1 * np.sin(steps / 20) + np.random.normal(0, 0.02, len(steps))
    ax1.plot(steps, ai_usage, 'b-', linewidth=2, marker='o', markersize=4)
    ax1.set_xlabel('Simulation Steps', fontsize=11)
    ax1.set_ylabel('AI Usage Rate', fontsize=11)
    ax1.set_title('AI Adoption Dynamics', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Plot 2: Satisfaction Distribution (placeholder)
    ax2 = axes[0, 1]
    satisfaction_data = [np.random.normal(0.7, 0.15, 500), 
                         np.random.normal(0.65, 0.18, 500),
                         np.random.normal(0.72, 0.12, 500)]
    bp = ax2.boxplot(satisfaction_data, labels=['Random', 'Small World', 'Scale Free'], patch_artist=True)
    colors = ['lightblue', 'lightgreen', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    ax2.set_ylabel('Satisfaction Score', fontsize=11)
    ax2.set_title('User Satisfaction by Network Type', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Convergence Comparison (placeholder)
    ax3 = axes[1, 0]
    topologies = ['Random', 'Small World', 'Scale Free']
    convergence_steps = [85, 62, 95]
    bars = ax3.bar(topologies, convergence_steps, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax3.set_ylabel('Steps to Convergence', fontsize=11)
    ax3.set_title('Convergence Speed Comparison', fontsize=12)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, val in zip(bars, convergence_steps):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{val}', ha='center', va='bottom', fontsize=10)
    
    # Plot 4: Network Metrics Radar Chart (placeholder)
    ax4 = axes[1, 1]
    categories = ['Clustering', 'Path Length', 'Degree Dist.', 'Robustness', 'Efficiency']
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    values_random = [0.3, 0.6, 0.5, 0.7, 0.6]
    values_small_world = [0.8, 0.7, 0.6, 0.6, 0.7]
    values_scale_free = [0.2, 0.8, 0.9, 0.4, 0.8]
    
    for values, label, color in zip([values_random, values_small_world, values_scale_free], 
                                     ['Random', 'Small World', 'Scale Free'],
                                     ['red', 'green', 'blue']):
        values += values[:1]
        ax4.plot(angles, values, 'o-', linewidth=2, label=label, color=color)
        ax4.fill(angles, values, alpha=0.15, color=color)
    
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(categories, fontsize=9)
    ax4.set_title('Network Topology Metrics', fontsize=12)
    ax4.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = output_path / 'network_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    plt.close()
    
    return output_file


if __name__ == "__main__":
    # Test visualization
    results = {'test': 'data'}
    output_file = visualize_network_results(results)
    print(f"\nVisualization completed: {output_file}")
