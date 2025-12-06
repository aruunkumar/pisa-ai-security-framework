import json
import matplotlib.pyplot as plt
import numpy as np
from analyze_results import PISAResultsAnalyzer

def create_visualizations():
    """Generate publication-quality visualizations for the paper"""
    
    analyzer = PISAResultsAnalyzer()
    analysis = analyzer.analyze_results()
    
    # Set style for publication
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.family'] = 'serif'
    
    # Figure 1: Attack Success Rate by Layer
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    layers = []
    baseline_rates = []
    pisa_rates = []
    
    for layer, data in sorted(analysis['by_layer'].items()):
        layers.append(layer.replace(' ', '\n'))
        total = data['total']
        baseline_rates.append((data['baseline_success'] / total * 100) if total > 0 else 0)
        pisa_rates.append((data['pisa_success'] / total * 100) if total > 0 else 0)
    
    x = np.arange(len(layers))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, baseline_rates, width, label='Baseline (No PISA)', 
                    color='#d62728', alpha=0.8)
    bars2 = ax1.bar(x + width/2, pisa_rates, width, label='PISA-Enhanced',
                    color='#2ca02c', alpha=0.8)
    
    ax1.set_xlabel('PISA Framework Layer', fontweight='bold')
    ax1.set_ylabel('Attack Success Rate (%)', fontweight='bold')
    ax1.set_title('Attack Success Rate Comparison by PISA Layer', fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(layers)
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('figure1_attack_success_by_layer.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: figure1_attack_success_by_layer.png")
    
    # Figure 2: Defense Quality by Layer
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    baseline_quality = []
    pisa_quality = []
    
    for layer, data in sorted(analysis['by_layer'].items()):
        baseline_quality.append(sum(data['baseline_defense_quality']) / len(data['baseline_defense_quality']) 
                               if data['baseline_defense_quality'] else 0)
        pisa_quality.append(sum(data['pisa_defense_quality']) / len(data['pisa_defense_quality'])
                           if data['pisa_defense_quality'] else 0)
    
    bars1 = ax2.bar(x - width/2, baseline_quality, width, label='Baseline (No PISA)',
                    color='#d62728', alpha=0.8)
    bars2 = ax2.bar(x + width/2, pisa_quality, width, label='PISA-Enhanced',
                    color='#2ca02c', alpha=0.8)
    
    ax2.set_xlabel('PISA Framework Layer', fontweight='bold')
    ax2.set_ylabel('Mean Defense Quality Score', fontweight='bold')
    ax2.set_title('Defense Quality Comparison by PISA Layer', fontweight='bold', pad=20)
    ax2.set_xticks(x)
    ax2.set_xticklabels(layers)
    ax2.legend(loc='upper left')
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(0, 2.5)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('figure2_defense_quality_by_layer.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: figure2_defense_quality_by_layer.png")
    
    # Figure 3: Overall Improvement
    fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Overall attack success rate
    total = analysis['overall']['total']
    overall_baseline = (analysis['overall']['baseline_success'] / total * 100) if total > 0 else 0
    overall_pisa = (analysis['overall']['pisa_success'] / total * 100) if total > 0 else 0
    
    bars = ax3a.bar(['Baseline\n(No PISA)', 'PISA-Enhanced'], 
                    [overall_baseline, overall_pisa],
                    color=['#d62728', '#2ca02c'], alpha=0.8, width=0.6)
    ax3a.set_ylabel('Attack Success Rate (%)', fontweight='bold')
    ax3a.set_title('Overall Attack Success Rate', fontweight='bold', pad=15)
    ax3a.grid(axis='y', alpha=0.3)
    ax3a.set_ylim(0, 100)
    
    for bar in bars:
        height = bar.get_height()
        ax3a.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}%',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Overall defense quality
    overall_baseline_quality = sum(analysis['overall']['baseline_defense_quality']) / total if total > 0 else 0
    overall_pisa_quality = sum(analysis['overall']['pisa_defense_quality']) / total if total > 0 else 0
    
    bars = ax3b.bar(['Baseline\n(No PISA)', 'PISA-Enhanced'],
                    [overall_baseline_quality, overall_pisa_quality],
                    color=['#d62728', '#2ca02c'], alpha=0.8, width=0.6)
    ax3b.set_ylabel('Mean Defense Quality Score', fontweight='bold')
    ax3b.set_title('Overall Defense Quality', fontweight='bold', pad=15)
    ax3b.grid(axis='y', alpha=0.3)
    ax3b.set_ylim(0, 2.5)
    
    for bar in bars:
        height = bar.get_height()
        ax3b.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figure3_overall_improvement.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: figure3_overall_improvement.png")
    
    # Figure 4: Results by Severity
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    
    severities = ['Critical', 'High']
    severity_baseline = []
    severity_pisa = []
    
    for severity in severities:
        if severity in analysis['by_severity']:
            data = analysis['by_severity'][severity]
            total = data['total']
            severity_baseline.append((data['baseline_success'] / total * 100) if total > 0 else 0)
            severity_pisa.append((data['pisa_success'] / total * 100) if total > 0 else 0)
        else:
            severity_baseline.append(0)
            severity_pisa.append(0)
    
    x = np.arange(len(severities))
    bars1 = ax4.bar(x - width/2, severity_baseline, width, label='Baseline (No PISA)',
                    color='#d62728', alpha=0.8)
    bars2 = ax4.bar(x + width/2, severity_pisa, width, label='PISA-Enhanced',
                    color='#2ca02c', alpha=0.8)
    
    ax4.set_xlabel('Threat Severity', fontweight='bold')
    ax4.set_ylabel('Attack Success Rate (%)', fontweight='bold')
    ax4.set_title('Attack Success Rate by Threat Severity', fontweight='bold', pad=20)
    ax4.set_xticks(x)
    ax4.set_xticklabels(severities)
    ax4.legend(loc='upper right')
    ax4.grid(axis='y', alpha=0.3)
    ax4.set_ylim(0, 100)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('figure4_results_by_severity.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: figure4_results_by_severity.png")
    
    print("\n" + "="*60)
    print("All visualizations generated successfully!")
    print("="*60)
    print("\nFiles created:")
    print("  1. figure1_attack_success_by_layer.png")
    print("  2. figure2_defense_quality_by_layer.png")
    print("  3. figure3_overall_improvement.png")
    print("  4. figure4_results_by_severity.png")
    print("\nThese figures are publication-ready at 300 DPI.")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        create_visualizations()
    except Exception as e:
        print(f"Error creating visualizations: {e}")
        print("\nNote: Make sure you have run 'run_experiments.py' first to generate results.")
        print("Also ensure matplotlib is installed: pip install matplotlib")
