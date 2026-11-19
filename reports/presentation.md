# 7-Minute Presentation Deck: EV Spare-Parts Import Prioritization

**Candidate**: Data & AI Engineering Intern Candidate  
**Assessment**: iCog Labs EV Spare-Parts Prioritization Technical Assignment  
**Target Market**: Addis Ababa, Ethiopia  
**Presentation Time**: 7 Minutes (Strict Aligned Timing)  
**Deliverables**:
- Editable Slide Deck: [`reports/EV_Spare_Parts_Prioritization_Presentation.pptx`](file:///c:/Users/zeeje/Desktop/ev-spare-parts-prioritization/reports/EV_Spare_Parts_Prioritization_Presentation.pptx)
- Generated Figures: [`reports/figures/`](file:///c:/Users/zeeje/Desktop/ev-spare-parts-prioritization/reports/figures)
- Master Technical Report: [`reports/comprehensive_project_report.md`](file:///c:/Users/zeeje/Desktop/ev-spare-parts-prioritization/reports/comprehensive_project_report.md)
- Analytical Notebooks: [`notebooks/01_vehicle_selection.ipynb`](file:///c:/Users/zeeje/Desktop/ev-spare-parts-prioritization/notebooks/01_vehicle_selection.ipynb) to [`04_analysis_and_scoring.ipynb`](file:///c:/Users/zeeje/Desktop/ev-spare-parts-prioritization/notebooks/04_analysis_and_scoring.ipynb)

---

## Presentation Structure & Timing Guide

| Slide | Topic | Visual Asset | Target Duration | Running Time |
| :---: | :--- | :--- | :---: | :---: |
| **1** | Title & Context | Cover slide | 30s | 0:00 – 0:30 |
| **2** | The Ethiopian Dilemma | Policy & Forex context | 45s | 0:30 – 1:15 |
| **3** | Vehicle Selection Matrix | 5 candidate comparison table | 45s | 1:15 – 2:00 |
| **4** | Evidence Architecture | 4 observation types (45/8/4/2) across 8 sources | 45s | 2:00 – 2:45 |
| **5** | Data Cleaning & Missing Values | Pipeline flow & rules | 30s | 2:45 – 3:15 |
| **6** | Multi-Factor Scoring Model | Formula & 5 factor weights | 45s | 3:15 – 4:00 |
| **7** | Matrix Heatmap & Patterns | `scoring_matrix_heatmap.png` | 45s | 4:00 – 4:45 |
| **8** | Top 5 Defensible Recommendations | Prioritized categories with OE applications | 60s | 4:45 – 5:45 |
| **9** | Sensitivity & Robustness | `sensitivity_comparison.png` | 45s | 5:45 – 6:30 |
| **10** | Strategic Logistics Roadmap | Air vs Ocean two-tier flow | 30s | 6:30 – 7:00 |
| **11** | Boundaries & Defense Q&A | Honest limitations & FAQ | Q&A Period | Post 7:00 |

---

## Slide 1: Title & Introduction (0:00 – 0:30)

### Slide Content:
- **Title**: DATA-DRIVEN EV SPARE-PARTS IMPORT PRIORITIZATION
- **Subtitle**: Strategic Multi-Factor Decision Framework for the Ethiopian EV Market
- **Scope**: 3 Vehicles × 10 Spare Part Categories = 30 Evaluated Combinations
- **Presenter**: Data & AI Engineering Candidate | iCog Labs Assessment | November 2026

### Speaker Notes (Spoken Word):
> *"Good morning, evaluators. Today I am presenting an end-to-end data-driven decision framework designed to solve a critical commercial dilemma in Ethiopia: identifying exactly which replacement parts an automotive importer should prioritize under constrained working capital and strict foreign exchange rationing.
>
> Rather than relying on unverified assumptions, our system integrates live marketplace evidence, third-party catalogues, and verified supplier inventories into an explainable, 100% robust scoring framework."*

---

## Slide 2: The Ethiopian EV Dilemma (0:30 – 1:15)

### Slide Content:
- **Policy Catalyst**: Federal prohibition on non-electric private passenger vehicle imports (early 2024) triggered an immediate surge in EV imports into Addis Ababa.
- **The Working Capital Bottleneck**: Importers cannot stock every component across every vehicle. A broad catalogue ties up scarce cash in slow-moving inventory.
- **Foreign Exchange Rationing**: Strict allocation of letters of credit (LC) and ETB/USD access demands that every dollar imported turns quickly.
- **Operating Environment**: Congested urban corridors create high exterior mirror and bumper scrapes; rough peri-urban road surfaces accelerate damper fatigue.

### Speaker Notes:
> *"The problem space is unique to Ethiopia. With the government's ban on ICE imports, electric vehicles now dominate new car arrivals. But spare parts supply has severely lagged behind.
>
> An importer faces two risks: stocking parts that sit on shelves for months, or stocking parts with unverified fitment that damage customer trust. Because foreign exchange is rationed, inventory decisions must be mathematically defensible and grounded in verified data."*

---

## Slide 3: Vehicle Selection Matrix (1:15 – 2:00)

### Slide Content:
| Vehicle Model | Category | Adey Market Evidence | Decision | Core Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **BYD Seagull** | Subcompact Hatchback | 25+ listings | **SELECTED** | Leading urban commuter; high traffic exposure; active supplier catalogue (35 verified listings in Landin S003). |
| **BYD Yuan Up** | Compact SUV / CUV | 1,360+ listings | **SELECTED** | Dominant mass-market family crossover; crucial test case for supplier catalogue gap analysis. |
| **Toyota bZ4X** | Midsize Electric SUV | 50+ listings | **SELECTED** | High brand equity; corporate fleet presence; verified via third-party parts catalogue (`toyota-spare-parts.com` S005). |
| **VW ID.4** | Compact Crossover | 12 listings | **EXCLUDED** | Grey-market imports; fragmented EU vs China software and hardware variants. |
| **Tesla Model 3/Y** | Premium Sedan / SUV | 5 listings | **EXCLUDED** | Niche luxury segment; closed repair ecosystem; low volume. |

### Speaker Notes:
> *"We evaluated five candidate models against market data from Adey Market and Gezat Electric. We selected three archetypes: the BYD Seagull for entry-level mass commuting, the BYD Yuan Up for high-volume family crossover demand, and the Toyota bZ4X representing trusted global brand equity."*

---

## Slide 4: Evidence Architecture & Sourcing (2:00 – 2:45)

### Slide Content:
- **59 Total Observations** classified into four distinct types across 8 sources (`data/source_log.csv`):
  - **45 Supplier Catalogue Listings (`S003` & `S005`)**: 35 verified Landin listings for Seagull; 10 Toyota bZ4X items in third-party catalogue (`toyota-spare-parts.com`).
  - **8 Documented Catalogue Gaps (`S003`)**: Confirmed negative search findings in Landin Parts (e.g. Seagull filter/wiper, and complete lack of Yuan Up listings).
  - **4 Unverified Trade Quotations (`S008`)**: Unnamed overseas export directory quotes for Yuan Up. Part numbers are trade listing codes, not confirmed OEM EPC numbers. Scored conservatively ($P=1, E=1$).
  - **2 Safety Context Records (`S006`)**: NHTSA defect datasets (Campaign 22V444 hub bolt recall; brake shudder). Documented strictly as engineering platform context; decoupled from part demand/fitment.

### Speaker Notes:
> *"Our evidence architecture comprises 59 observations across four distinct types. We enforce research honesty: only 45 rows are verified supplier catalogue listings.
>
> Crucially, we do not hallucinate parts for the Yuan Up: Landin's zero coverage is documented as an empirical catalogue gap, and trade quotes are isolated under S008. Furthermore, Toyota's source is explicitly identified as a third-party catalogue, not official Toyota EPC."*

---

## Slide 5: Data Cleaning & Integrity (2:45 – 3:15)

### Slide Content:
- **Taxonomy Standardization**: Harmonized irregular scraped categories (e.g. `Bumpers` → `Bumper`).
- **Currency Normalization**: Standardized all RMB and ETB quotes to USD at fixed benchmark rates (`1 RMB = 0.14 USD`, `1 ETB = 0.008 USD`) while preserving original currencies for auditability.
- **Missing Value Preservation**: Preserved 22 unpriced body panels and catalogue gaps with `price_missing = True`. Never zero-filled or guessed catalogue prices.
- **NHTSA Isolation**: Excluded `safety_context` records from part cross-check counts so US recall records do not falsely inflate compatibility confidence.
- **Reproducibility Verification**: Cleaned CSV loads cleanly with pandas (0 tokenizing errors; fully quoted fields).

### Speaker Notes:
> *"In data cleaning, transparency and reproducibility were paramount. We normalized currencies to USD, harmonized taxonomy across all 30 matrix combinations, and preserved unpriced body panels as missing rather than substituting artificial numbers. Cleaned datasets load with zero errors."*

---

## Slide 6: Multi-Factor Priority Scoring Model (3:15 – 4:00)

### Slide Content:
$$\text{Priority Score} = 0.30 \times D + 0.25 \times S + 0.20 \times C + 0.15 \times P + 0.10 \times E$$

| Factor | Weight | Operational Definition (Empirical Basis) | Scale (1–5) |
| :--- | :---: | :--- | :---: |
| **Demand Evidence ($D$)** | **30%** | Vehicle market presence (Adey listings) + functional wear classification (friction wear vs collision repair). | 1 = Rare model, 5 = Top volume & wear |
| **Observed Public Catalogue Scarcity ($S$)** | **25%** | Absence in investigated public online catalogues (Gezat S002 local distributor, Landin S003 overseas supplier, toyota-spare-parts S005). | 1 = In distributor, 5 = Confirmed catalogue gap |
| **Vehicle Compatibility ($C$)** | **20%** | Verification level: supplier-listed OE reference in named catalogue with model compatibility statement. | 1 = Gap, 5 = Confirmed OE in named catalogue |
| **Catalogue Sourcing Practicality ($P$)** | **15%** | Active verified catalogue listing status and unit price visibility (no speculative landed cost claims). | 1 = Unverified quote/gap, 5 = Verified price < $50 |
| **Evidence Confidence ($E$)** | **10%** | Number and independence of corroborating sources (Landin, CQSW benchmark, third-party catalogue). | 1 = Unverified quote/gap, 5 = Named catalogue + cross-check |

### Speaker Notes:
> *"Our scoring framework directly satisfies the assessment rubric. Demand is weighted at 30%, reflecting market volume and wear type. Observed Public Catalogue Scarcity is weighted at 25%, distinguishing local distributor absence from overseas supplier availability. Vehicle Compatibility is 20%, verifying supplier OE references.
>
> Catalogue Sourcing Practicality is 15%, evaluating verified catalogue pricing brackets without speculative shipping assumptions. Evidence Confidence is 10%, rewarding multi-source corroboration. Every factor is scored on a clear 1 to 5 scale."*

---

## Slide 7: Prioritization Heatmap & Patterns (4:00 – 4:45)

### Slide Content:
*(Displays `reports/figures/scoring_matrix_heatmap.png`)*

- **Seagull Average (4.09)**: Leads the overall ranking due to complete supplier catalog coverage and active commercial pricing.
- **Toyota bZ4X Average (3.65)**: Sourced via third-party catalogue; honest labelling ($C=4, E=3$) places bZ4X shock absorber at Rank 8 (Score 3.90).
- **Yuan Up Average (2.89)**: High demand (5/5), but penalized by upstream catalogue absence on Landin and unverified trade quotes ($P=1, E=1$).
- **Dominant Categories**: Side mirrors, brake pads, shock absorbers, headlights, and bumpers lead across all vehicles.

### Speaker Notes:
> *"Looking at the 30-combination heatmap, clear operational patterns emerge. The BYD Seagull captures the highest scores because active supplier pricing and supplier-listed OE references confirm immediate sourcing feasibility.
>
> Toyota bZ4X ranks realistically at 3.90 due to third-party catalogue labelling. Yuan Up exhibits tremendous market demand, but its low sourcing scores reflect current catalogue absence."*

---

## Slide 8: Top 5 Defensible Recommendations (4:45 – 5:45)

### Slide Content:
| Rank | Vehicle Model | Part Category & Defined Application | Priority Score | Catalogue Price | Supplier-Listed OE Reference | Primary Sourcing Reference |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **#1** | **BYD Seagull** | **Side mirror**<br>*(LH mirror assembly; companion RH)* | **4.75** | 429 RMB ($60.06 USD)<br>*(RH: 264 RMB / $36.96)* | `EQEA-8202100` (LH)<br>`EQEA-8202109` (RH) | Landin Parts (`S003`) active stock |
| **#2** | **BYD Seagull** | **Brake pads**<br>*(Front pad set; companion Rear)* | **4.45** | 64 RMB ($8.96 USD)<br>*(Rear: 64 RMB / $8.96)* | `EQEA-3501500CH` (Front)<br>`EQEA-3502140SS` (Rear) | Landin Parts (`S003`) / CQSW benchmark |
| **#3** | **BYD Seagull** | **Shock absorber**<br>*(Front strut LH; companion RH)* | **4.30** | 138 RMB ($19.32 USD)<br>*(RH: 138 RMB / $19.32)* | `EQEA-2905100A` (LH)<br>`EQEA-2905200A` (RH) | Landin Parts (`S003`) suspension catalogue |
| **#4** | **BYD Seagull** | **Headlight assembly**<br>*(LH headlight; companion RH)* | **4.30** | 418 RMB ($58.52 USD)<br>*(RH: 418 RMB / $58.52)* | `EQEA-4121010B` (LH)<br>`EQEA-4121020B` (RH) | Landin Parts (`S003`) lighting catalogue |
| **#5** | **BYD Seagull** | **Bumper**<br>*(Front bumper cover upper fascia)* | **4.15** | 198 RMB ($27.72 USD) | `EQEA-2083111` | Landin Parts (`S003`) body catalogue |

> *Note on Application Definition*: The scoring model evaluates 30 vehicle-model + part-category combinations. The top 5 recommendations represent prioritized categories accompanied by concrete supplier-listed OE applications for commercial implementation.

### Speaker Notes:
> *"Here is our Top 5 recommendation list. Our top 5 recommendations represent prioritized part categories for the BYD Seagull, supported by specific supplier-listed OE applications and transparent catalogue prices.
>
> Rank 1 is the BYD Seagull side mirror at 4.75 (exemplar LH mirror at $60.06; companion RH at $36.96). Rank 2 is brake pads at 4.45 and $8.96 USD. Ranks 3 and 4 are shock absorbers and headlights at 4.30. Rank 5 is bumper at 4.15.
>
> All five top recommendations are BYD Seagull parts, directly reflecting that Seagull is the only vehicle with 35 verified Landin listings. Toyota bZ4X shock absorber is at Rank 8 (3.90) due to honest third-party source labelling."*

---

## Slide 9: Sensitivity Analysis & Robustness (5:45 – 6:30)

### Slide Content:
*(Displays `reports/figures/sensitivity_comparison.png`)*

$$\text{Ranking Stability} = \frac{|\text{Top } 5_{\text{Baseline}} \cap \text{Top } 5_{\text{Scenario}}|}{5} \times 100\%$$

| Scenario | Weight Configuration (D, S, C, P, E) | Top 5 Composition | Stability |
| :--- | :--- | :--- | :---: |
| **1. Original Baseline** | 30% / 25% / 20% / 15% / 10% | Seagull Mirror, Pads, Strut, Headlight, Bumper | **100.0%** |
| **2. Scarcity-First** | 25% / 30% / 20% / 15% / 10% | Seagull Mirror, Pads, Strut, Headlight, Bumper | **100.0%** |
| **3. Equal-Weights** | 20% / 20% / 20% / 20% / 20% | Seagull Mirror, Pads, Strut, Headlight, Bumper | **100.0%** |
| **4. Evidence-Focused** | 25% / 20% / 20% / 15% / 20% | Seagull Mirror, Pads, Strut, Headlight, Bumper | **100.0%** |

### Speaker Notes:
> *"To ensure this recommendation is not an artifact of our weight choices, we conducted a sensitivity analysis across four contrasting business scenarios in notebook 04.
>
> The result is 100.0% stability. The exact same five categories populate the top 5 across all scenarios. Even under equal weighting, the Seagull mirror remains rank 1 and brake pads rank 2. This invariance confirms robust top-5 set stability across all tested weighting scenarios."*

---

## Slide 10: Strategic Logistics Roadmap (6:30 – 7:00)

### Slide Content:
- **Phase 1: Air Cargo Fast-Turn (High-Exposure Wear)**
  - *Target Categories*: BYD Seagull Side Mirrors & Brake Pad Sets.
  - *Route*: Shenzhen/Guangzhou → Bole International Airport, Addis Ababa.
  - *Commercial Rationale*: Compact volumetric size; rapid turnaround to address urgent vehicle downtime for high-exposure collision and wear parts.
  - *Capital Exposure*: Low unit capital outlay ($8.96 pads, $36.96–$60.06 mirrors), mitigating initial foreign exchange exposure.
- **Phase 2: Ocean Freight Heavy-Stock (Consolidated)**
  - *Target Categories*: BYD Seagull Suspension Struts, Headlight Assemblies, & Bumper Covers.
  - *Route*: China → Port of Djibouti → Modjo Dry Port, Ethiopia.
  - *Commercial Rationale*: Heavy suspension dampers and bulky bumper covers require ocean freight consolidation to manage dimensional shipping costs effectively.
  - *Order Timing*: Scheduled as planned inventory replenishment following initial market validation.

### Speaker Notes:
> *"Finally, we translate these analytical findings into an executable procurement roadmap. We recommend a two-tier strategy:
>
> Tier 1 uses air cargo for compact, high-turnover wear items to minimize customer vehicle downtime and test market demand. Tier 2 leverages ocean freight via Djibouti and Modjo Dry Port for heavier suspension dampers and bulky body panels to optimize freight efficiency."*

---

## Slide 11: Methodological Limitations & Defense Q&A (Post 7:00)

### Honest Data Boundaries:
1. **Absence of Brick-and-Mortar Survey**: Scarcity scores reflect investigated online catalogue absence; physical spare-part shops in Addis were not surveyed.
2. **Marketplace Listings ≠ Total Fleet**: Adey Market listings represent active seller listings, not cumulative licensed vehicle registrations.
3. **NHTSA Datasets Are Geographic Boundaries**: Recall campaigns reflect US market data; utilized strictly as platform stress context rather than direct local failure rates.
4. **Catalogue Gaps**: Documented Landin's lack of Yuan Up listings honestly rather than inventing data.

### Evaluator Defense Cheatsheet:
- **Q1: Why does Seagull rank higher than Yuan Up when Yuan Up has 1,360+ marketplace listings?**  
  *Response*: "While Yuan Up has immense market presence on Adey Market (earning 5/5 in Demand), investigated supplier catalogues (Landin S003) had zero public listings for Yuan Up. Seagull had 35 verified listings with exact prices and supplier-listed OE references, yielding far higher Catalogue Sourcing Practicality (P) and Evidence Confidence (E). Importing parts without verified catalogue listings creates severe fitment and capital risk."
- **Q2: Why did Toyota bZ4X shock absorber drop to Rank 8?**  
  *Response*: "Because toyota-spare-parts.com is a third-party aggregator catalogue, not official Toyota EPC. Labeling it honestly lowered Compatibility from 5 to 4 and Confidence from 5 to 3, yielding an honest score of 3.90."
- **Q3: How do you explain the Top 5 being all BYD Seagull?**  
  *Response*: "This is an evidence-driven finding. Seagull is the only vehicle with an active, transparent commercial catalogue (Landin S003) covering 8 categories with confirmed prices and supplier-listed OE references. It represents the lowest-risk entry point for a new importer."
