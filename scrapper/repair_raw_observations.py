"""
repair_raw_observations.py
--------------------------
Applies all provenance corrections to data/raw/raw_observations.csv:

1. Yuan Up trade quotations (OBS038, OBS039, OBS043, OBS047):
   - Corrected source_id from S003 (Landin) to S008 (unverified trade quotation).
   - source_url updated from landinparts.com to reflect the actual unverified trade source.
   - supplier corrected from 'China Auto Spare Parts Export Directory' (which never appeared
     in source_log.csv) to 'Unknown Export Supplier (Unverified Trade Quotation)'.
   - availability updated to 'unverified_quotation'.
   - evidence_type retained as 'trade_quotation'.
   - notes strengthened to flag that OEM numbers are trade listing codes, not independently
     verified against a manufacturer EPC or authorised dealer catalogue.

2. NHTSA rows (OBS058, OBS059):
   - Corrected source_id from S007 (AutoZone) to S006 (NHTSA).
   - source_url already points to nhtsa.gov — retained.

3. All rows: collection_date standardised to 2026-11-18 (actual collection date).

4. New column `observation_type` added to make row classification machine-readable:
   - 'supplier_catalogue': verified listing in a named supplier/manufacturer catalogue
   - 'catalogue_gap': searched catalogue; part not listed
   - 'trade_quotation_unverified': trade supplier price or part number, not EPC-verified
   - 'safety_context': NHTSA defect/recall data used as platform stress context only
"""

import pandas as pd

df = pd.read_csv('data/raw/raw_observations.csv')

# --------------------------------------------------------------------------
# FIX 1: Reclassify Yuan Up trade quotations
# These four observations were incorrectly attributed to S003 (Landin).
# They came from an unnamed export directory that is not in source_log.csv.
# We reclassify them to S008 (Unverified Trade Quotation) and correct the URL
# and supplier name so the provenance is honest.
# --------------------------------------------------------------------------
trade_quotation_ids = ['OBS038', 'OBS039', 'OBS043', 'OBS047']

for obs_id in trade_quotation_ids:
    mask = df['observation_id'] == obs_id
    df.loc[mask, 'source_id'] = 'S008'
    df.loc[mask, 'source_url'] = 'unverified_trade_quotation — URL not recorded at collection'
    df.loc[mask, 'supplier'] = 'Unknown Export Supplier (Unverified Trade Quotation)'
    df.loc[mask, 'availability'] = 'unverified_quotation'
    # Strengthen notes to be explicit
    existing_note = df.loc[mask, 'notes'].values[0]
    df.loc[mask, 'notes'] = (
        existing_note +
        ' | PROVENANCE CORRECTION 2026-11-19: source_id corrected from S003 (Landin) '
        'to S008. The URL was incorrectly recorded as landinparts.com/byd/; '
        'Landin carries zero Yuan Up listings. Part number is a trade listing code — '
        'NOT independently verified against a manufacturer EPC or authorised dealer catalogue. '
        'Do not treat as a confirmed OEM number.'
    )

# --------------------------------------------------------------------------
# FIX 2: Correct NHTSA rows source_id S007 → S006
# OBS058 and OBS059 reference the NHTSA database, which is S006 in source_log.csv.
# S007 is AutoZone / O'Reilly. The URL already points to nhtsa.gov correctly.
# --------------------------------------------------------------------------
nhtsa_ids = ['OBS058', 'OBS059']
for obs_id in nhtsa_ids:
    mask = df['observation_id'] == obs_id
    df.loc[mask, 'source_id'] = 'S006'

# --------------------------------------------------------------------------
# FIX 3: Standardise all collection_date to 2026-11-18
# Source log was dated 2026-11-17 (session start); actual observations were
# collected and recorded on 2026-11-18. The observation-level date takes precedence.
# --------------------------------------------------------------------------
df['collection_date'] = '2026-11-18'

# --------------------------------------------------------------------------
# FIX 4: Add observation_type column for machine-readable row classification
# --------------------------------------------------------------------------
def classify_observation(row):
    et = str(row.get('evidence_type', '')).strip().lower()
    if et == 'supplier_catalogue' or et == 'parts_catalogue':
        return 'supplier_catalogue'
    elif et == 'catalogue_gap':
        return 'catalogue_gap'
    elif et == 'trade_quotation':
        return 'trade_quotation_unverified'
    elif et == 'safety_defect_context':
        return 'safety_context'
    else:
        return 'unknown'

df['observation_type'] = df.apply(classify_observation, axis=1)

# Save corrected file
df.to_csv('data/raw/raw_observations.csv', index=False)

# Print summary
print("=== CORRECTION SUMMARY ===")
print(f"Total rows: {len(df)}")
print("\nObservation type breakdown:")
print(df['observation_type'].value_counts().to_string())
print("\nSource ID breakdown:")
print(df['source_id'].value_counts().to_string())
print("\nYuan Up rows (should all be S008 for trade quotations):")
yu_rows = df[df['vehicle'] == 'BYD Yuan Up'][['observation_id', 'part_category', 'source_id', 'observation_type', 'availability']]
print(yu_rows.to_string())
print("\nNHTSA rows (should be S006):")
nhtsa_rows = df[df['observation_type'] == 'safety_context'][['observation_id', 'vehicle', 'part_category', 'source_id']]
print(nhtsa_rows.to_string())
print("\nCollection dates (all should be 2026-11-18):")
print(df['collection_date'].unique())
