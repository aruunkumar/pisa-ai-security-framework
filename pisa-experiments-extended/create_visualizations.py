#!/usr/bin/env python3
"""
Create visualizations for PISA framework evaluation results
"""
import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#e74c3c', '#3498db']  # Red for baseline, Blue for PISA

# Data
layers = ['Information\nBoundary', 'Prompt\nIntegrity', 'Semantic\nVerification', 'Agency\nAuthorization']
baseline_scores = [9.1, 58.3, 50.0, 22.2]
pisa_scores = [90.9, 100.0, 83.3, 94.4]

# Figure 1: Layer-by-Layer Comparison
fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(layers))
width = 0.35

bars1 = ax.bar(x - width/2, baseline_scores, width, label='Baseline', color=colors[0], alpha=0.8)
bars2 = ax.bar(x + width/2, pisa_scores, width, label='PISA', color=colors[1], alpha=0.8)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xlabel('PISA Security Layer', fontsize=12, fontweight='bold')
ax.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('PISA Framework: Layer-by-Layer Effectiveness Comparison', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(layers, fontsize=11)
ax.legend(fontsize=11, loc='upper left')
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)

# Add improvement annotations
for i, (baseline, pisa) in enumerate(zip(baseline_scores, pisa_scores)):
    improvement = pisa - baseline
    ax.annotate(f'+{improvement:.1f}',
                xy=(i, max(baseline, pisa) + 3),
                ha='center', fontsize=9, color='green', fontweight='bold')

plt.tight_layout()
plt.savefig('pisa_layer_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Created pisa_layer_comparison.png")

# Figure 2: Overall Effectiveness - Single Bar Comparison
fig, ax = plt.subplots(figsize=(8, 7))

categories = ['Overall Effectiveness\n(53 Tests)']
baseline_overall = [34.0]
pisa_overall = [92.5]

x = np.arange(len(categories))
width = 0.4

bars1 = ax.bar(x - width/2, baseline_overall, width, label='Baseline', color=colors[0], alpha=0.8)
bars2 = ax.bar(x + width/2, pisa_overall, width, label='PISA', color=colors[1], alpha=0.8)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold')

ax.set_ylabel('Success Rate (%)', fontsize=13, fontweight='bold')
ax.set_title('PISA Framework: Overall Effectiveness', fontsize=15, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.legend(fontsize=12, loc='upper left')
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)

# Add improvement annotation
improvement = pisa_overall[0] - baseline_overall[0]
ax.annotate(f'+{improvement:.1f} points',
            xy=(0, pisa_overall[0] + 3),
            ha='center', fontsize=12, color='green', fontweight='bold')

# Add breakdown text
breakdown_text = (
    'Breakdown:\n'
    '• Attack Detection: 92.3% (36/39)\n'
    '• Legitimate Operations: 92.9% (13/14)'
)
ax.text(0.98, 0.65, breakdown_text, 
        transform=ax.transAxes, ha='right', va='top',
        fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

plt.tight_layout()
plt.savefig('pisa_overall_effectiveness.png', dpi=300, bbox_inches='tight')
print("✓ Created pisa_overall_effectiveness.png")

# Figure 3: Test Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Test count by layer
test_counts = [11, 12, 12, 18]
colors_layers = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

ax1.bar(range(len(layers)), test_counts, color=colors_layers, alpha=0.8)
ax1.set_xlabel('PISA Layer', fontsize=11, fontweight='bold')
ax1.set_ylabel('Number of Tests', fontsize=11, fontweight='bold')
ax1.set_title('Test Distribution by Layer', fontsize=12, fontweight='bold')
ax1.set_xticks(range(len(layers)))
ax1.set_xticklabels(layers, fontsize=10)
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for i, count in enumerate(test_counts):
    ax1.text(i, count + 0.3, str(count), ha='center', fontsize=11, fontweight='bold')

# Right: Success/Failure breakdown
pisa_success = [10, 12, 10, 17]
pisa_failure = [1, 0, 2, 1]

x = np.arange(len(layers))
width = 0.6

bars1 = ax2.bar(x, pisa_success, width, label='Success', color='#2ecc71', alpha=0.8)
bars2 = ax2.bar(x, pisa_failure, width, bottom=pisa_success, label='Failure', color='#e74c3c', alpha=0.8)

ax2.set_xlabel('PISA Layer', fontsize=11, fontweight='bold')
ax2.set_ylabel('Number of Tests', fontsize=11, fontweight='bold')
ax2.set_title('PISA Success/Failure by Layer', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(layers, fontsize=10)
ax2.legend(fontsize=10)
ax2.grid(axis='y', alpha=0.3)

# Add percentage labels
for i, (success, failure) in enumerate(zip(pisa_success, pisa_failure)):
    total = success + failure
    pct = (success / total * 100) if total > 0 else 0
    ax2.text(i, total + 0.3, f'{pct:.1f}%', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('pisa_test_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Created pisa_test_distribution.png")

print("\n" + "="*60)
print("All visualizations created successfully!")
print("="*60)
print("\nGenerated files:")
print("  1. pisa_layer_comparison.png - Layer-by-layer effectiveness")
print("  2. pisa_overall_effectiveness.png - Overall performance metrics")
print("  3. pisa_test_distribution.png - Test distribution and breakdown")
