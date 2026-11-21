"""
Export publication-quality charts for the presentation and report.
Reads data/scoring_results.csv and saves charts into reports/figures/
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('reports/figures', exist_ok=True)

# Load data
df = pd.read_csv('data/scoring_results.csv')

# Configure styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 11

# 1. HEATMAP OF 30 COMBINATIONS (3 vehicles x 10 categories)
pivot_df = df.pivot(index='part_category', columns='vehicle', values='priority_score')
# Sort by Seagull score descending
pivot_df = pivot_df.sort_values(by='BYD Seagull', ascending=False)

plt.figure(figsize=(10, 7), dpi=300)
ax = sns.heatmap(pivot_df, annot=True, fmt='.2f', cmap='YlGnBu', cbar_kws={'label': 'Priority Score (Max 5.0)'},
                 linewidths=1.2, linecolor='white')
plt.title('Priority Score Matrix: 30 EV Vehicle-Part Combinations', fontsize=14, weight='bold', pad=15)
plt.xlabel('Vehicle Model', fontsize=12, labelpad=10)
plt.ylabel('Spare-Part Category', fontsize=12, labelpad=10)
plt.tight_layout()
plt.savefig('reports/figures/scoring_matrix_heatmap.png')
plt.close()
print("Saved scoring_matrix_heatmap.png")

# 2. TOP 10 RANKED PARTS BAR CHART
top10 = df.sort_values(by=['priority_score', 'demand_evidence'], ascending=[False, False]).head(10).copy()
top10['label'] = top10['vehicle'] + ' — ' + top10['part_category']
top10 = top10.sort_values(by=['priority_score', 'demand_evidence'], ascending=[True, True])

plt.figure(figsize=(11, 6), dpi=300)
colors = ['#2b5c8f' if 'Seagull' in lbl else '#c2593f' if 'Toyota' in lbl else '#2a9d8f' for lbl in top10['label']]
bars = plt.barh(top10['label'], top10['priority_score'], color=colors, height=0.65)
plt.xlim(3.0, 5.0)
plt.xlabel('Priority Score (0.30D + 0.25S + 0.20C + 0.15P + 0.10E)', fontsize=12, labelpad=10)
plt.title('Top 10 EV Spare-Parts Import Priority Rankings', fontsize=14, weight='bold', pad=15)

for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.03, bar.get_y() + bar.get_height()/2, f'{w:.2f}', va='center', ha='left', fontsize=10, weight='bold')

plt.tight_layout()
plt.savefig('reports/figures/top10_priority_rankings.png')
plt.close()
print("Saved top10_priority_rankings.png")

# 3. SENSITIVITY COMPARISON ACROSS 4 SCENARIOS
scenarios = {
    'Original (Baseline)': {'D': 0.30, 'S': 0.25, 'C': 0.20, 'P': 0.15, 'E': 0.10},
    'Scarcity-First': {'D': 0.25, 'S': 0.30, 'C': 0.20, 'P': 0.15, 'E': 0.10},
    'Equal-Weights': {'D': 0.20, 'S': 0.20, 'C': 0.20, 'P': 0.20, 'E': 0.20},
    'Evidence-Focused': {'D': 0.25, 'S': 0.20, 'C': 0.20, 'P': 0.15, 'E': 0.20}
}

top5_df = df.sort_values(by=['priority_score', 'demand_evidence'], ascending=[False, False]).head(5)
top5_labels = (top5_df['vehicle'] + ' — ' + top5_df['part_category']).tolist()

# Plot Sensitivity Bar Chart for the Top 5
plt.figure(figsize=(12, 6), dpi=300)
x = np.arange(5)
width = 0.2

for i, (name, weights) in enumerate(scenarios.items()):
    temp_scores = []
    for idx, row in top5_df.iterrows():
        s = (weights['D'] * row['demand_evidence'] +
             weights['S'] * row['market_scarcity'] +
             weights['C'] * row['vehicle_compatibility'] +
             weights['P'] * row['sourcing_practicality'] +
             weights['E'] * row['evidence_confidence'])
        temp_scores.append(s)
    plt.bar(x + i*width, temp_scores, width, label=name)

plt.xlabel('Top 5 Recommended Vehicle-Part Combinations', fontsize=12, labelpad=10)
plt.ylabel('Scenario Score (Max 5.0)', fontsize=12, labelpad=10)
plt.title('Stability Across 4 Predefined Weighting Scenarios (100% Set Overlap)', fontsize=14, weight='bold', pad=15)
plt.xticks(x + width*1.5, [lbl.replace(' — ', '\n') for lbl in top5_labels], fontsize=9)
plt.ylim(3.5, 5.0)
plt.legend(frameon=True, facecolor='white', loc='lower right')
plt.tight_layout()
plt.savefig('reports/figures/sensitivity_comparison.png')
plt.close()
print("Saved sensitivity_comparison.png")

# 4. RADAR CHART FOR TOP 5
categories = ['Demand Proxy\n(30%)', 'Catalogue Gap\n(25%)', 'Compatibility\n(20%)', 'Sourcing\n(15%)', 'Confidence\n(10%)']
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)

palette = ['#e63946', '#1d3557', '#457b9d', '#2a9d8f', '#e76f51']
for i, (_, row) in enumerate(top5_df.iterrows()):
    values = [row['demand_evidence'], row['market_scarcity'], row['vehicle_compatibility'],
              row['sourcing_practicality'], row['evidence_confidence']]
    values += values[:1]
    lbl = f"{row['vehicle']} {row['part_category']} ({row['priority_score']:.2f})"
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=lbl, color=palette[i])
    ax.fill(angles, values, color=palette[i], alpha=0.1)

plt.xticks(angles[:-1], categories, size=11, weight='bold')
ax.set_rlabel_position(0)
plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=9)
plt.ylim(0, 5.5)
plt.title('Multi-Factor Dimension Profiles: Top 5 Recommended Parts', size=14, weight='bold', y=1.08)
plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=9)
plt.tight_layout()
plt.savefig('reports/figures/top5_radar_profiles.png')
plt.close()
print("Saved top5_radar_profiles.png")

# 5. MONTE-CARLO STABILITY (Top-5 inclusion probability over Dirichlet weight draws)
# Produced by scraper/generate_scores_defensible.py -> data/sensitivity_monte_carlo.csv.
# Unlike the 4-scenario chart, this draws 2,000 weight vectors uniformly from the
# 5-factor simplex, so it measures robustness without depending on hand-picked weights.
mc = pd.read_csv('data/sensitivity_monte_carlo.csv')
ROBUST_THRESHOLD = 80.0  # %

mc_top = mc[mc['p_top5'] > 0].head(12).copy()
mc_top['label'] = mc_top['vehicle'] + ' — ' + mc_top['part_category']
mc_top = mc_top.sort_values('p_top5', ascending=True)

plt.figure(figsize=(11, 6.5), dpi=300)
color_map = {'robust': '#2a9d8f', 'sensitive': '#e9c46a'}
bar_colors = [color_map.get(s, '#adb5bd') for s in mc_top['stability']]
bars = plt.barh(mc_top['label'], mc_top['p_top5'] * 100.0, color=bar_colors, height=0.68)

plt.axvline(ROBUST_THRESHOLD, color='#c1121f', linestyle='--', linewidth=1.6)
plt.text(ROBUST_THRESHOLD + 1.0, -0.9, f'{ROBUST_THRESHOLD:.0f}% robustness threshold',
         color='#c1121f', fontsize=9, va='center', ha='left')

for bar in bars:
    w = bar.get_width()
    plt.text(w + 1.2, bar.get_y() + bar.get_height() / 2, f'{w:.1f}%',
             va='center', ha='left', fontsize=9, weight='bold')

plt.xlim(0, 108)
plt.xlabel('Top-5 inclusion probability across 2,000 Dirichlet weight draws (%)', fontsize=12, labelpad=10)
plt.title('Monte-Carlo Robustness: How Often Each Combination Ranks Top-5',
          fontsize=14, weight='bold', pad=15)
plt.tight_layout()
plt.savefig('reports/figures/monte_carlo_stability.png')
plt.close()
print("Saved monte_carlo_stability.png")
