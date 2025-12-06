#!/usr/bin/env python3
"""
Create Baseline vs PISA Layer Comparison Chart
Standalone script to generate the layer-by-layer comparison visualization
"""
import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def load_analysis_data():
    """Load the analysis results from JSON file"""
    try:
        with open('analysis_results.json', 'r') as f:
            data = json.load(f)
        print("✓ Loaded analysis data successfully")
        return data
    except FileNotFoundError:
        print("ERROR: analysis_results.json not found!")
        print("Please run analyze_results.py first")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in analysis_results.json: {e}")
        sys.exit(1)

def create_layer_comparison_chart(analysis):
    """Create grouped bar chart comparing baseline vs PISA for each layer"""
    print("Creating layer comparison chart...")
    
    # Set up the plot style
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    layers = ['Prompt\nIntegrity', 'Information\nBoundary', 'Semantic\nVerification']
    
    baseline_scores = [
        analysis['layers']['prompt_integrity']['baseline_score'],
        analysis['layers']['information_boundary']['baseline_score'],
        analysis['layers']['semantic_verification']['baseline_score']
    ]
    
    pisa_scores = [
        analysis['layers']['prompt_integrity']['pisa_score'],
        analysis['layers']['information_boundary']['pisa_score'],
        analysis['layers']['semantic_verification']['pisa_score']
    ]
    
    improvements = [
        analysis['layers']['prompt_integrity']['improvement'],
        analysis['layers']['information_boundary']['improvement'],
        analysis['layers']['semantic_verification']['improvement']
    ]
    
    # Set up bar positions
    x = np.arange(len(layers))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar(x - width/2, baseline_scores, width, label='Baseline',
                   color='#e74c3c', alpha=0.85, edgecolor='black', linewidth=2)
    bars2 = ax.bar(x + width/2, pisa_scores, width, label='PISA',
                   color='#2ecc71', alpha=0.85, edgecolor='black', linewidth=2)
    
    # Styling
    ax.set_ylabel('Protection Score', fontsize=15, fontweight='bold')
    ax.set_title('Baseline vs PISA Protection by Layer', 
                 fontsize=17, fontweight='bold', pad=25)
    ax.set_xticks(x)
    ax.set_xticklabels(layers, fontsize=13, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(axis='y', alpha=0.3, linewidth=1.5)
    
    # Legend
    ax.legend(fontsize=14, loc='upper left', frameon=True, shadow=True,
             fancybox=True, framealpha=0.95)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Add improvement annotations above each layer
    for i, imp in enumerate(improvements):
        ax.text(i, 108, f'+{imp:.1f}',
               ha='center', va='center', fontsize=11, fontweight='bold',
               color='green',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                        edgecolor='green', linewidth=2, alpha=0.95))
    
    plt.tight_layout()
    
    # Save the figure
    output_file = 'pisa_layer_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Chart saved to {output_file}")
    print(f"\nLayer Scores:")
    for i, layer in enumerate(['Prompt Integrity', 'Information Boundary', 'Semantic Verification']):
        print(f"  {layer}:")
        print(f"    Baseline: {baseline_scores[i]:.1f}/100")
        print(f"    PISA: {pisa_scores[i]:.1f}/100")
        print(f"    Improvement: +{improvements[i]:.1f} points")
    
    return output_file

def main():
    """Main execution function"""
    print("="*60)
    print("PISA Layer Comparison Chart Generator")
    print("="*60)
    
    # Load data
    analysis = load_analysis_data()
    
    # Create chart
    output_file = create_layer_comparison_chart(analysis)
    
    # Verify file was created
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"\n✓ SUCCESS: Chart created ({file_size:,} bytes)")
    else:
        print("\n✗ ERROR: Chart file was not created")
        sys.exit(1)
    
    print("="*60)

if __name__ == "__main__":
    main()
