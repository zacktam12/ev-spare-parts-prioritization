"""
update_notebooks.py
-------------------
Updates notebook 03 and notebook 04 code cells to ensure full alignment
with the defensible scoring pipeline and clean reproducible CSV export.
"""

import nbformat

# ==============================================================================
# 1. UPDATE NOTEBOOK 03 (Data Cleaning)
# ==============================================================================
nb3 = nbformat.read('notebooks/03_data_cleaning.ipynb', as_version=4)

cell_cross_check = '''# Mark cross-checked observations
# Exclude safety_context (NHTSA) so safety context records do not falsely inflate part cross-check counts
direct_sources = cleaned[cleaned.get('observation_type', '') != 'safety_context']
source_counts = direct_sources.groupby(['vehicle', 'part_category'])['source_id'].nunique().reset_index()
source_counts.columns = ['vehicle', 'part_category', 'source_count']
source_counts['is_cross_checked'] = source_counts['source_count'] >= 2

cleaned = cleaned.merge(
    source_counts[['vehicle', 'part_category', 'is_cross_checked']],
    on=['vehicle', 'part_category'],
    how='left'
)
cleaned['is_cross_checked'] = cleaned['is_cross_checked'].fillna(False)

print(f"Cross-checked combinations: {source_counts['is_cross_checked'].sum()} / {len(source_counts)}")
print(f"Single-source combinations: {(~source_counts['is_cross_checked']).sum()} / {len(source_counts)}")
'''

cell_compatibility = '''# Classify compatibility evidence strength
def classify_compatibility(row):
    obs_type = row.get('observation_type', '')
    if obs_type == 'safety_context':
        return 'contextual_reference'
    if obs_type == 'catalogue_gap':
        return 'not_listed'
    if obs_type == 'trade_quotation_unverified':
        return 'unverified_trade_code'
    
    statement = str(row.get('compatibility_statement', '')).lower()
    has_oem = pd.notna(row.get('oem_part_number')) and str(row.get('oem_part_number')).strip() != '' and str(row.get('oem_part_number')).lower() not in ['not_listed', 'not_applicable']
    
    if has_oem and ('confirmed' in statement or 'oem' in statement or 'exact' in statement):
        return 'confirmed_oem'       # OEM part number + explicit compatibility statement
    elif has_oem:
        return 'catalogue_match'      # OEM part number found in catalogue
    elif 'compatible' in statement or 'fits' in statement:
        return 'generic_listing'      # Supplier claims compatibility without OEM number
    elif 'not' in statement:
        return 'not_verifiable'       # Listing exists but compatibility unclear
    else:
        return 'unknown'              # Insufficient information

cleaned['compatibility_strength'] = cleaned.apply(classify_compatibility, axis=1)
print("Compatibility strength distribution:")
print(cleaned['compatibility_strength'].value_counts())
'''

cell_save3 = '''# Save cleaned dataset using pandas to_csv ensuring clean quoting without field overflow
cleaned.to_csv('../data/cleaned/cleaned_observations.csv', index=False)
print(f"Cleaned dataset saved: {len(cleaned)} rows")
print("Output: data/cleaned/cleaned_observations.csv")

# Immediate verification that the exported CSV loads cleanly
test_df = pd.read_csv('../data/cleaned/cleaned_observations.csv')
print(f"Verification load check: {test_df.shape[0]} rows, {test_df.shape[1]} columns loaded without error.")
'''

for cell in nb3.cells:
    if cell.cell_type == 'code':
        if 'source_counts = cleaned.groupby' in cell.source or 'direct_sources = cleaned[' in cell.source:
            cell.source = cell_cross_check
        elif 'def classify_compatibility' in cell.source:
            cell.source = cell_compatibility
        elif "cleaned.to_csv('../data/cleaned/cleaned_observations.csv'" in cell.source:
            cell.source = cell_save3

nbformat.write(nb3, 'notebooks/03_data_cleaning.ipynb')
print("Updated notebook 03 successfully.")

# ==============================================================================
# 2. UPDATE NOTEBOOK 04 (Analysis and Scoring)
# ==============================================================================
nb4 = nbformat.read('notebooks/04_analysis_and_scoring.ipynb', as_version=4)

cell_load_scores = '''# Load the complete, evidence-justified scoring table covering all 30 vehicle-part combinations
import sys
sys.path.insert(0, '..')

from scraper.generate_scores_defensible import get_scoring_data
scores_data = get_scoring_data()

scores_df = pd.DataFrame(scores_data)
print(f"Scoring table loaded: {len(scores_df)} combinations across 3 vehicles and 10 categories.")
scores_df.head(10)
'''

cell_sensitivity = '''# Define alternative weight scenarios
scenarios = {
    'Original': {
        'demand_evidence': 0.30, 'market_scarcity': 0.25,
        'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.15,
        'evidence_confidence': 0.10
    },
    'Scarcity-first': {
        'demand_evidence': 0.25, 'market_scarcity': 0.30,
        'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.15,
        'evidence_confidence': 0.10
    },
    'Equal weights': {
        'demand_evidence': 0.20, 'market_scarcity': 0.20,
        'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.20,
        'evidence_confidence': 0.20
    },
    'Evidence-focused': {
        'demand_evidence': 0.25, 'market_scarcity': 0.20,
        'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.15,
        'evidence_confidence': 0.20
    }
}

# Calculate scores under each scenario
sensitivity_results = {}
for name, weights in scenarios.items():
    temp_df = scores_df.copy()
    temp_df['scenario_score'] = (
        temp_df['demand_evidence'] * weights['demand_evidence'] +
        temp_df['market_scarcity'] * weights['market_scarcity'] +
        temp_df['vehicle_compatibility'] * weights['vehicle_compatibility'] +
        temp_df['sourcing_practicality'] * weights['sourcing_practicality'] +
        temp_df['evidence_confidence'] * weights['evidence_confidence']
    )
    scores_df[f'score_{name}'] = temp_df['scenario_score']
    # Unique item identifier: vehicle + ' — ' + part_category
    ranked_items = (temp_df.sort_values(by='scenario_score', ascending=False)
                           .head(5)
                           .apply(lambda r: f"{r['vehicle']} — {r['part_category']}", axis=1)
                           .tolist())
    sensitivity_results[name] = ranked_items

# Display sensitivity rankings
sensitivity_df = pd.DataFrame(sensitivity_results)
sensitivity_df.index = [f"Rank {i+1}" for i in range(5)]
sensitivity_df
'''

cell_stability = '''# Check stability: how many of the original top 5 remain in each alternative scenario?
original_top5 = set(sensitivity_results['Original'])

print("=== Ranking Stability Analysis ===")
print(f"Baseline Top 5: {sensitivity_results['Original']}")
print()
for scenario_name, top5 in sensitivity_results.items():
    overlap = len(original_top5.intersection(set(top5)))
    stability_pct = (overlap / 5) * 100
    print(f"Scenario: {scenario_name:<20} | Top 5 Overlap: {overlap}/5 | Stability: {stability_pct:.0f}%")
'''

for cell in nb4.cells:
    if cell.cell_type == 'code':
        if 'from scraper.generate_scores' in cell.source or 'from scraper.generate_scores_defensible' in cell.source:
            cell.source = cell_load_scores
        elif "scenarios = {" in cell.source and "'Scarcity-first'" in cell.source or "'Equal weights'" in cell.source:
            cell.source = cell_sensitivity
        elif 'original_top5 = set(sensitivity_results' in cell.source:
            cell.source = cell_stability

nbformat.write(nb4, 'notebooks/04_analysis_and_scoring.ipynb')
print("Updated notebook 04 successfully.")
