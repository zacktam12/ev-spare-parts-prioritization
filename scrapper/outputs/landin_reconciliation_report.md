# Landin Dataset Reconciliation & Validation Report

**Assignment**: iCog Labs EV Spare-Parts Import Prioritization (BYD Seagull)  
**Primary Dataset**: Landin Parts BYD Catalog ([landin.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin.csv))  
**Audited Datasets**: [landin_verified.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin_verified.csv) and [landin_review.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin_review.csv)  
**Cross-Source Benchmark**: CQSW BYD Seagull OE Identification Benchmark  
**Validation Date**: 2026-11-18  

---

## 1. Executive Summary & Chain of Custody

This report documents the final validation, semantic correction, and reconciliation of the Landin Parts spare-parts datasets. 

Key corrections executed in this final phase:
1. **Compatibility Semantics Correction**: `compatibility_status` was corrected across the verified dataset from `independently_supported` to `supplier_claimed`. While CQSW OE benchmarks corroborate *part identity and taxonomy*, they do not independently prove supplier-specific vehicle fitment or model-year interchangeability. Part identity evidence is retained under `cross_source_match`.
2. **Brake-Disc Cross-Source Matches**: Verified brake-disc records (`BYD0041960F1` and `BYD0041960R1`) were explicitly corroborated with their CQSW benchmark descriptions (`EM2E-3501011` $\rightarrow$ Front brake disc; `EM2E-3502111` $\rightarrow$ Rear brake disc), preserving secondary catalog OE numbers.
3. **Parking-Brake Naming Conflict Flagging**: In `landin_review.csv`, two listings titled "Right Parking Brake" (`BYD0042210F1` and `BYD0042210R1`) carry brake-disc OE numbers. They have been flagged with `cross_source_conflict` and set to `unresolved` without reclassifying them as confirmed brake discs. `BYD0042210` (OE: `TA-3502210B`) was excluded from this conflict.
4. **Primary OE Duplicate Audit**: Identified 10 repeated primary OE numbers across the datasets, distinguishing genuine production-run revisions from duplicate supplier listings and potential OE assignment conflicts.
5. **Zero Data Loss & File Isolation**: The original raw extraction [outputs/landin.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin.csv) was left unmodified. Previous versions of the verified and review files were preserved in `outputs/backup_prev/`.

---

## 2. Dataset Reconciliation & Record Counts

| Dataset | Row Count | Status & Scope |
| :--- | :---: | :--- |
| **Original Baseline Extraction (`landin.csv`)** | **83** | Untouched raw dataset |
| **Verified Part Applications (`landin_verified.csv`)** | **35** | High-confidence core replacement parts |
| **Comprehensive Review Queue (`landin_review.csv`)** | **150** | Ambiguous, related hardware, variants, and conflicts |
| &nbsp;&nbsp;├── *Reclassified from `landin.csv`* | *48* | 4 conflicts + 4 variants + 1 ambiguous wiper + 39 related |
| &nbsp;&nbsp;└── *Original Catalog Review Components* | *102* | Electrical, interior, control arms, calipers, sensors |
| **Excluded Unrelated Components** | **12** | Logos, car letters, mud guards, wheel rims/hubs, side skirts |
| **Total Catalog Universe (BYD Seagull)** | **197** | $35 + 150 + 12 = 197$ total catalog cards |

### Reconciliation Integrity Verification
- $\text{Verified (35)} + \text{Reclassified from 83 (48)} = 83 \text{ rows}$.
- **Overlap check**: $0$ part numbers appear in both `landin_verified.csv` and `landin_review.csv` ($\text{Intersection} = \emptyset$).
- **Completeness**: $100\%$ of the original 83 raw rows are accounted for.

---

## 3. Counts by Classification Status & Category

### 3.1 Verified Dataset Breakdown (`landin_verified.csv`, Total = 35)

| Category | Verified Count | Represented Components |
| :--- | :---: | :--- |
| **Fenders / Body panels** | **16** | Front fenders (L/R), rear fenders (L/R), door panels (front/rear L/R), hood/bonnet, roof metal, rear body panel |
| **Bumpers** | **5** | Complete front bumper covers (`BYD0020040`, `BYD0040040U1`, `BYD0040040L6`) and rear bumper covers (`BYD0040190`, `BYD0020190`) |
| **Shock absorbers** | **3** | Front LH strut (`EQEA-2905100A`), Front RH strut (`EQEA-2905200A`), Rear damper (`EQEA-2915800A`) |
| **Tail lights** | **3** | Outer rear lamp assemblies (L/R), center tailgate light bar |
| **Headlights** | **2** | Left and right complete headlamp assemblies |
| **Side mirrors** | **2** | Left and right exterior rearview mirror assemblies |
| **Brake pads** | **2** | Front brake pad set (`EQEA-3501500CH`), Rear brake pad set (`EQEA-3502140SS`) |
| **Brake discs** | **2** | Front brake rotor disc (`EM2E-3501011`), Rear brake rotor disc (`EM2E-3502111`) |
| **Wiper blades** | **0** | *Wiper arm* classified as related; *Wiper* listing routed to review |
| **Cabin-air filters** | **0** | *Not listed* for BYD Seagull in Landin catalog |
| **TOTAL VERIFIED** | **35** | **Classification Status: 35 `verified`** |

### 3.2 Review Dataset Breakdown (`landin_review.csv`, Total = 150)

| Classification Status | Count | Component Groups Included |
| :--- | :---: | :--- |
| **`related_component`** | **138** | Bumper brackets (6), bumper moulding (1), tailgates (2), reinforcement bars (3), inner fenders (4), fender brackets (6), hood hinges (4), hood latch/cable (2), air springs (2), shock absorber dust covers/bearings (3), tail-lamp brackets (4), headlamp lens (1), wiper arm (1), and general catalog accessories/hardware (99) |
| **`needs_review`** | **12** | 4 Bumper/Fender cross-source conflicts, 2 Parking brake naming conflicts, 1 Vibration damper OE conflict, 4 Duplicate OE supplier variants, 1 Ambiguous wiper |
| **TOTAL REVIEW** | **150** | **All non-core or ambiguous records preserved** |

---

## 4. Cross-Source Matches & Conflicts

### 4.1 Corroborated Cross-Source Matches (Part Identity Supported)

The following records have verified part identities corroborated by the CQSW benchmark:

| Supplier SKU | Dataset | Product Name | Primary OE | Secondary OE | Corroborated CQSW Identity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `BYD0040040L6` | Verified | Front Bumper | `EQEA-2803112` | *(None)* | Front bumper, lower |
| `BYD0040190` | Verified | Rear Bumper | `EQEA-2804110A/00` | *(None)* | Rear bumper |
| `BYD0020190` | Verified | Rear Bumper | `EQEA-2804110A/00` | *(None)* | Rear bumper |
| `BYD0040022` | Verified | Fender，Front | `EQEA-8403019/70` | *(None)* | Front fender, right |
| `BYD0040021` | Verified | Fender，Front | `EQEA-8403010/70` | *(None)* | Front fender, left |
| `BYD0040181` | Verified | Rear Fender | `EQEA-5401917/70` | *(None)* | Rear fender, left |
| `BYD0040182` | Verified | Rear Fender | `EQEA-5401918/70` | *(None)* | Rear fender, right |
| `BYD0041960F1` | Verified | Brake Disc | `EM2E-3501011` | `13423467-00` | Front brake disc (CQSW source) |
| `BYD0041960R1` | Verified | Brake Disc | `EM2E-3502111` | `13423445-00` | Rear brake disc (CQSW source) |

### 4.2 Cross-Source Conflicts (7 Records in Review)

All 7 records with conflicting external evidence are preserved in `landin_review.csv` with `compatibility_status: unresolved`:

| Supplier SKU | Landin Product Name | Primary OE | CQSW Benchmark Identification | Conflict Details & Reason |
| :--- | :--- | :--- | :--- | :--- |
| `BYD0020042` | Front Bumper | `14549363-00` | **Front fender, right** | Landin lists as 'Front Bumper', but CQSW identifies OE as right front fender. |
| `BYD0020041` | Front Bumper | `14549364-00` | **Front fender, left** | Landin lists as 'Front Bumper', but CQSW identifies OE as left front fender. |
| `BYD0020191` | Rear Bumper | `14780089-00` | **Rear fender, left** | Landin lists as 'Rear Bumper', but CQSW identifies OE as left rear fender. |
| `BYD0020192` | Rear Bumper | `14780084-00` | **Rear fender, right** | Landin lists as 'Rear Bumper', but CQSW identifies OE as right rear fender. |
| `BYD0042210F1` | Right Parking Brake | `EM2E-3501011` | **Front brake disc** | Landin lists as 'Right Parking Brake', but OE maps to front brake disc. Requires supplier confirmation; not reclassified as disc. |
| `BYD0042210R1` | Right Parking Brake | `EM2E-3502111` | **Rear brake disc** | Landin lists as 'Right Parking Brake', but OE maps to rear brake disc. Requires supplier confirmation; not reclassified as disc. |
| `BYD0021282F1` | VIBRATION DAMPER | `EQEA-2905200A` | **Front RH Shock Absorber** | Shares primary OE with suspension shock absorber `BYD0042302F1`, but listed as 'VIBRATION DAMPER' for SEAGULL 2023. |

*Note on `BYD0042210`*: Carries OE `TA-3502210B`. Because this OE does not conflict with CQSW brake-disc numbers, it remains classified as a standard review queue component without conflict flags.

---

## 5. Duplicate OE Audit & Supplier Variants

Checking across both datasets revealed **10 repeated primary OE numbers**:

| Primary OE Number | Count | Datasets & SKUs Involved | Nature of Duplication & Audit Resolution |
| :--- | :---: | :--- | :--- |
| **`EQEA-2804110A/00`** | 2 | `[verified] BYD0040190` (SEAGULL 2020-)<br>`[verified] BYD0020190` (SEAGULL 2023) | **Production-Run Revision**: Same OE bumper cover across model-year revisions. Both preserved in verified dataset. |
| **`EQEA-2905100A`** | 2 | `[verified] BYD0042301F1`<br>`[review] BYD0042301F1L5` | **Supplier Variant**: Identical front LH shock absorber application. Base SKU verified; variant listing routed to review. |
| **`EQEA-2905200A`** | 3 | `[verified] BYD0042302F1` (Shock Absorber)<br>`[review] BYD0042302R2` (Shock Absorber)<br>`[review] BYD0021282F1` (Vibration Damper) | **Mixed Application / Variant**: Base shock absorber verified; variant `BYD0042302R2` and damper `BYD0021282F1` routed to review. |
| **`EQEA-3501500CH`** | 2 | `[verified] BYD0042260F1`<br>`[review] BYD0042260F1P` | **Supplier Variant**: Identical front brake pad kit application. Base SKU verified; variant listing routed to review. |
| **`EQEA-3502140SS`** | 2 | `[verified] BYD0042260R1`<br>`[review] BYD0042260R1P` | **Supplier Variant**: Identical rear brake pad kit application. Base SKU verified; variant listing routed to review. |
| **`EM2E-3501011`** | 2 | `[verified] BYD0041960F1` (Brake Disc)<br>`[review] BYD0042210F1` (Right Parking Brake) | **Cross-Component OE Overlap**: Front brake disc vs parking brake listing. Brake disc verified; parking brake flagged in review. |
| **`EM2E-3502111`** | 2 | `[verified] BYD0041960R1` (Brake Disc)<br>`[review] BYD0042210R1` (Right Parking Brake) | **Cross-Component OE Overlap**: Rear brake disc vs parking brake listing. Brake disc verified; parking brake flagged in review. |
| **`F3-2904140`** | 2 | `[review] BYD0041440` (Ball Joint)<br>`[review] BYD0041440D1` (Ball Joint) | **Review Queue Variants**: Ball joint hardware variants preserved in review. |
| **`EQEA-2904010`** | 2 | `[review] BYD0041311` (Control Arm LH)<br>`[review] BYD0041311F1L5` (Control Arm LH) | **Review Queue Variants**: Suspension control arm variants preserved in review. |
| **`EQEA-2904020`** | 2 | `[review] BYD0041312` (Control Arm RH)<br>`[review] BYD0041312R2F1` (Control Arm RH) | **Review Queue Variants**: Suspension control arm variants preserved in review. |

---

## 6. Compatibility & Category Completeness Analysis

### 6.1 Compatibility Status Distribution
- **Verified Dataset (35 records)**:
  - `supplier_claimed`: **35 records (100%)**. An OE description match supports part identity and category, not vehicle fitment; fitment remains based on supplier catalog claims.
- **Review Dataset (150 records)**:
  - `supplier_claimed`: **142 records (94.7%)**.
  - `unresolved`: **8 records (5.3%)** (4 bumper/fender conflicts, 2 parking brake conflicts, 1 damper conflict, 1 ambiguous wiper).

### 6.2 Missing Assigned Categories
Of the 10 target EV spare-part categories:
1. **Wiper blades**: 0 confirmed in verified dataset. `BYD0042591F1` is a wiper linkage arm (`related_component`); `BYD0040831F1` (`Wiper`) is ambiguous and preserved in review.
2. **Cabin-air filters**: 0 confirmed in verified dataset. No cabin-air filter listings exist for BYD Seagull on Landin Parts (all catalog air filters belong to BYD Destroyer).

---

## 7. Records Requiring Supplier Confirmation

The following 8 records require direct confirmation from Landin Parts or physical inspection before procurement:

1. **`BYD0020042` & `BYD0020041`**: Confirm whether these 2023 listings are front bumper fascias or front steel fenders (OE: `14549363-00` / `14549364-00`).
2. **`BYD0020191` & `BYD0020192`**: Confirm whether these 2023 listings are rear bumper covers or rear fenders (OE: `14780089-00` / `14780084-00`).
3. **`BYD0042210F1` & `BYD0042210R1`**: Clarify why parts named "Right Parking Brake" carry brake-disc OE numbers (`EM2E-3501011` / `EM2E-3502111`).
4. **`BYD0021282F1`**: Clarify why a "VIBRATION DAMPER" shares OE `EQEA-2905200A` with front right shock absorber `BYD0042302F1`.
5. **`BYD0040831F1`**: Confirm whether "Wiper" represents a wearable rubber blade refill, a blade set, or a combined arm/blade assembly.

---

## 8. Final Compliance & Quality Checklist

- [x] **No Part Number Overlap**: 0 SKUs shared between verified (35) and review (150).
- [x] **Zero Data Loss**: All 83 rows from the raw scrape and all 102 initial review rows are fully accounted for ($35 + 150 = 185$ total across verified and review).
- [x] **Currency Uniformity**: 100% of priced items remain in RMB (`¥... RMB`).
- [x] **Stock Status Veracity**: 100% of records remain `stock_status_verified: "Not stated"` (no stock inferred from price).
- [x] **Collection Date Preserved**: 100% of records retain their actual collection date (`2026-11-18`).
- [x] **Raw Baseline Protected**: [outputs/landin.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin.csv) remains unmodified.
- [x] **Backup Preserved**: Prior states archived in `outputs/backup_prev/`.
