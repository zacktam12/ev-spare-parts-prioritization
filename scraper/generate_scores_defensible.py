"""
generate_scores_defensible.py
------------------------------
Authoritative scoring and sensitivity analysis module for the EV spare parts prioritization.

UNIT OF ANALYSIS:
The scoring model evaluates 30 distinct Vehicle Model + Part Category combinations
(3 vehicles x 10 categories). Recommendations represent prioritized part categories
accompanied by specific supplier-listed OE applications for implementation.

ANALYST JUDGEMENT DISCLOSURE & SCORING RUBRIC:
==============================================
Scores represent structured analyst judgements grounded in evidence collected in
data/raw/raw_observations.csv and data/source_log.csv.
They are NOT algorithmically derived from raw row counts.

D — Demand Evidence Proxy (30% Weight)
  Grounded in: Observed vehicle marketplace presence in S001 (Adey Market active listings)
  and component functional classification (routine friction/wear vs exterior contact vs structural).
  *Important: Indicative assessment proxy; no on-the-ground Ethiopian workshop replacement rates were measured.*
  5 = Dominant vehicle market presence on Adey (e.g. BYD Seagull / Yuan Up) + primary friction wear
      or high-exposure exterior contact component (analyst assessment).
  4 = High/moderate vehicle presence on Adey + secondary wear or collision-repair component.
  3 = Moderate vehicle presence + slower-wearing mechanical component (e.g. brake discs,
      where regenerative braking typically extends service life) or secondary body panel.
  2 = Lower vehicle presence or rarely replaced structural part.
  1 = Minimal marketplace presence or negligible replacement indication.

S — Local Distributor Catalogue Gap (25% Weight)
  Grounded in: The degree to which a part is absent from the investigated parts catalogues
  (S003 Landin, S005 third-party) and the investigated local distributor channel (S002 Gezat).
  *Important: Measures investigated public catalogue gaps only; does NOT establish physical
  unavailability in Addis Ababa shops. The S002 Gezat review was conducted at catalogue/model
  level only and no per-part search was recorded, so local per-part availability is UNVERIFIED
  and S is an analyst judgement (documented limitation, see reports/limitations.md).*
  5 = No listing in any of the investigated parts catalogues (e.g. Yuan Up categories, Seagull cabin filter).
  4 = Not carried by a local distributor channel and listed only by an overseas supplier (Landin S003 / toyota-spare-parts.com S005); local per-part availability unverified.
  3 = Standard overseas availability with common aftermarket cross-references, or limited / incomplete application information.
  2 = Broadly cross-compatible application supported by evidence (e.g. shared across TNGA platform models).
  1 = Clearly listed and locally available part number (no S=1 rows in the current model).

C — Vehicle Compatibility (20% Weight)
  Grounded in: Verification level of part number in named source catalogues.
  5 = Supplier-listed OE reference confirmed in named supplier catalogue (Landin S003) with an
      explicit vehicle model compatibility statement.
  4 = Part number listed in third-party parts catalogue (toyota-spare-parts.com S005) with
      chassis diagram (XEAM10), pending independent Toyota dealer EPC confirmation.
  2 = Trade listing code from unverified export directory (S008); format not confirmed by OEM EPC.
  1 = Catalogue gap — no part number or fitment evidence found in investigated sources.

P — Catalogue Sourcing Practicality (15% Weight)
  Grounded in: Active listing status and transparent unit catalogue price visibility applied to
  the exact primary representative application evaluated.
  (Measures catalogue price visibility and indicative unit capital exposure; does not assume
  freight quotes, minimum order quantities, customs tariffs, or landed costs).
  5 = Active catalogue listing with transparent unit price under $50 USD.
  4 = Active catalogue listing with transparent unit price between $50 and $250 USD.
  3 = Active catalogue listing with unit price over $250 USD, or listed as "Price on request".
  1 = Unverified trade quotation (S008) or catalogue gap (no verified supplier, no verifiable price).
  *Application Aggregation Rule: Category-level scoring evaluates the primary representative
  application explicitly cited in recommendations (e.g. Left-hand mirror EQEA-8202100 at $60.06 -> P=4;
  Front shock absorber strut EQEA-2905100A at $19.32 -> P=5; Front brake pad set EQEA-3501500CH at $8.96 -> P=5;
  Front bumper cover EQEA-2083111 at $27.72 -> P=5; Left headlight assembly EQEA-4121010B at $58.52 -> P=4).
  Coexisting secondary variants or unpriced entries within the same category are documented for transparency,
  but do not override the verified price of the primary application.*

E — Evidence Confidence (10% Weight)
  Grounded in: Primary source verification and independent cross-checking.
  5 = Named supplier catalogue listing (Landin S003) corroborated with secondary reference (CQSW S004).
  4 = Named supplier catalogue listing with supplier-listed OE reference (single named source).
  3 = Third-party aggregator catalogue listing (toyota-spare-parts.com S005).
  1 = Unverified trade quotation (S008) or catalogue gap record.

NHTSA SAFETY DATA CONTEXT:
--------------------------
NHTSA defect records (OBS058, OBS059 / S006) are classified as 'safety_context'.
They provide engineering platform context only and do NOT contribute to Demand,
Compatibility, or Evidence Confidence scores.
"""

import pandas as pd
import numpy as np

WEIGHTS = {
    'Original': {'demand_evidence': 0.30, 'market_scarcity': 0.25, 'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.15, 'evidence_confidence': 0.10},
    'Scarcity-first': {'demand_evidence': 0.25, 'market_scarcity': 0.30, 'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.15, 'evidence_confidence': 0.10},
    'Equal weights': {'demand_evidence': 0.20, 'market_scarcity': 0.20, 'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.20, 'evidence_confidence': 0.20},
    'Evidence-focused': {'demand_evidence': 0.25, 'market_scarcity': 0.20, 'vehicle_compatibility': 0.20, 'sourcing_practicality': 0.15, 'evidence_confidence': 0.20},
}

# Factor order used by the Monte-Carlo engine (must match db/schema.sql column order).
FACTOR_COLUMNS = [
    'demand_evidence', 'market_scarcity', 'vehicle_compatibility',
    'sourcing_practicality', 'evidence_confidence',
]

N_MONTE_CARLO = 2000
MC_SEED = 42
MC_TOP_N = 5


def get_scoring_data():
    return [
        # =========================================================================
        # 1. BYD SEAGULL (35 Listings in Landin S003; 8 Categories Priced)
        # =========================================================================
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Side mirror',
            'demand_evidence': 5,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 4,
            'evidence_confidence': 5,
            'score_justification': (
                'D=5: High Adey Market presence (37 Seagull listings in the collected Adey sample — scraper/outputs/adey_cleaned.csv) + high exterior contact exposure (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: Supplier-listed OE references EQEA-8202100 (LH) / EQEA-8202109 (RH) confirmed in Landin with SEAGULL compatibility statement [OBS019, OBS020 / S003]. '
                'P=4: Active catalogue listing; primary evaluated application is Left exterior mirror assembly (EQEA-8202100) at 429 RMB ($60.06 USD), falling into the $50-$250 bracket (companion RH mirror EQEA-8202109 is 264 RMB / $36.96 USD). '
                'E=5: Landin named catalogue; OE reference corroborated by CQSW benchmark [S003, S004].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Brake pads',
            'demand_evidence': 4,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 5,
            'evidence_confidence': 5,
            'score_justification': (
                'D=4: High Adey presence + routine friction wear consumable (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: Supplier-listed OE references EQEA-3501500CH (Front) / EQEA-3502140SS (Rear) confirmed in Landin with SEAGULL compatibility [OBS024, OBS025 / S003]. '
                'P=5: Active catalogue listing; evaluated application is Front brake pad set at 64 RMB ($8.96 USD) per set (<$50 bracket; companion Rear pad set also 64 RMB). '
                'E=5: Landin catalogue listing; OE reference corroborated by CQSW benchmark [S003, S004].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Shock absorber',
            'demand_evidence': 4,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 5,
            'evidence_confidence': 5,
            'score_justification': (
                'D=4: High Adey presence + suspension damping wear component on rough topography (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: Supplier-listed OE references EQEA-2905100A (LH) / EQEA-2905200A (RH) confirmed in Landin with SEAGULL statement [OBS021, OBS022 / S003]. '
                'P=5: Active catalogue listing; evaluated application is Front shock absorber strut (LH EQEA-2905100A) at 138 RMB ($19.32 USD) per strut (<$50 bracket; companion RH strut also 138 RMB). '
                'E=5: Landin named catalogue; EQEA- prefix format corroborated by CQSW benchmark [S003, S004].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Headlight assembly',
            'demand_evidence': 4,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 4,
            'evidence_confidence': 5,
            'score_justification': (
                'D=4: High Adey presence + frontal collision damage exposure (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: Supplier-listed OE references EQEA-4121010B (LH) / EQEA-4121020B (RH) confirmed in Landin [OBS013, OBS014 / S003]. '
                'P=4: Active catalogue listing; evaluated application is Left headlight assembly (EQEA-4121010B) at 418 RMB ($58.52 USD), falling into the $50-$250 bracket (companion RH headlight also 418 RMB). '
                'E=5: Two Landin SKUs; EQEA- prefix corroborated by CQSW benchmark [S003, S004].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Bumper',
            'demand_evidence': 4,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 5,
            'evidence_confidence': 5,
            'score_justification': (
                'D=4: High Adey presence + urban low-speed frontal contact exposure (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: Supplier-listed OE references EQEA-2083111 (Front upper) / EQEA-2804110A/00 (Rear) confirmed in Landin [OBS001, OBS004, OBS028 / S003]. '
                'P=5: Active catalogue listing; evaluated application is Front bumper cover upper fascia (EQEA-2083111) at 198 RMB ($27.72 USD), falling into the <$50 bracket (coexisting lower grille EQEA-2803112 is 88 RMB / $12.32 USD; companion rear bumper EQEA-2804110A/00 is 198 RMB / $27.72 USD in OBS028). '
                'E=5: Five Landin SKUs covering front and rear assemblies. NOTE (OE-verification flag): the primary front-upper reference EQEA-2083111 does NOT match the CQSW benchmark reference for that component, so it is NOT cross-source corroborated and is flagged for supplier confirmation (see OBS001 note); the EQEA- prefix format itself is consistent with the CQSW benchmark [S003, S004].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Brake discs',
            'demand_evidence': 3,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 5,
            'evidence_confidence': 5,
            'score_justification': (
                'D=3: Slower wear cycle than pads due to EV regenerative braking assist (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: Supplier-listed OE references EM2E-3501011 (Front) / EM2E-3502111 (Rear) confirmed in Landin [OBS034, OBS035 / S003]. '
                'P=5: Active catalogue listing; evaluated application is Front brake disc (EM2E-3501011) at 108 RMB ($15.12 USD), falling into the <$50 bracket (companion rear disc is 94 RMB / $13.16 USD). '
                'E=5: Two Landin SKUs; rotor part numbers corroborated by CQSW benchmark [S003, S004].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Tail-light assembly',
            'demand_evidence': 3,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 4,
            'evidence_confidence': 5,
            'score_justification': (
                'D=3: Rear impact replacement item; lower turnover than frontal components (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: Supplier-listed OE references EQEA-4133010 (Outer LH) / EQEA-4133020 (Outer RH) / EQEA-4107300 (Center bar) confirmed in Landin [OBS015-OBS017 / S003]. '
                'P=4: Active catalogue listing; outer lamps are 198 RMB ($27.72 USD) and full center bar assembly is 528 RMB ($73.92 USD), falling into the $50-$250 bracket. '
                'E=5: Three distinct Landin SKUs; EQEA- prefix corroborated by CQSW benchmark [S003, S004].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Fender / body panel',
            'demand_evidence': 3,
            'market_scarcity': 4,
            'vehicle_compatibility': 5,
            'sourcing_practicality': 3,
            'evidence_confidence': 5,
            'score_justification': (
                'D=3: Collision-only sheet metal panels; slower replacement turnover (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas supplier (Landin S003). '
                'C=5: 16 confirmed Landin SKUs covering door panels, fenders, hood [OBS005-OBS012, OBS018, OBS026-OBS033 / S003]. '
                'P=3: Active catalogue listing, but multiple primary body panels are listed as "Price on request" (OBS005-OBS012, OBS018) in supplier catalogue. '
                'E=5: 16 distinct Landin SKUs; EQEA- and 14549- prefixes confirmed [S003].'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Cabin-air filter',
            'demand_evidence': 4,
            'market_scarcity': 5,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=4: Routine air quality maintenance consumable (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=1: CATALOGUE GAP: Zero part number or fitment evidence in investigated catalogues [OBS036 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price in investigated sources. '
                'E=1: CATALOGUE GAP: No primary catalogue evidence.'
            )
        },
        {
            'vehicle': 'BYD Seagull',
            'part_category': 'Wiper blades',
            'demand_evidence': 4,
            'market_scarcity': 3,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=4: Annual wear consumable (indicative demand proxy). '
                'S=3: Standard overseas availability via universal wiper sizing; absent from investigated local catalogue Gezat S002. '
                'C=1: CATALOGUE GAP: Zero Seagull-specific blade part number in investigated catalogues [OBS037 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price in investigated sources. '
                'E=1: CATALOGUE GAP: No primary catalogue evidence.'
            )
        },

        # =========================================================================
        # 2. TOYOTA bZ4X (10 Listings in Third-Party Catalogue S005)
        # =========================================================================
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Shock absorber',
            'demand_evidence': 4,
            'market_scarcity': 4,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 4,
            'evidence_confidence': 3,
            'score_justification': (
                'D=4: Heavy EV curb weight (>2,000 kg) on Ethiopian road topography (indicative demand proxy; NHTSA hub-bolt recall explicitly excluded from D score). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas third-party catalogue (S005). '
                'C=4: OE 48520-42290 listed in third-party catalogue (toyota-spare-parts.com S005) for chassis XEAM10; pending independent authorised dealer confirmation. '
                'P=4: Listed with catalogue price of $240.00 USD ($50-$250 bracket) [OBS057 / S005]. '
                'E=3: Third-party aggregator catalogue; NHTSA context excluded from evidence count.'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Side mirror',
            'demand_evidence': 4,
            'market_scarcity': 4,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 3,
            'evidence_confidence': 3,
            'score_justification': (
                'D=4: Moderate-volume Adey vehicle + exterior collision contact item (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas third-party catalogue (S005). '
                'C=4: OE 87910-42E10 listed in third-party catalogue [OBS054 / S005]. '
                'P=3: High unit catalogue price: $460.00 USD (>$250 bracket; increased capital exposure). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Brake pads',
            'demand_evidence': 4,
            'market_scarcity': 3,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 4,
            'evidence_confidence': 3,
            'score_justification': (
                'D=4: Heavy vehicle mass friction wear consumable (indicative demand proxy; NHTSA brake complaint OBS059 explicitly excluded). '
                'S=3: Absent from investigated Gezat catalogue, but standard availability in global Toyota catalogue channels. '
                'C=4: OE 04465-42250 listed in third-party catalogue [OBS048 / S005]. '
                'P=4: Listed with catalogue price of $78.50 USD ($50-$250 bracket). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Cabin-air filter',
            'demand_evidence': 4,
            'market_scarcity': 2,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 5,
            'evidence_confidence': 3,
            'score_justification': (
                'D=4: Periodic maintenance consumable (indicative demand proxy). '
                'S=2: Broadly cross-compatible application supported by evidence (OE 87139-58010 shared across multiple Toyota TNGA models), reducing catalogue gap. '
                'C=4: OE 87139-58010 listed in third-party catalogue [OBS050 / S005]. '
                'P=5: Listed with catalogue price of $24.00 USD (<$50 bracket). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Wiper blades',
            'demand_evidence': 4,
            'market_scarcity': 2,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 5,
            'evidence_confidence': 3,
            'score_justification': (
                'D=4: Periodic maintenance consumable (indicative demand proxy). '
                'S=2: Broadly cross-compatible application supported by evidence (universal sizing shared across Toyota models), reducing catalogue gap. '
                'C=4: OE 85212-42140 listed in third-party catalogue [OBS051 / S005]. '
                'P=5: Listed with catalogue price of $32.00 USD (<$50 bracket). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Bumper',
            'demand_evidence': 4,
            'market_scarcity': 4,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 3,
            'evidence_confidence': 3,
            'score_justification': (
                'D=4: Front collision repair item (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas third-party catalogue (S005). '
                'C=4: OE 52119-42C40 listed in third-party catalogue [OBS055 / S005]. '
                'P=3: High unit catalogue price: $520.00 USD (>$250 bracket). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Tail-light assembly',
            'demand_evidence': 3,
            'market_scarcity': 4,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 3,
            'evidence_confidence': 3,
            'score_justification': (
                'D=3: Rear collision repair item; lower turnover (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas third-party catalogue (S005). '
                'C=4: OE 81550-42240 listed in third-party catalogue [OBS053 / S005]. '
                'P=3: High unit catalogue price: $395.00 USD (>$250 bracket). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Fender / body panel',
            'demand_evidence': 3,
            'market_scarcity': 4,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 3,
            'evidence_confidence': 3,
            'score_justification': (
                'D=3: Collision-only quarter panel replacement (indicative demand proxy). '
                'S=4: Not carried by the investigated local distributor channel (Gezat S002 review was catalogue/model-level only — no per-part search recorded, so local per-part availability is UNVERIFIED); listed by overseas third-party catalogue (S005). '
                'C=4: OE 53812-42240 listed in third-party catalogue [OBS056 / S005]. '
                'P=3: High unit catalogue price: $285.00 USD (>$250 bracket). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Headlight assembly',
            'demand_evidence': 3,
            'market_scarcity': 5,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 3,
            'evidence_confidence': 3,
            'score_justification': (
                'D=3: Frontal collision damage item (indicative demand proxy). '
                'S=5: No listing with active availability in any investigated relevant catalogue (available on order only in third-party catalogue S005; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=4: OE 81110-42B20 listed in third-party catalogue [OBS052 / S005]. '
                'P=3: Highest unit catalogue price in dataset: $1,180.00 USD (extreme capital exposure). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },
        {
            'vehicle': 'Toyota bZ4X',
            'part_category': 'Brake discs',
            'demand_evidence': 3,
            'market_scarcity': 3,
            'vehicle_compatibility': 4,
            'sourcing_practicality': 4,
            'evidence_confidence': 3,
            'score_justification': (
                'D=3: Regenerative braking extends disc replacement intervals (indicative demand proxy). '
                'S=3: Absent from investigated Gezat catalogue, but standard cast-iron rotor available through global Toyota catalogue channels. '
                'C=4: OE 43512-42150 listed in third-party catalogue [OBS049 / S005]. '
                'P=4: Listed with catalogue price of $115.00 USD ($50-$250 bracket). '
                'E=3: Third-party aggregator catalogue (S005).'
            )
        },

        # =========================================================================
        # 3. BYD YUAN UP (10 Categories; Landin Catalogue Gap S003 + 4 Quotes S008)
        # =========================================================================
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Side mirror',
            'demand_evidence': 5,
            'market_scarcity': 5,
            'vehicle_compatibility': 2,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=5: Dominant market presence (36 Yuan Up listings in the collected Adey sample — scraper/outputs/adey_cleaned.csv) + high exterior contact exposure (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=2: UNVERIFIED TRADE QUOTATION: Code BYD-YU-8202100 is from an unverified export directory [OBS039 / S008]; format not confirmed by OEM EPC. '
                'P=1: UNVERIFIED TRADE QUOTATION: Sourcing practicality scored 1 because no verified supplier catalogue listing exists. '
                'E=1: Unverified trade quotation (S008); Landin has zero Yuan Up parts.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Brake pads',
            'demand_evidence': 4,
            'market_scarcity': 5,
            'vehicle_compatibility': 2,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=4: Dominant market presence + routine friction wear consumable (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=2: UNVERIFIED TRADE QUOTATION: Code BYD-YU-3501500 is from an unverified export directory [OBS038 / S008]; format not confirmed by OEM EPC. '
                'P=1: UNVERIFIED TRADE QUOTATION: Sourcing practicality scored 1 because no verified supplier catalogue listing exists. '
                'E=1: Unverified trade quotation (S008); Landin has zero Yuan Up parts.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Headlight assembly',
            'demand_evidence': 4,
            'market_scarcity': 5,
            'vehicle_compatibility': 2,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=4: Dominant market presence + front collision damage exposure (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=2: UNVERIFIED TRADE QUOTATION: Code BYD-YU-4121020 is from an unverified export directory [OBS043 / S008]; format not confirmed by OEM EPC. '
                'P=1: UNVERIFIED TRADE QUOTATION: Sourcing practicality scored 1 because no verified supplier catalogue listing exists. '
                'E=1: Unverified trade quotation (S008); Landin has zero Yuan Up parts.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Shock absorber',
            'demand_evidence': 4,
            'market_scarcity': 5,
            'vehicle_compatibility': 2,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=4: Dominant market presence + suspension damping wear component (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=2: UNVERIFIED TRADE QUOTATION: Code BYD-YU-2905100 is from an unverified export directory [OBS047 / S008]; format not confirmed by OEM EPC. '
                'P=1: UNVERIFIED TRADE QUOTATION: Sourcing practicality scored 1 because no verified supplier catalogue listing exists. '
                'E=1: Unverified trade quotation (S008); Landin has zero Yuan Up parts.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Cabin-air filter',
            'demand_evidence': 4,
            'market_scarcity': 5,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=4: Routine air quality maintenance consumable (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=1: CATALOGUE GAP: Zero part number or fitment evidence in investigated catalogues [OBS040 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price. '
                'E=1: CATALOGUE GAP: Zero primary catalogue evidence.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Brake discs',
            'demand_evidence': 3,
            'market_scarcity': 5,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=3: Slower wear cycle due to regenerative braking assist (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=1: CATALOGUE GAP: Zero part number or fitment evidence in investigated catalogues [OBS041 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price. '
                'E=1: CATALOGUE GAP: Zero primary catalogue evidence.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Wiper blades',
            'demand_evidence': 3,
            'market_scarcity': 5,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=3: Annual wear consumable (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=1: CATALOGUE GAP: Zero part number or fitment evidence in investigated catalogues [OBS042 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price. '
                'E=1: CATALOGUE GAP: Zero primary catalogue evidence.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Bumper',
            'demand_evidence': 3,
            'market_scarcity': 5,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=3: Front/rear collision repair item (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=1: CATALOGUE GAP: Zero part number or fitment evidence in investigated catalogues [OBS045 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price. '
                'E=1: CATALOGUE GAP: Zero primary catalogue evidence.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Tail-light assembly',
            'demand_evidence': 3,
            'market_scarcity': 5,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=3: Rear collision repair item (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=1: CATALOGUE GAP: Zero part number or fitment evidence in investigated catalogues [OBS044 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price. '
                'E=1: CATALOGUE GAP: Zero primary catalogue evidence.'
            )
        },
        {
            'vehicle': 'BYD Yuan Up',
            'part_category': 'Fender / body panel',
            'demand_evidence': 3,
            'market_scarcity': 5,
            'vehicle_compatibility': 1,
            'sourcing_practicality': 1,
            'evidence_confidence': 1,
            'score_justification': (
                'D=3: Collision-only quarter panel replacement (indicative demand proxy). '
                'S=5: No listing in any of the investigated relevant catalogues (Landin S003 confirmed gap; Gezat S002 review was catalogue/model-level only with no per-part search recorded). '
                'C=1: CATALOGUE GAP: Zero part number or fitment evidence in investigated catalogues [OBS046 / S003]. '
                'P=1: CATALOGUE GAP: No verified supplier or price. '
                'E=1: CATALOGUE GAP: Zero primary catalogue evidence.'
            )
        },
    ]


def calculate_scores(df=None, weights=None):
    """
    Authoritative priority score calculation engine.
    Calculates weighted priority scores and ranks combinations.
    """
    if df is None:
        df = pd.DataFrame(get_scoring_data())
    else:
        df = df.copy()

    w = weights if weights else WEIGHTS['Original']
    df['priority_score'] = (
        w['demand_evidence'] * df['demand_evidence'] +
        w['market_scarcity'] * df['market_scarcity'] +
        w['vehicle_compatibility'] * df['vehicle_compatibility'] +
        w['sourcing_practicality'] * df['sourcing_practicality'] +
        w['evidence_confidence'] * df['evidence_confidence']
    )

    for scenario, sw in WEIGHTS.items():
        col_name = f"score_{scenario.replace('-', '_').replace(' ', '_')}"
        df[col_name] = (
            sw['demand_evidence'] * df['demand_evidence'] +
            sw['market_scarcity'] * df['market_scarcity'] +
            sw['vehicle_compatibility'] * df['vehicle_compatibility'] +
            sw['sourcing_practicality'] * df['sourcing_practicality'] +
            sw['evidence_confidence'] * df['evidence_confidence']
        )

    # Sort primarily by priority_score descending, and secondarily by demand_evidence descending
    df = df.sort_values(['priority_score', 'demand_evidence'], ascending=[False, False]).reset_index(drop=True)
    df['rank'] = df.index + 1
    return df


def run_sensitivity_analysis(df=None):
    """
    Authoritative sensitivity analysis comparing 4 weighting scenarios.
    Returns (sensitivity_df, stability_summary_dict).
    """
    if df is None or 'priority_score' not in df.columns:
        df = calculate_scores(df)

    sensitivity_results = {}
    baseline_top5 = set(
        (df.head(5)['vehicle'] + ' — ' + df.head(5)['part_category']).tolist()
    )

    stability_summary = {}
    for name, sw in WEIGHTS.items():
        temp_df = df.copy()
        temp_df['sc_score'] = (
            sw['demand_evidence'] * temp_df['demand_evidence'] +
            sw['market_scarcity'] * temp_df['market_scarcity'] +
            sw['vehicle_compatibility'] * temp_df['vehicle_compatibility'] +
            sw['sourcing_practicality'] * temp_df['sourcing_practicality'] +
            sw['evidence_confidence'] * temp_df['evidence_confidence']
        )
        ranked_items = (
            temp_df.sort_values(by=['sc_score', 'demand_evidence'], ascending=[False, False])
                   .head(5)
                   .apply(lambda r: f"{r['vehicle']} — {r['part_category']}", axis=1)
                   .tolist()
        )
        sensitivity_results[name] = ranked_items
        overlap = len(baseline_top5.intersection(set(ranked_items)))
        stability_summary[name] = {
            'top5': ranked_items,
            'overlap': overlap,
            'stability_pct': (overlap / 5.0) * 100.0
        }

    sens_df = pd.DataFrame(sensitivity_results)
    sens_df.index = [f"Rank {i+1}" for i in range(5)]
    return sens_df, stability_summary


def run_monte_carlo(df=None, n_sim=N_MONTE_CARLO, alpha=1.0, seed=MC_SEED, top_n=MC_TOP_N):
    """
    Monte-Carlo robustness test over Dirichlet weight draws.

    The four-scenario table in `run_sensitivity_analysis` only tests hand-picked
    weight vectors, so "100% stable" is partly a statement about the analyst's choice
    of scenarios. This test removes that dependence: it draws `n_sim` weight vectors
    uniformly from the 5-factor simplex (Dirichlet(alpha)) and records how often each
    combination lands in the Top-N. The resulting inclusion probability `p_top5` is the
    defensible stability statement.

    Deterministic: identical (seed, n_sim, alpha) always reproduce the same output.

    Returns (mc_df, summary_dict).
    """
    if df is None or 'priority_score' not in df.columns:
        df = calculate_scores(df)

    rng = np.random.default_rng(seed)
    factor_matrix = df[FACTOR_COLUMNS].to_numpy(dtype=float)
    weights = rng.dirichlet(np.full(len(FACTOR_COLUMNS), float(alpha)), size=n_sim)

    simulated = weights @ factor_matrix.T              # (n_sim, 30) weighted scores
    winners = np.argsort(-simulated, axis=1)[:, :top_n]
    counts = np.bincount(winners.ravel(), minlength=len(df))

    mc = df[['vehicle', 'part_category', 'rank', 'priority_score']].copy()
    mc['p_top5'] = counts / float(n_sim)
    mc['stability'] = np.where(
        mc['p_top5'] >= 0.80, 'robust',
        np.where(mc['p_top5'] > 0.0, 'sensitive', 'excluded'))
    mc = mc.sort_values(['p_top5', 'rank'], ascending=[False, True]).reset_index(drop=True)

    baseline_top5 = mc[mc['rank'] <= top_n]
    summary = {
        'n_sim': int(n_sim),
        'alpha': float(alpha),
        'seed': int(seed),
        'baseline_top5_min_p': float(baseline_top5['p_top5'].min()),
        'baseline_top5_all_robust': bool((baseline_top5['p_top5'] >= 0.80).all()),
        'n_combinations_ever_top5': int((mc['p_top5'] > 0).sum()),
    }
    return mc, summary


def run_factor_dropout(df=None, top_n=MC_TOP_N):
    """
    One-way robustness test: drop each factor to zero weight, renormalise the
    remaining weights, and check whether the baseline Top-N survives.

    This directly addresses the reviewer concern that the 25%-weighted Scarcity
    factor (S) rests partly on an UNVERIFIED distributor-channel review — the Gezat
    S002 review was conducted at catalogue/model level only, with no per-part search
    recorded. If the Top-N is unchanged when S is removed entirely, the
    recommendation does not hinge on that unverified input.

    Deterministic (no random draws).

    Returns (dropout_df, summary_dict).
    """
    if df is None or 'priority_score' not in df.columns:
        df = calculate_scores(df)

    base = WEIGHTS['Original']
    baseline_top5 = set(
        (df[df['rank'] <= top_n]['vehicle'] + ' — ' +
         df[df['rank'] <= top_n]['part_category']).tolist()
    )

    rows = []
    for dropped in FACTOR_COLUMNS:
        remaining = {k: v for k, v in base.items() if k != dropped}
        total = sum(remaining.values())
        temp = df.copy()
        temp['drop_score'] = sum((w / total) * temp[k] for k, w in remaining.items())
        top5 = (
            temp.sort_values(['drop_score', 'demand_evidence'], ascending=[False, False])
                .head(top_n)
                .apply(lambda r: f"{r['vehicle']} — {r['part_category']}", axis=1)
                .tolist()
        )
        overlap = len(baseline_top5.intersection(top5))
        rows.append({
            'dropped_factor': dropped,
            'top5': ' | '.join(top5),
            'overlap': overlap,
            'stability_pct': (overlap / float(top_n)) * 100.0,
        })

    dropout_df = pd.DataFrame(rows).set_index('dropped_factor')
    summary = {
        'top_n': int(top_n),
        'min_overlap': int(dropout_df['overlap'].min()),
        'scarcity_dropout_overlap': int(dropout_df.loc['market_scarcity', 'overlap']),
    }
    return dropout_df, summary


if __name__ == "__main__":
    df = calculate_scores()
    df.to_csv('data/scoring_results.csv', index=False)
    print(f"Generated {len(df)} defensible scoring rows.")
    print("\n=== TOP 10 RANKINGS ===")
    print(df[['rank', 'vehicle', 'part_category', 'priority_score']].head(10).to_string(index=False))

    sens_df, stability_summary = run_sensitivity_analysis(df)
    print("\n=== SENSITIVITY ROBUSTNESS TABLE ===")
    print(sens_df)
    print("\n=== STABILITY SUMMARY ===")
    for sc, info in stability_summary.items():
        print(f"  {sc:<20}: Overlap {info['overlap']}/5 | Stability {info['stability_pct']:.0f}%")

    mc_df, mc_summary = run_monte_carlo(df)
    mc_df.to_csv('data/sensitivity_monte_carlo.csv', index=False)
    print(f"\n=== MONTE-CARLO TOP-{MC_TOP_N} INCLUSION PROBABILITY "
          f"({mc_summary['n_sim']} Dirichlet draws, seed={mc_summary['seed']}) ===")
    print(mc_df.head(10)[['rank', 'vehicle', 'part_category',
                           'priority_score', 'p_top5', 'stability']].to_string(index=False))
    print(f"\n  Baseline Top-{MC_TOP_N} minimum inclusion probability: "
          f"{mc_summary['baseline_top5_min_p']:.1%}")
    print(f"  Combinations that ever entered the Top-{MC_TOP_N}: "
          f"{mc_summary['n_combinations_ever_top5']}/30")

    dropout_df, dropout_summary = run_factor_dropout(df)
    dropout_df.to_csv('data/sensitivity_factor_dropout.csv')
    print(f"\n=== ONE-WAY FACTOR DROPOUT ROBUSTNESS "
          f"(Top-{dropout_summary['top_n']} survival, deterministic) ===")
    print(dropout_df[['overlap', 'stability_pct']].to_string())
    print(f"\n  Minimum Top-{dropout_summary['top_n']} overlap when any single "
          f"factor is removed: {dropout_summary['min_overlap']}/{dropout_summary['top_n']}")
    print(f"  Top-{dropout_summary['top_n']} overlap when the Scarcity (S) factor is "
          f"removed entirely: {dropout_summary['scarcity_dropout_overlap']}/"
          f"{dropout_summary['top_n']}")
