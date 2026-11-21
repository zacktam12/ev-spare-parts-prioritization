# Data Dictionary — EV Spare-Parts Import Prioritization

Column-level reference for every dataset shipped with this project. All files are
UTF-8 CSV with a single header row and are validated by
[`tests/test_data_integrity.py`](../tests/test_data_integrity.py).

| Dataset | Path | Shape | Role |
| :--- | :--- | :---: | :--- |
| Raw observations | [`data/raw/raw_observations.csv`](../data/raw/raw_observations.csv) | 59 rows × 19 cols | Source-of-truth evidence as collected (one row = one source-backed fact) |
| Cleaned observations | [`data/cleaned/cleaned_observations.csv`](../data/cleaned/cleaned_observations.csv) | 59 rows × 23 cols | Raw + 4 derived columns (USD price, missing flag, cross-check flag, compatibility class) |
| Source registry | [`data/source_log.csv`](../data/source_log.csv) | 8 rows × 7 cols | Master list of the 8 sources (`S001`–`S008`) |
| Scoring results | [`data/scoring_results.csv`](../data/scoring_results.csv) | 30 rows × 14 cols | One row per vehicle × part-category combination; the model output |

> **Unit-of-analysis warning.** These files have different row meanings and must not be
> compared by row count. 59 observations support 30 scored combinations because several
> observations can support one combination.

---

## 1. `data/raw/raw_observations.csv` (59 × 19)

One row = one observation: a supplier catalogue listing, a catalogue gap, an unverified
trade quotation, or a safety-context record.

| # | Column | Type | Description | Allowed values / notes |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `observation_id` | string | Primary key, stable row identifier | `OBS001`–`OBS059`, unique |
| 2 | `vehicle` | string | Vehicle model | `BYD Seagull`, `BYD Yuan Up`, `Toyota bZ4X` |
| 3 | `model_year` | string | Model-year range claimed by the source | e.g. `2023-2024`, `2020-` |
| 4 | `part_category` | string | Harmonised part category (one of the 10) | see §5 |
| 5 | `part_description` | string | Human-readable part name | free text |
| 6 | `oem_part_number` | string | Part reference **as printed by the source** | empty when the source listed no number; NOT independently EPC-verified |
| 7 | `supplier` | string | Supplier / catalogue name | e.g. `Landin BYD Parts` |
| 8 | `price` | float | Catalogue price in the source currency | empty (not `0`) when no price shown |
| 9 | `currency` | string | Source currency | `RMB`, `USD`, `ETB` |
| 10 | `availability` | string | Listing/absence status in the source | `listed_in_catalogue`, `not_listed`, `not_verifiable`, `unverified_quotation`, `not_applicable` |
| 11 | `price_status` | string | Whether a price is visible | `Priced`, `Price on request`, `Not applicable` |
| 12 | `stock_status` | string | Physical stock statement | `Not stated` (default — a listing ≠ stock), `Not applicable` |
| 13 | `compatibility_statement` | string | Fitment text as claimed by the source | free text; supplier claim, not independent verification |
| 14 | `source_id` | string | Foreign key → `source_log.csv` | `S001`–`S008` |
| 15 | `source_url` | string | Deep link to the evidence | URL or `unverified_trade_quotation — URL not recorded at collection` |
| 16 | `collection_date` | date | Date the observation was collected | ISO `YYYY-MM-DD` (standardised to `2026-11-18`) |
| 17 | `evidence_type` | string | Evidence class as originally logged | `supplier_catalogue`, `parts_catalogue`, `catalogue_gap`, `trade_quotation`, `safety_defect_context` |
| 18 | `notes` | string | Analyst notes, flags, SKU, limitation text | free text (quoted; contains commas) |
| 19 | `observation_type` | string | Machine-readable row classification (added by `repair_raw_observations.py`) | `supplier_catalogue`, `catalogue_gap`, `trade_quotation_unverified`, `safety_context` |

### `observation_type` counts (validated in tests)

| Value | Rows | Methodological treatment |
| :--- | :---: | :--- |
| `supplier_catalogue` | 45 | Verified listing in a named catalogue (Landin `S003` or Toyota third-party `S005`) |
| `catalogue_gap` | 8 | Confirmed negative search in Landin `S003` — a valid finding, not an error |
| `trade_quotation_unverified` | 4 | Yuan Up quotes from an unnamed export directory (`S008`) |
| `safety_context` | 2 | NHTSA records (`S006`) — platform context only |

### `source_id` distribution (raw)

`S003` = 43 · `S005` = 10 · `S008` = 4 · `S006` = 2 (sums to 59).

---

## 2. `data/cleaned/cleaned_observations.csv` (59 × 23)

All 19 raw columns, plus 4 derived columns appended in notebook 03 / the cleaning stage.
The cleaning stage harmonises labels, standardises dates, and adds derived flags — it
never fabricates values.

| Column | Type | Description |
| :--- | :--- | :--- |
| `price_usd` | float | `price` converted to USD at fixed analyst benchmark rates (0.14 USD/RMB, 0.008 USD/ETB). Cuurenncy-dependent: RMB/ETB prices are converted, USD prices are passed through. Empty when `price` is empty. |
| `price_missing` | bool | `True` when the source showed no price (22 rows). Guarantees no price was zero-filled. |
| `is_cross_checked` | bool | `True` when a vehicle-category pair has ≥2 distinct non-safety source IDs. Currently `False` for all 59 rows at row level (part-identity cross-checks are documented in prose, e.g. the CQSW `S004` benchmark, rather than attached to individual rows). |
| `compatibility_strength` | string | Fitment-evidence class as claimed by the source |

### `compatibility_strength` values

| Value | Meaning |
| :--- | :--- |
| `confirmed_oem` | Supplier-listed OE reference in a named catalogue with a compatibility statement |
| `catalogue_match` | Listed in a named catalogue (fitment not independently confirmed) |
| `contextual_reference` | Platform/safety context only (not fitment evidence) |
| `unverified_trade_code` | Trade listing code; format not confirmed by an OEM EPC |
| `not_listed` | Catalogue gap — no number or fitment evidence found |

---

## 3. `data/source_log.csv` (8 × 7)

| Column | Description |
| :--- | :--- |
| `source_id` | Key, `S001`–`S008` |
| `source_name` | Human-readable source name |
| `url` | Source URL (or a note when no URL was recorded) |
| `source_type` | Source category (`Marketplace`, `Distributor catalogue`, `Parts supplier catalogue`, `Parts reference`, `Third-party parts catalogue`, `Government safety database`, `Commercial aftermarket catalogue`, `Trade quotation`) |
| `collection_date` | ISO date (`2026-11-18`) |
| `what_it_provides` | What the source contributes to the project |
| `reliability_note` | Honest reliability caveat for that source |

> Note: `source_type` here uses human-readable labels. `db/schema.sql` stores a
> normalised lowercase enum for the same concept.

---

## 4. `data/scoring_results.csv` (30 × 14)

One row = one vehicle × part-category combination. Produced by
[`scraper/generate_scores_defensible.py`](../scraper/generate_scores_defensible.py).

| Column | Type | Description |
| :--- | :--- | :--- |
| `vehicle` | string | Vehicle model |
| `part_category` | string | Part category |
| `demand_evidence` | int 1–5 | Factor **D** |
| `market_scarcity` | int 1–5 | Factor **S** |
| `vehicle_compatibility` | int 1–5 | Factor **C** |
| `sourcing_practicality` | int 1–5 | Factor **P** |
| `evidence_confidence` | int 1–5 | Factor **E** |
| `score_justification` | string | Per-factor evidence citation for the row (>20 chars) |
| `priority_score` | float | `0.30·D + 0.25·S + 0.20·C + 0.15·P + 0.10·E` (range 0–5) |
| `score_Original` | float | Score under baseline weights (30/25/20/15/10) |
| `score_Scarcity_first` | float | Score under 25/30/20/15/10 |
| `score_Equal_weights` | float | Score under 20/20/20/20/20 |
| `score_Evidence_focused` | float | Score under 25/20/20/15/20 |
| `rank` | int 1–30 | Dense rank by `priority_score` (1 = highest), a permutation of 1–30 |

Scenario columns use lowercase snake_case names so they are valid SQL/Python identifiers.

---

## 5. Shared controlled vocabularies

**10 part categories**: Brake pads · Brake discs · Cabin-air filter · Wiper blades ·
Headlight assembly · Tail-light assembly · Side mirror · Bumper · Fender / body panel ·
Shock absorber.

**3 vehicle models**: BYD Seagull · BYD Yuan Up · Toyota bZ4X.

**4 weighting scenarios**: Original (30/25/20/15/10) · Scarcity-first (25/30/20/15/10) ·
Equal-weights (20 × 5) · Evidence-focused (25/20/20/15/20). All sum to 1.00.

---

## 6. Non-negotiable data-integrity rules

These are enforced by [`tests/`](../tests/) and restated in
[`CONTRIBUTING.md`](../CONTRIBUTING.md):

1. Missing prices are **never** zero-filled — they are flagged with `price_missing`.
2. OEM numbers are **never** invented; gaps are recorded as `catalogue_gap`.
3. `toyota-spare-parts.com` is **never** described as the official Toyota EPC.
4. Yuan Up observations are **never** attributed to Landin (`S003`); they carry `S008`.
5. NHTSA (`S006`) rows are **never** used to score C, E, or demand.
6. One SKU per rank — no duplicate combinations in the ranking.
7. Demand and scarcity are labelled analyst judgement, not measured values.
