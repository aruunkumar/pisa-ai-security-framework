#!/usr/bin/env python3
"""
Create Overall PISA Framework Effectiveness Chart
Standalone script to generate the overall comparison visualization
"""
import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
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

def create_overall_effectiveness_chart(analysis):
    """Create bar chart showing baseline vs PISA overall scores"""
    print("Creating overall effectiveness chart...")
    
    # Set up the plot style
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Data
    categories = ['Baseline\nSystem', 'PISA\nFramework']
    baseline_score = analysis['overall']['baseline_score']
    pisa_score = analysis['overall']['pisa_score']
    scores = [baseline_score, pisa_score]
    improvement = analysis['overall']['improvement']
    
    # Colors: red for baseline, green for PISA
    colors = ['#e74c3c', '#2ecc71']
    
    # Create bars
    bars = ax.bar(categories, scores, color=colors, alpha=0.85, 
                  edgecolor='black', linewidth=2.5, width=0.5)
    
    # Styling
    ax.set_ylabel('Protection Score', fontsize=15, fontweight='bold')
    ax.set_title('Overall PISA Framework Effectiveness', 
                 fontsize=17, fontweight='bold', pad=25)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', alpha=0.3, linewidth=1.5)
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=12)
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}/100',
                ha='center', va='bottom', fontweight='bold', fontsize=14,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='black', linewidth=1))
    
    # Add improvement annotation in the middle
    mid_point = (baseline_score + pisa_score) / 2
    ax.text(0.5, mid_point, f'+{improvement:.1f} points\nimprovement',
            fontsize=14, fontweight='bold', color='green',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                     edgecolor='green', linewidth=2.5, alpha=0.95))
    
    # Add curved arrow showing improvement
    from matplotlib.patches import FancyArrowPatch
    arrow = FancyArrowPatch((0.05, baseline_score + 5), (0.95, pisa_score - 5),
                           connectionstyle="arc3,rad=0.3", 
                           arrowstyle='->', mutation_scale=30,
                           linewidth=3, color='green', alpha=0.7)
    ax.add_patch(arrow)
    
    # Add summary text at bottom
    summary_text = f'Baseline: {baseline_score:.1f}/100  →  PISA: {pisa_score:.1f}/100'
    fig.text(0.5, 0.02, summary_text, ha='center', fontsize=12, 
             fontweight='bold', style='italic')
    
    plt.tight_layout()
    
    # Save the figure
    output_file = 'pisa_overall_effectiveness.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Chart saved to {output_file}")
    print(f"  Baseline: {baseline_score:.1f}/100")
    print(f"  PISA: {pisa_score:.1f}/100")
    print(f"  Improvement: +{improvement:.1f} points")
    
    return output_file

def main():
    """Main execution function"""
    print("="*60)
    print("PISA Overall Effectiveness Chart Generator")
    print("="*60)
    
    # Load data
    analysis = load_analysis_data()
    
    # Create chart
    output_file = create_overall_effectiveness_chart(analysis)
    
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
