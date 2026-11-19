# Findings — Top 5 EV Spare Parts Import Recommendations

**Assignment**: EV Spare-Parts Import Prioritization (iCog Labs)  
**Target Market**: Ethiopia (Addis Ababa metropolitan & regional transport corridors)  
**Analysis Date**: 2026-11-19 (Audited and Defensible Baseline)  
**Dataset Reference**: [`data/cleaned/cleaned_observations.csv`](../data/cleaned/cleaned_observations.csv)  
**Scoring Output**: [`data/scoring_results.csv`](../data/scoring_results.csv)  

---

## 1. Unit of Analysis & Evidence Inventory Disclosure

### 1.1 Unit of Analysis
The scoring model evaluates **30 distinct Vehicle Model + Part Category combinations** ($3 \text{ vehicles} \times 10 \text{ part categories}$). 

The Top 5 recommendations represent the **highest-priority part categories**, accompanied by concrete **supplier-listed OE applications** for commercial procurement planning.

### 1.2 Evidence Classification
The raw evidence base consists of **59 observations** categorized across four distinct types in [`data/raw/raw_observations.csv`](../data/raw/raw_observations.csv):

| Observation Type | Row Count | Methodological Treatment |
| :--- | :---: | :--- |
| `supplier_catalogue` | **45** | Verified part listings in named supplier/parts catalogues (Landin S003 or third-party Toyota catalogue S005). These provide the basis for pricing and compatibility scoring. |
| `catalogue_gap` | **8** | Confirmed negative search findings in Landin Parts (S003). Valid empirical findings of catalogue absence; scored $C=1, P=1, E=1$. |
| `trade_quotation_unverified` | **4** | Price and fitment claims from an unnamed export directory (S008) for Yuan Up. Part numbers are trade codes, not confirmed OEM EPC numbers. Scored $C=2, P=1, E=1$ (cannot establish sourcing feasibility). |
| `safety_context` | **2** | NHTSA defect/recall records (S006). Documented strictly as engineering platform context; explicitly excluded from part compatibility and demand scoring. |

---

## 2. Priority Scoring Methodology

$$\text{Priority Score} = 0.30 \times D + 0.25 \times S + 0.20 \times C + 0.15 \times P + 0.10 \times E$$

All factors are rated on a **1 to 5 integer scale** based strictly on collected evidence:

| Factor | Weight | Operational Definition (Empirical Basis) | Important Methodological Qualification |
| :--- | :---: | :--- | :--- |
| **$D$ — Demand Evidence** | **30%** | Observed vehicle volume on Adey Market (S001) + component functional wear classification (friction wear vs collision repair vs structural). | **Analyst assessment**: Grounded in vehicle market density and component engineering wear type. No on-the-ground Ethiopian workshop replacement rates were measured. |
| **$S$ — Observed Public Catalogue Scarcity** | **25%** | Degree to which a part is absent from investigated public catalogues (Gezat S002, Landin S003, toyota-spare-parts S005). | **Public catalogue scarcity only**: Measures absence in investigated public catalogues. Does **not** establish physical unavailability in Addis Ababa shops. |
| **$C$ — Vehicle Compatibility** | **20%** | Verification level of supplier-listed OE reference in named catalogues. | 5 = Supplier-listed OE reference in named catalogue (Landin S003); 4 = third-party catalogue (S005); 2 = unverified trade code (S008); 1 = catalogue gap. |
| **$P$ — Catalogue Sourcing Practicality** | **15%** | Active listing status and unit catalogue price visibility in verified catalogues. | 5 = Verified catalogue price < $50 USD; 4 = $50–$250; 3 = >$250 or price on request; 1 = unverified trade quote (S008) or gap. No landed costs or freight quotes assumed. |
| **$E$ — Evidence Confidence** | **10%** | Degree of cross-validation across independent sources (S001–S008). | 5 = Named catalogue + CQSW benchmark cross-check; 4 = single named catalogue; 3 = third-party catalogue; 1 = unverified quotation (S008) or gap only. |

---

## 3. Top 5 Recommended Part Categories & Specific OE Applications

The Top 5 recommendations represent the highest-scoring part categories from the 30-combination matrix, all originating from the **BYD Seagull** platform. This directly reflects that Seagull is the only vehicle with 35 verified Landin listings with transparent pricing and supplier-listed OE references:

| Rank | Vehicle Model | Recommended Part Category | Priority Score | Supplier Catalogue Price | Supplier-Listed OE Reference(s) | Primary Sourcing Evidence |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **#1** | **BYD Seagull** | **Side mirror** | **4.75** | 429 RMB ($60.06 USD)<br>*(RH: 264 RMB / $36.96)* | `EQEA-8202100` (LH)<br>`EQEA-8202109` (RH) | Landin Parts (`S003`) active stock; corroborated by CQSW benchmark (`S004`). |
| **#2** | **BYD Seagull** | **Brake pads** | **4.45** | 64 RMB ($8.96 USD)<br>*(Rear: 64 RMB / $8.96)* | `EQEA-3501500CH` (Front)<br>`EQEA-3502140SS` (Rear) | Landin Parts (`S003`) active stock; corroborated by CQSW benchmark (`S004`). |
| **#3** | **BYD Seagull** | **Shock absorber** | **4.30** | 138 RMB ($19.32 USD)<br>*(RH: 138 RMB / $19.32)* | `EQEA-2905100A` (LH)<br>`EQEA-2905200A` (RH) | Landin Parts (`S003`) suspension catalogue; EQEA- prefix confirmed format. |
| **#4** | **BYD Seagull** | **Headlight assembly** | **4.30** | 418 RMB ($58.52 USD)<br>*(RH: 418 RMB / $58.52)* | `EQEA-4121010B` (LH)<br>`EQEA-4121020B` (RH) | Landin Parts (`S003`) lighting catalogue; corroborated by CQSW benchmark (`S004`). |
| **#5** | **BYD Seagull** | **Bumper** | **4.15** | 198 RMB ($27.72 USD) | `EQEA-2083111` (Front upper)<br>`EQEA-2804110A/00` (Rear) | Landin Parts (`S003`) body catalogue; rear bumper corroborated by CQSW (`S004`). |

*(Note on Other Candidates: Toyota bZ4X shock absorber ranks at **Rank #8 with a Score of 3.90** due to honest third-party catalogue labelling with $C=4, E=3$. Yuan Up parts rank lower due to Landin catalogue absence and unverified trade quotations).*

---

## 4. Per-Category Evidence & Procurement Justifications

### Rank #1 — BYD Seagull: Side Mirror (Priority Score: 4.75)
* **Demand ($D=5$)**: High vehicle presence on Adey Market (25+ active listings); exterior side mirrors represent primary contact-exposure components in congested Addis Ababa urban traffic corridors (analyst assessment).
* **Scarcity ($S=4$)**: Absent from investigated local distributor catalogue (Gezat S002); model-specific assembly.
* **Compatibility ($C=5$)**: Supplier-listed OE references `EQEA-8202100` (LH) and `EQEA-8202109` (RH) verified in Landin catalogue with explicit "SEAGULL 2020-" compatibility statement [OBS019, OBS020 / S003].
* **Practicality ($P=5$)**: Active catalogue listing with transparent unit pricing: 264–429 RMB ($36.96–$60.06 USD).
* **Confidence ($E=5$)**: Landin named supplier catalogue; EQEA- prefix format corroborated by CQSW benchmark [S003, S004].
* **Procurement Application**: Order both Left-Hand (`EQEA-8202100`) and Right-Hand (`EQEA-8202109`) assemblies as companion procurement SKUs.

### Rank #2 — BYD Seagull: Brake Pads (Priority Score: 4.45)
* **Demand ($D=4$)**: Routine friction wear consumable in stop-and-go city commuting.
* **Scarcity ($S=4$)**: EV-specific caliper compound absent from investigated local distributor catalogue (S002).
* **Compatibility ($C=5$)**: Supplier-listed OE references `EQEA-3501500CH` (Front) and `EQEA-3502140SS` (Rear) confirmed in Landin with "SEAGULL 2020-" compatibility [OBS024, OBS025 / S003].
* **Practicality ($P=5$)**: Active catalogue listing with transparent unit price: 64 RMB ($8.96 USD) per set (<$50 bracket).
* **Confidence ($E=5$)**: Landin catalogue listing; OE reference corroborated by CQSW benchmark [S003, S004].
* **Procurement Application**: Stock Front pad sets (`EQEA-3501500CH`) and Rear pad sets (`EQEA-3502140SS`) as companion consumable sets.

### Rank #3 — BYD Seagull: Shock Absorber (Priority Score: 4.30)
* **Demand ($D=4$)**: Suspension damping wear component under uneven urban road surfaces (analyst assessment).
* **Scarcity ($S=4$)**: Model-specific MacPherson strut geometry; absent from investigated local distributor catalogue (S002).
* **Compatibility ($C=5$)**: Supplier-listed OE references `EQEA-2905100A` (LH) and `EQEA-2905200A` (RH) confirmed in Landin [OBS021, OBS022 / S003].
* **Practicality ($P=4$)**: Active catalogue listing with transparent unit price: 138 RMB ($19.32 USD) per strut.
* **Confidence ($E=5$)**: Landin named catalogue; EQEA- prefix format corroborated by CQSW benchmark [S003, S004].
* **Procurement Application**: Stock Left-Hand (`EQEA-2905100A`) and Right-Hand (`EQEA-2905200A`) struts as paired suspension replacements.

### Rank #4 — BYD Seagull: Headlight Assembly (Priority Score: 4.30)
* **Demand ($D=4$)**: High Adey Market presence + frontal impact collision repair item.
* **Scarcity ($S=4$)**: Full LED projector assembly; absent from investigated local distributor catalogue (S002).
* **Compatibility ($C=5$)**: Supplier-listed OE references `EQEA-4121010B` (LH) and `EQEA-4121020B` (RH) confirmed in Landin with SEAGULL compatibility [OBS013, OBS014 / S003].
* **Practicality ($P=4$)**: Active catalogue listing with transparent unit price: 418 RMB ($58.52 USD) ($50–$250 bracket).
* **Confidence ($E=5$)**: Two distinct Landin SKUs (LH/RH); corroborated by CQSW benchmark [S003, S004].
* **Procurement Application**: Stock Left-Hand (`EQEA-4121010B`) and Right-Hand (`EQEA-4121020B`) units.

### Rank #5 — BYD Seagull: Bumper (Priority Score: 4.15)
* **Demand ($D=4$)**: Common frontal and rear collision repair shell.
* **Scarcity ($S=4$)**: Seagull-specific molded fascia; absent from investigated local distributor catalogue.
* **Compatibility ($C=5$)**: Supplier-listed OE references `EQEA-2083111` (Front upper) and `EQEA-2804110A/00` (Rear) confirmed in Landin [OBS001, OBS028 / S003].
* **Practicality ($P=3$)**: Front bumper listed at 198 RMB ($27.72 USD), but rear panel listed as Price on request in OBS004.
* **Confidence ($E=5$)**: Multiple verified Landin SKUs; rear bumper corroborated by CQSW benchmark [S003, S004].
* **Procurement Application**: Prioritize Front upper cover (`EQEA-2083111`) for initial container shipment.

---

## 5. Sensitivity Analysis & Robustness Verification

$$\text{Ranking Stability} = \frac{|\text{Top } 5_{\text{Baseline}} \cap \text{Top } 5_{\text{Scenario}}|}{5} \times 100\%$$

The priority ranking was evaluated under four contrasting business perspectives in `notebooks/04_analysis_and_scoring.ipynb`:

| Scenario | Weight Configuration (D / S / C / P / E) | Top 5 Members Identified | Stability Score |
| :--- | :--- | :--- | :---: |
| **Original (Baseline)** | 30% / 25% / 20% / 15% / 10% | Seagull Mirror (4.75), Pads (4.45), Shock (4.30), Headlight (4.30), Bumper (4.15) | **Baseline** |
| **Scarcity-First** | 25% / 30% / 20% / 15% / 10% | Seagull Mirror (4.70), Pads (4.45), Shock (4.30), Headlight (4.30), Bumper (4.15) | **100%** |
| **Equal-Weights** | 20% / 20% / 20% / 20% / 20% | Seagull Mirror (4.80), Pads (4.60), Shock (4.40), Headlight (4.40), Bumper (4.20) | **100%** |
| **Evidence-Focused** | 25% / 20% / 20% / 15% / 20% | Seagull Mirror (4.80), Pads (4.55), Shock (4.40), Headlight (4.40), Bumper (4.25) | **100%** |

### Stability Finding:
Across all four scenarios, the identical five vehicle-category combinations remain in the Top 5 (**100.0% set stability**). The Seagull side mirror is unconditionally Rank #1 (4.70–4.80) and brake pads are unconditionally Rank #2 (4.45–4.60).
