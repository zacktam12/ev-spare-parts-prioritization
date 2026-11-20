# Landin Parts Final Data Quality & Reconciliation Audit

**Assignment**: iCog Labs EV Spare-Parts Import Prioritization (BYD Seagull)  
**Primary Source**: [Landin Parts BYD Catalog](https://www.landinparts.com/byd/)  
**Secondary Benchmark**: CQSW BYD Seagull OE Identification Article  
**Audit Date**: 2026-11-18  
**Scope**: Complete accounting of all raw extracted listings, cross-source conflict documentation, duplicate OE analysis, compatibility status verification, and full record reconciliation.

---

## 1. Executive Summary & Full Record Reconciliation

This final audit establishes a verifiable, auditable chain of custody from the raw catalog scrape down to verified priority parts. **No records have been deleted or overwritten.** The original raw baseline in [outputs/landin.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin.csv) remains 100% intact.

### Master Record Reconciliation Table

| Dataset / Classification Group | Record Count | Description & Status |
| :--- | :---: | :--- |
| **Total Original Raw Scraped Rows (`landin.csv`)** | **83** | **Baseline raw extraction preserved untouched** |
| ├── **Verified Distinct Part Applications (`landin_verified.csv`)** | **35** | Passed all conservative taxonomy and cross-source checks |
| └── **Reclassified from `landin.csv` to Review (`landin_review.csv`)** | **48** | Component hardware, conflicts, duplicate listings, and ambiguous items |
| &nbsp;&nbsp;&nbsp;&nbsp;├── *Cross-Source Conflicts (Bumper vs. Fender OE)* | *4* | Discrepancies between Landin and CQSW (2023 bumper models) |
| &nbsp;&nbsp;&nbsp;&nbsp;├── *Duplicate OE Supplier Listings (Shock/Pad Variants)* | *4* | Secondary listings sharing identical OE applications |
| &nbsp;&nbsp;&nbsp;&nbsp;├── *Ambiguous Wiper Component* | *1* | Wiper (`BYD0040831F1`) identity unconfirmed (blade vs arm assembly) |
| &nbsp;&nbsp;&nbsp;&nbsp;└── *Related Hardware & Sub-Assembly Components* | *39* | Brackets, reinforcement bars, hinges, inner splash shields, gas struts |
| **General Catalog Accessory & Component Listings** | **102** | Electrical, interior, suspension control arms, calipers, sensors, cooling |
| **Total Comprehensive Review Queue (`landin_review.csv`)** | **150** | **48 reclassified + 102 general catalog review items** |
| **Excluded Unrelated Components (Scraper Quality Gate)** | **12** | Logos, car letters, mud guards, wheel rims/hubs, side skirts |
| **Total BYD Seagull Catalog Universe** | **197** | **35 verified + 150 in review + 12 excluded = 197 total** |

*Reconciliation Check*: Exactly $35 + 48 = 83$ rows. Every single item from the original extraction is accounted for with zero loss.

---

## 2. Verified Row Count by Category & Compatibility Status

The 35 verified records are evaluated along two independent dimensions:
1. **Verified Spare-Part Category** (Taxonomic classification).
2. **Compatibility Status**:
   - `independently_supported`: Corroborated by independent automotive benchmarks (e.g., CQSW OE mapping).
   - `supplier_claimed`: Declared solely by Landin Parts catalog metadata without external corroboration.
   - `unresolved`: Conflicting cross-source claims requiring engineering clarification.

| Category | Verified Count | Independently Supported | Supplier Claimed | Populated Components |
| :--- | :---: | :---: | :---: | :--- |
| **Fenders / Body panels** | **16** | 4 | 12 | Front fenders (L/R), rear fenders (L/R), door panels (front/rear L/R), hood/bonnet, roof metal, rear body panel |
| **Bumpers** | **5** | 3 | 2 | Complete front bumper covers (`BYD0020040`, `BYD0040040U1`, `BYD0040040L6`) and rear bumper covers (`BYD0040190`, `BYD0020190`) |
| **Shock absorbers** | **3** | 0 | 3 | Front LH strut (`EQEA-2905100A`), Front RH strut (`EQEA-2905200A`), Rear damper (`EQEA-2915800A`) |
| **Tail lights** | **3** | 0 | 3 | Outer rear lamp assemblies (L/R), center tailgate light bar |
| **Headlights** | **2** | 0 | 2 | Left and right complete headlamp assemblies |
| **Side mirrors** | **2** | 0 | 2 | Left and right complete exterior rearview mirror assemblies |
| **Brake pads** | **2** | 0 | 2 | Front brake pad set (`EQEA-3501500CH`), Rear brake pad set (`EQEA-3502140SS`) |
| **Brake discs** | **2** | 0 | 2 | Front brake rotor disc (`EM2E-3501011`), Rear brake rotor disc (`EM2E-3502111`) |
| **Wiper blades** | **0** | 0 | 0 | *Wiper arm* classified as related; *Wiper* listing routed to review |
| **Cabin-air filters** | **0** | 0 | 0 | *Not found* for BYD Seagull in Landin catalog |
| **TOTAL VERIFIED** | **35** | **7** | **28** | **High-confidence core replacement parts** |

---

## 3. Detailed Cross-Source Discrepancies (Landin vs. CQSW)

Cross-referencing Landin product descriptions against the CQSW benchmark revealed **four critical conflicts** in the 2023 bumper catalog:

| Supplier SKU | Landin Product Name | Landin OE Number | CQSW Benchmark Identification | Conflict Details & Audit Action |
| :--- | :--- | :--- | :--- | :--- |
| `BYD0020042` | Front Bumper | `14549363-00` | **Front fender, right** | Landin names this a bumper, but CQSW identifies it as a right front fender. Marked `classification_status: needs_review`, `compatibility_status: unresolved`, moved to `landin_review.csv`. |
| `BYD0020041` | Front Bumper | `14549364-00` | **Front fender, left** | Landin names this a bumper, but CQSW identifies it as a left front fender. Marked `classification_status: needs_review`, `compatibility_status: unresolved`, moved to `landin_review.csv`. |
| `BYD0020191` | Rear Bumper | `14780089-00` | **Rear fender, left** | Landin names this a bumper, but CQSW identifies it as a left rear fender. Marked `classification_status: needs_review`, `compatibility_status: unresolved`, moved to `landin_review.csv`. |
| `BYD0020192` | Rear Bumper | `14780084-00` | **Rear fender, right** | Landin names this a bumper, but CQSW identifies it as a right rear fender. Marked `classification_status: needs_review`, `compatibility_status: unresolved`, moved to `landin_review.csv`. |

**Why this matters**: Classifying these 4 records as bumpers based solely on Landin's title would risk purchasing exterior steel fenders when plastic bumper fascias are required. Both sources are explicitly documented in `landin_review.csv`.

---

## 4. Repeated OE Numbers & Duplicate Supplier Listings

### 4.1 Bumper Production-Run Revisions (Preserved in Verified Dataset)
- **OE**: `EQEA-2804110A/00` (Rear Bumper)
  1. `BYD0040190`: Compatibility `SEAGULL 2020-`, Price: Price on request
  2. `BYD0020190`: Compatibility `SEAGULL 2023`, Price: ¥198 RMB
- **Audit Decision**: Both are preserved in `landin_verified.csv`. They represent distinct supplier SKUs manufactured across model-year revisions, maintaining distinct pricing and catalog numbers.

### 4.2 Duplicate Supplier Listings (Moved to Review Queue)
Four records represent alternative supplier listings or packaging variants mapping to identical OE applications:

| Component Application | Primary OE Number | Verified Base SKU | Duplicate Variant SKU | Audit Action & Field Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **Front LH Shock Absorber** | `EQEA-2905100A` | `BYD0042301F1` | `BYD0042301F1L5` | Variant SKU moved to review; reason: *"Duplicate supplier variant listing for same OE application (matches base SKU BYD0042301F1)"* |
| **Front RH Shock Absorber** | `EQEA-2905200A` | `BYD0042302F1` | `BYD0042302R2` | Variant SKU moved to review; reason: *"Duplicate supplier variant listing for same OE application (matches base SKU BYD0042302F1)"* |
| **Front Brake Pad Kit** | `EQEA-3501500CH` | `BYD0042260F1` | `BYD0042260F1P` | Variant SKU moved to review; reason: *"Duplicate supplier variant listing for same OE application (matches base SKU BYD0042260F1)"* |
| **Rear Brake Pad Kit** | `EQEA-3502140SS` | `BYD0042260R1` | `BYD0042260R1P` | Variant SKU moved to review; reason: *"Duplicate supplier variant listing for same OE application (matches base SKU BYD0042260R1)"* |

---

## 5. Wiper Listings Re-Examination

1. **Wiper Arm (`BYD0042591F1`, OE: `EQEA-5205120`)**:
   - Title: `Wiper armL`
   - Classification: `related_component` (mechanical metal pivot/linkage arm, not a wearable rubber blade).
2. **Ambiguous Wiper (`BYD0040831F1`, OE: `EQEA-5205110`)**:
   - Title: `Wiper`
   - Audit Finding: The catalog title does not indicate whether this is an individual wiper blade insert, a pair, or a combined arm/blade assembly.
   - Classification: `classification_status: needs_review`, `compatibility_status: unresolved`, moved to `landin_review.csv` pending physical product confirmation.

---

## 6. Itemized Accounting of the 48 Reclassified Records

All 48 records moved from `landin.csv` to `landin_review.csv` are accounted for below:

| Supplier SKU | Original Landin Product Name | OE Number | Reclassification Reason & Component Group |
| :--- | :--- | :--- | :--- |
| `BYD0040051` | Bracket,Front Bumper | `EQEA-2803311` | Bumper bracket (mounting hardware, not complete bumper) |
| `BYD0040052` | Bracket,Front Bumper | `EQEA-2803411` | Bumper bracket (mounting hardware, not complete bumper) |
| `BYD0040201L6` | Bracket,Rear Bumper | `EQEA-2804331` | Bumper bracket (mounting hardware, not complete bumper) |
| `BYD0040202L6` | Bracket,Rear Bumper | `EQEA-2804431` | Bumper bracket (mounting hardware, not complete bumper) |
| `BYD0040201F1` | Bracket,Rear Bumper | `EQEA-2804310` | Bumper bracket (mounting hardware, not complete bumper) |
| `BYD0040202F1` | Bracket,Rear Bumper | `EQEA-2804410` | Bumper bracket (mounting hardware, not complete bumper) |
| `BYD0020411` | Moulding,Rear bumper | `EQEA-2804114` | Bumper decorative trim moulding (not complete bumper) |
| `BYD0041520` | Tail Gate | `EQEA-6301010/70` | Tail gate liftgate closure panel (not bumper) |
| `BYD0021520` | Tail Gate | `14549368-00` | Tail gate liftgate closure panel (not bumper) |
| `BYD0040610F1` | Reinforcement Bars | `EQEA-8400010/70` | Structural crash impact beam (not exterior bumper) |
| `BYD0040610R1` | Reinforcement Bars | `EQEA-8400211/70` | Structural crash impact beam (not exterior bumper) |
| `BYD0020610` | Reinforcement Bars | `14549480-00` | Structural crash impact beam (not exterior bumper) |
| `BYD0040031F1` | Inner Fender | `EQEA-3102110A` | Inner wheel-arch splash shield (separated from exterior fenders) |
| `BYD0040032F1` | Inner Fender | `EQEA-3102120A` | Inner wheel-arch splash shield (separated from exterior fenders) |
| `BYD0040031R1` | Inner Fender | `EQEA-3102130A` | Inner wheel-arch splash shield (separated from exterior fenders) |
| `BYD0040032R1` | Inner Fender | `EQEA-3102140A` | Inner wheel-arch splash shield (separated from exterior fenders) |
| `BYD0041122` | Fender Bracket | `EQEA-5401142Q/70` | Fender mounting bracket (not body panel) |
| `BYD0041121U1` | Fender Bracket | `EQEA-5401141Q/70` | Fender mounting bracket (not body panel) |
| `BYD0041121L6` | Fender Bracket | `EQEA-5301677Q/70` | Fender mounting bracket (not body panel) |
| `BYD0041122L6` | Fender Bracket | `EQEA-5301678Q/70` | Fender mounting bracket (not body panel) |
| `BYD0041121D1` | Fender Bracket | `EQEA-5401137Q/70` | Fender mounting bracket (not body panel) |
| `BYD0041122D1` | Fender Bracket | `EQEA-5401138Q/70` | Fender mounting bracket (not body panel) |
| `BYD0040651` | Hood Hinge | `EQEA-8402610` | Hood articulation hinge (not body panel) |
| `BYD0040652` | Hood Hinge | `EQEA-8402619` | Hood articulation hinge (not body panel) |
| `BYD0020651F1` | Hood Hinge | `13608001-00` | Hood articulation hinge (not body panel) |
| `BYD0020652F1` | Hood Hinge | `13608002-00` | Hood articulation hinge (not body panel) |
| `BYD0040660F1` | Hood Latch Lock | `EQEA-8402530` | Hood latching mechanism (not body panel) |
| `BYD0042060F1` | Hood release cable | `EQEA-8402520` | Mechanical release cable (not body panel) |
| `BYD0040981` | Air Spring | `EQEA-6309111` | Pneumatic lift stay strut for tailgate/hood (not shock absorber) |
| `BYD0040982` | Air Spring | `EQEA-6309112` | Pneumatic lift stay strut for tailgate/hood (not shock absorber) |
| `BYD0042670` | Dust Cover, Shock Absorber | `HADF-2905421` | Protective boot accessory (not shock absorber) |
| `BYD0042680` | SHOCK ABSORBER BEARING ASSEMBLY | `HADF-2905600` | Upper strut mount bearing (not shock absorber) |
| `BYD0042690` | BUFFER BODY ASSY., DUST COVER | `EQEA-2915400` | Auxiliary rubber bump stop (not shock absorber) |
| `BYD0042231` | Tail Lamp Brackets | `EQEA-2804831` | Tail-lamp mounting bracket (not tail light) |
| `BYD0042232` | Tail Lamp Brackets | `EQEA-2804841` | Tail-lamp mounting bracket (not tail light) |
| `BYD0042231ST` | Tail Lamp Brackets | `EQEA-5401240/70` | Tail-lamp mounting bracket (not tail light) |
| `BYD0042232ST` | Tail Lamp Brackets | `EQEA-5401249/70` | Tail-lamp mounting bracket (not tail light) |
| `BYD0020130` | HeadLamp Lens | *(None)* | Polycarbonate lens cover shell (not complete headlight) |
| `BYD0042591F1` | Wiper arm | `EQEA-5205120` | Metal linkage arm (not replacement blade) |
| `BYD0040831F1` | Wiper | `EQEA-5205110` | Ambiguous listing; blade vs assembly unconfirmed |
| `BYD0020042` | Front Bumper | `14549363-00` | Cross-source conflict: CQSW identifies as right front fender |
| `BYD0020041` | Front Bumper | `14549364-00` | Cross-source conflict: CQSW identifies as left front fender |
| `BYD0020191` | Rear Bumper | `14780089-00` | Cross-source conflict: CQSW identifies as left rear fender |
| `BYD0020192` | Rear Bumper | `14780084-00` | Cross-source conflict: CQSW identifies as right rear fender |
| `BYD0042301F1L5` | Shock Absorber | `EQEA-2905100A  13505643-00` | Duplicate supplier listing for base SKU `BYD0042301F1` |
| `BYD0042302R2` | Shock Absorber | `EQEA-2905200A  13505757-00` | Duplicate supplier listing for base SKU `BYD0042302F1` |
| `BYD0042260F1P` | Brake Pads | `EQEA-3501500CH 14758996-00` | Duplicate supplier listing for base SKU `BYD0042260F1` |
| `BYD0042260R1P` | Brake Pads | `EQEA-3502140SS 14753311-00` | Duplicate supplier listing for base SKU `BYD0042260R1` |

---

## 7. Deliverable Status & Integrity Confirmation

- [outputs/landin.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin.csv): **Unmodified** (83 original raw rows).
- [outputs/landin_verified.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin_verified.csv): **35** verified distinct part applications with explicit `compatibility_status` (`independently_supported` vs `supplier_claimed`), separated price/stock fields, and parsed primary/secondary OE numbers.
- [outputs/landin_review.csv](file:///c:/Users/zeeje/Desktop/scrapper/outputs/landin_review.csv): **150** items preserved with specific `classification_reason`, `cross_source_conflict`, and `compatibility_status` tags.
