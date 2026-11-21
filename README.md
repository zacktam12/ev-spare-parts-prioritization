# EV Spare-Parts Import Prioritization

A data-driven recommendation system that identifies which electric vehicle (EV) replacement parts a new automotive importer should prioritize for the Ethiopian market under constrained working capital and strict foreign exchange rationing.

## Business Context

Following Ethiopia's 2024 ban on internal combustion engine (ICE) passenger car imports, electric vehicles surged in Addis Ababa. However, the local spare-parts supply chain is severely bottlenecked. An importer cannot stock every component across every vehicle model.

This project delivers an end-to-end, reproducible decision framework by:
1. Selecting three representative EV models from live Ethiopian marketplace evidence
2. Investigating 10 spare-part categories across those vehicles (a complete $3 \times 10 = 30$ combination matrix)
3. Compiling an auditable evidence dataset of 59 empirical observations classified across 8 reliability-tiered sources (tiers `A`/`B`/`C`, each with a recorded URL)
4. Cleaning and standardizing the dataset, preserving missing values and normalizing currencies to USD
5. Evaluating all 30 combinations with an explainable, 5-factor weighted priority scoring model
6. Verifying robustness three ways — 4 contrasting weighting scenarios (**100.0% Top-5 set overlap**), a **2,000-draw Monte-Carlo** over the weight simplex (top-4 combinations robust at ≥95% inclusion), and a **one-way factor dropout** (Top-5 survives intact when the unverified Scarcity factor is removed entirely)
7. Recommending the top 5 prioritized part categories accompanied by concrete supplier-listed OE applications

---

## Selected Vehicles

| Vehicle | Segment | Ethiopian Market Justification | Primary Evidence |
|---------|---------|--------------------------------|------------------|
| **BYD Seagull** | Subcompact Hatchback | Leading urban commuter; high traffic contact exposure; active commercial supplier catalogue. | 37 listings in this project's collected Adey sample (`S001`); 35 Landin catalogue listings (`S003`) — 23 priced, 12 price on request; compatibility supplier-claimed, stock not stated. |
| **BYD Yuan Up** | Compact SUV / CUV | Dominant mass-market family crossover; crucial test case for supplier catalogue gap analysis. | 36 listings in this project's collected Adey sample (`S001`); confirmed catalogue gap on Landin (`S003`). |
| **Toyota bZ4X** | Midsize Electric SUV | High brand equity in Ethiopia; established corporate and embassy fleet presence. | 28 listings in this project's collected Adey sample (`S001`); third-party parts catalogue (`S005`). |

---

## Part Categories Investigated (10 Categories)

1. Brake pads
2. Brake discs
3. Cabin-air filter
4. Wiper blades
5. Headlight assembly
6. Tail-light assembly
7. Side mirror
8. Bumper
9. Fender / body panel
10. Shock absorber

*Total evaluated matrix: 3 vehicles × 10 categories = 30 combinations.*

---

## Project Structure

```
ev-spare-parts-prioritization/
│
├── README.md                           ← [You Are Here] Project overview & quickstart
├── RUBRIC.md                           ← Rubric weights + self-assessment mapped to evidence
├── CONTRIBUTING.md                     ← Contributing guide + the 7 data-integrity rules
├── CHANGELOG.md                        ← Keep-a-Changelog release history
├── REUSE.md                            ← Reference repository attribution & audit
├── LICENSE                             ← MIT license
├── requirements.txt                    ← Python virtual environment dependencies
├── pyproject.toml                      ← Build metadata & tool config (pytest / ruff / black)
├── .editorconfig                       ← Cross-editor whitespace & encoding rules
├── Makefile                            ← Convenience targets (setup / pipeline / test / lint)
├── run_pipeline.py                     ← Offline pipeline orchestrator (raw → … → deck)
├── .github/workflows/ci.yml            ← CI: run pipeline + pytest on windows-latest
│
├── data/
│   ├── raw/
│   │   └── raw_observations.csv        ← 59 rows: unedited scraped & logged observations
│   ├── cleaned/
│   │   └── cleaned_observations.csv    ← 59 rows, 23 columns: normalized currencies, clean taxonomy
│   ├── source_log.csv                  ← Master registry of all 8 sources with URLs, dates & A/B/C reliability tiers
│   ├── scoring_results.csv             ← 30 rows: calculated factor scores, weights, sensitivity ranks
│   ├── sensitivity_monte_carlo.csv     ← 30 rows: Top-5 inclusion probability over 2,000 weight draws
│   └── sensitivity_factor_dropout.csv  ← 5 rows: Top-5 survival when each single factor is dropped
│
├── notebooks/                          ← 4 sequential, fully executed Jupyter Notebooks
│   ├── 01_vehicle_selection.ipynb      ← Vehicle market analysis (5 candidates -> 3 selected)
│   ├── 02_data_collection.ipynb        ← Evidence collection logging across 3x10 combinations
│   ├── 03_data_cleaning.ipynb          ← Cleaning pipeline, currency normalization, missing flags
│   └── 04_analysis_and_scoring.ipynb   ← Weighted scoring model, sensitivity matrix, visualizations
│
├── reports/
│   ├── findings.md                     ← Final recommendations, OE application specs, and roadmap
│   ├── limitations.md                  ← Documented data boundaries, catalogue gaps, and assumptions
│   ├── comprehensive_project_report.md ← Master technical dossier for external audit
│   ├── presentation.md                 ← 7-minute presentation script with speaker notes & defense Q&A
│   ├── EV_Spare_Parts_Prioritization_Presentation.pptx ← 12-slide executive presentation
│   └── figures/                        ← 300 DPI publication charts
│       ├── scoring_matrix_heatmap.png  ← 30-combination prioritization heatmap
│       ├── top10_priority_rankings.png ← Horizontal bar chart of Top 10 recommendations
│       ├── sensitivity_comparison.png  ← Stability across 4 predefined weighting scenarios
│       ├── monte_carlo_stability.png   ← Top-5 inclusion probability over 2,000 Dirichlet draws
│       └── top5_radar_profiles.png     ← 5-axis factor radar charts for Top 5 recommendations
│
├── scraper/                           ← Pipeline automation & export scripts
    ├── compile_raw_observations_defensible.py ← Rebuilds data/raw/raw_observations.csv
    ├── repair_raw_observations.py      ← Applies provenance corrections to raw observations
    ├── generate_scores_defensible.py   ← Authoritative scoring and sensitivity analysis module
    ├── export_figures.py               ← Visualizations exporter producing reports/figures/
    ├── generate_presentation.py        ← Presentation generator producing reports/*.pptx
    ├── main.py / scrapers/             ← Multi-source scraper CLI (13 registered sources)
    └── ...                             ← compile/repair helpers & legacy scripts

├── db/
│   ├── schema.sql                     ← SQLite DDL reference model (5 tables, 4 indexes)
│   └── ev_parts.db                    ← Materialised SQLite build of the datasets (59/30/8 rows)

├── docs/
│   ├── data_dictionary.md             ← Column-level reference for every dataset
│   └── rubric_compliance.csv          ← Machine-readable rubric self-assessment

└── tests/                             ← pytest suite (the executable contract)
    ├── conftest.py                    ← Loads standalone pipeline scripts as modules
    ├── test_data_integrity.py         ← Row counts, provenance, enums, no-fabrication rules
    ├── test_scoring_model.py          ← Recomputes the model, diffs vs committed CSV
    ├── test_scrapers.py               ← Source registry wiring + payload-parsing helpers
    └── test_schema.py                 ← Loads db/schema.sql into SQLite; checks CHECKs
```

> `refer/` is **not part of this project** — it holds third-party reference repositories.
> It is git-ignored and excluded from the submission archive.

---

## Scoring Method & Rubric

Each of the 30 vehicle-part combinations is scored using 5 weighted factors on a 1–5 scale:

$$\text{Priority Score} = 0.30 \times D + 0.25 \times S + 0.20 \times C + 0.15 \times P + 0.10 \times E$$

| Factor | Weight | What It Measures | Justification for Weight |
|--------|:------:|------------------|-------------------------|
| **Demand Evidence Proxy ($D$)** | **30%** | Observed vehicle marketplace presence on Adey Market (`S001`) + component functional wear classification (friction wear vs collision contact vs structural). | Highest weight because an importer's greatest risk is stocking parts with low market turnover. *(Indicative assessment proxy; no workshop replacement rate measured. NHTSA records decoupled).* |
| **Local Distributor Catalogue Gap ($S$)** | **25%** | Degree to which a part is absent from the investigated catalogues (Landin `S003` confirmed gaps; Gezat `S002` reviewed at catalogue/model level only), compared to overseas supplier availability (`S003`/`S005`). | Supply gaps in investigated catalogues indicate commercial stocking necessity. *(Measures investigated online catalogue gaps only; the Gezat `S002` review recorded no per-part search, so local per-part availability is UNVERIFIED. Does not establish physical unavailability in Addis Ababa shops).* |
| **Vehicle Compatibility ($C$)** | **20%** | Verification level of supplier-listed OE reference in named catalogues. | Wrong-fit part shipments cause costly cross-border returns and dead inventory. Verified OE references mitigate fitment risk. |
| **Catalogue Sourcing Practicality ($P$)** | **15%** | Catalogue listing status and unit catalogue price brackets in verified catalogues applied to the primary representative application evaluated. | Evaluates whether a part can be procured with transparent catalogue pricing (listing presence ≠ physical stock). Unverified trade quotations receive P=1 because sourcing feasibility cannot be confirmed without a verified supplier catalogue listing. |
| **Evidence Confidence ($E$)** | **10%** | Degree of cross-validation across independent sources (`S001`–`S008`). | Acts as a data-quality trust multiplier, validating the reliability of underlying catalogue sources. |

*Application Aggregation Rule for $P$*: Category-level scoring evaluates the specific primary application explicitly cited in recommendations. Coexisting secondary variants or unpriced entries within the same category are documented for transparency, but do not override the verified price of the primary application.

---

## Data Sources (Complete 8-Source Registry)

All 59 observations originate from 8 documented sources logged in [`data/source_log.csv`](data/source_log.csv):

| Source ID | Source Name | Role in Project | Evidence Type / Output |
|:---------:|-------------|-----------------|------------------------|
| **`S001`** | **Adey Market** (`adey-market.com`) | Local vehicle marketplace volume | Vehicle market prices (1.9M–4.2M ETB) and sampled listing counts from this project's collected Adey dataset (Seagull 37, Yuan Up 36, bZ4X 28). |
| **`S002`** | **Gezat Electric** (`ev.gezat.et`) | Investigated local EV distributor | Warranty terms and a catalogue/model-level review only — no per-part search recorded, so local per-part availability is UNVERIFIED (S-factor limitation). |
| **`S003`** | **Landin BYD Parts** (`landinparts.com/byd/`) | Overseas supplier catalogue | 35 verified Seagull listings with prices and OE numbers; 8 documented catalogue gaps (filter, wiper, Yuan Up). |
| **`S004`** | **CQSW Auto Parts** (`cqsw.com`) | Secondary benchmark catalogue | Corroborating benchmark used to cross-reference BYD part numbers; not a direct observation row. |
| **`S005`** | **toyota-spare-parts.com** | Third-party parts catalogue | 10 Toyota bZ4X chassis/powertrain part listings and prices. *(Third-party aggregator, NOT official Toyota EPC).* |
| **`S006`** | **NHTSA Datasets** (`nhtsa.gov`) | Safety & defect context | 2 safety context records (Recall 22V444 hub bolts; brake shudder). Used strictly as platform engineering context. |
| **`S007`** | **AutoZone Catalogue** (`autozone.com`) | Aftermarket retail benchmark | Aftermarket benchmark for universal consumable dimensions (filters, wipers); not a direct observation row. |
| **`S008`** | **Export Directory Quotations** | Unverified trade quotations | 4 trade quotations for Yuan Up with unverified trade codes. Scored conservatively ($P=1, E=1$). |

---

## Top 5 Final Recommendations

The scoring model evaluates 30 vehicle-model + part-category combinations. The top 5 recommendations represent prioritized categories accompanied by concrete supplier-listed OE applications:

| Rank | Vehicle Model | Part Category & Defined Application | Priority Score | Catalogue Price | Supplier-Listed OE Reference | Primary Sourcing Reference |
|:----:|---------------|-------------------------------------|:--------------:|:---------------:|------------------------------|----------------------------|
| **#1** | **BYD Seagull** | **Side mirror**<br>*(LH mirror; companion RH)* | **4.60** | 429 RMB ($60.06 USD)<br>*(RH: 264 RMB / $36.96)* | `EQEA-8202100` (LH)<br>`EQEA-8202109` (RH) | Landin Parts (`S003`) catalogue listing (stock not stated) |
| **#2** | **BYD Seagull** | **Brake pads**<br>*(Front pad set; companion Rear)* | **4.45** | 64 RMB ($8.96 USD)<br>*(Rear: 64 RMB / $8.96)* | `EQEA-3501500CH` (Front)<br>`EQEA-3502140SS` (Rear) | Landin Parts (`S003`) / CQSW benchmark |
| **#3** | **BYD Seagull** | **Shock absorber**<br>*(Front strut LH; companion RH)* | **4.45** | 138 RMB ($19.32 USD)<br>*(RH: 138 RMB / $19.32)* | `EQEA-2905100A` (LH)<br>`EQEA-2905200A` (RH) | Landin Parts (`S003`) suspension catalogue |
| **#4** | **BYD Seagull** | **Bumper**<br>*(Front bumper cover upper fascia)* | **4.45** | 198 RMB ($27.72 USD) | `EQEA-2083111`<br>*(OE flagged for supplier confirmation — see limitations)* | Landin Parts (`S003`) body catalogue |
| **#5** | **BYD Seagull** | **Headlight assembly**<br>*(LH headlight; companion RH)* | **4.30** | 418 RMB ($58.52 USD)<br>*(RH: 418 RMB / $58.52)* | `EQEA-4121010B` (LH)<br>`EQEA-4121020B` (RH) | Landin Parts (`S003`) lighting catalogue |

*Robustness Finding: The same five vehicle-category combinations remained in the top five across the four tested weighting scenarios (100% set overlap). Under a stronger **Monte-Carlo** test — 2,000 weight vectors drawn uniformly from the 5-factor simplex (`data/sensitivity_monte_carlo.csv`) — the top **four** combinations are robust (≥95% Top-5 inclusion: Shock absorber 99.1%, Bumper 99.1%, Brake pads 98.7%, Side mirror 95.4%), while the 5th slot is genuinely contested (Headlight assembly 45.5%, Brake discs 48.2%). A **one-way factor dropout** (`data/sensitivity_factor_dropout.csv`) then removes each factor in turn: dropping the **Scarcity (`S`) factor entirely leaves the Top-5 unchanged (5/5)**, so the recommendation does not hinge on the catalogue/model-level distributor review (`S002`) that underpins `S`. Dropping any other single factor keeps at least 4/5 — only Demand is load-bearing. The result demonstrates stability under the tested scenarios, not universal robustness or proven market demand.*

---

## Execution Guide

### 1. Environment Setup
```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install project dependencies
pip install -r requirements.txt
```

### 2. End-to-End Pipeline Execution

The supported way to rebuild every derived artefact is the orchestrator:

```powershell
python run_pipeline.py             # raw → repair → scores → figures → deck
python run_pipeline.py --list      # list stages
python run_pipeline.py --only scores
python run_pipeline.py --notebooks # also re-execute notebooks 01–04
```

The equivalent manual steps (run from the repo root):

```powershell
# 1. Rebuild the raw observation table (only if inputs changed)
python scraper/compile_raw_observations_defensible.py
# 2. Apply provenance corrections to the raw observations
python scraper/repair_raw_observations.py
# 3. Execute scoring engine → data/scoring_results.csv
python scraper/generate_scores_defensible.py
# 4. Export publication charts → reports/figures/
python scraper/export_figures.py
# 5. Generate the 12-slide PowerPoint deck with speaker notes
python scraper/generate_presentation.py
```

### 3. Scraper registry

The multi-source collector app lives in [`scraper/`](scraper/) (`main.py` + `scrapers/`).
Each source is a `BaseScraper` subclass registered in a central registry:

```powershell
python scraper/main.py --list            # list the 13 registered sources
python scraper/main.py --scraper gezat   # scrape one source (→ outputs/gezat.json)
python scraper/main.py --all --pages 2   # run every source, two pages each
```

| Source | Site / endpoint | What it collects |
| :--- | :--- | :--- |
| `adey` | adey-market.com | BYD/Toyota/VW EV listings (`S001`) |
| `landin` | landinparts.com | BYD Seagull parts catalogue (`S003`) |
| `gezat` | gezat.et | Electric-vehicle listing cards (`S002`) |
| `jiji` | jiji.com.et (JSON) | Vehicle listings **and** `scrape_parts()` car-parts searches |
| `mekina` | mekina.net (JSON) | Electric-vehicle listings |
| `afromekina` | api.afromekina.com (JSON) | Electric-vehicle listings |
| `asiautos` | asiautos.net (Shopify feed) | BYD parts / part numbers |
| `evprotec` | evprotec.com (WooCommerce API) | VW ID.4 / ID.6 parts |
| `nbe` | api.nbe.gov.et | Official ETB exchange rates |
| `nhtsa` | api.nhtsa.gov | Owner complaints & recall campaigns (platform context only) |
| `quotes`, `books`, `dynamic_sample` | teaching fixtures | dummy targets for the scraping harness |

The ported sources honour the main app's `BaseScraper` contract and consult `robots.txt`
before fetching. Every fetch redacts phone numbers and e-mail addresses before persisting.

### 4. Verification

```powershell
python -m pytest -ra              # the executable contract (77 tests)
python -m pytest --cov=scraper    # with coverage
```

The suite recomputes the scoring model and diffs it against the committed
`data/scoring_results.csv`, validates dataset schemas/provenance, loads
`db/schema.sql` into SQLite to exercise its CHECK constraints, and checks the
scraper registry wiring plus each source's payload-parsing helpers (offline).

---

## Deliverables Summary

- **Rubric Compliance & Self-Assessment**: [`RUBRIC.md`](RUBRIC.md)
- **Master Technical Report**: [`reports/comprehensive_project_report.md`](reports/comprehensive_project_report.md)
- **Detailed Findings & Procurement Roadmap**: [`reports/findings.md`](reports/findings.md)
- **Documented Limitations & Assumptions**: [`reports/limitations.md`](reports/limitations.md)
- **Data Dictionary**: [`docs/data_dictionary.md`](docs/data_dictionary.md)
- **7-Minute Presentation Script & Defense Q&A**: [`reports/presentation.md`](reports/presentation.md)
- **PowerPoint Presentation Deck**: [`reports/EV_Spare_Parts_Prioritization_Presentation.pptx`](reports/EV_Spare_Parts_Prioritization_Presentation.pptx)
- **SQLite Schema Reference**: [`db/schema.sql`](db/schema.sql)

---

## License

MIT License. Grounded strictly in public automotive evidence.
