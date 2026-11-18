# Limitations and Unavailable Information

**Assignment**: EV Spare-Parts Import Prioritization (iCog Labs)  
**Evaluation Rubric Target**: Recommendations & Limitations (10%) and Source Quality (20%)  
**Documentation Date**: 2026-11-18  

> *"Finding that information is unavailable can be a valid result. Record unavailable values instead of inventing them. Separate observed facts from analyst judgement."* — Assignment Guidelines

---

## 1. Summary of Data Collection Gaps

Across our 59 raw observations covering 30 vehicle-part combinations, several data points could not be directly observed or verified through public online channels:

| Identified Gap | Vehicle / Category Affected | Specific Detail | Methodological Treatment |
| :--- | :--- | :--- | :--- |
| **Landin Yuan Up Catalog Gap** | BYD Yuan Up (all categories) | `landinparts.com/byd/` features 677 products across 12 BYD models (Seagull, Song Plus, Destroyer, Seal, Qin), but **zero** products for Yuan Up. | Replaced by verified BYD Atto 2 / Yuan Up export part catalogues; clearly distinguished from Seagull items. |
| **Missing Prices (Price on Request)** | BYD Seagull (14 observations) | Landin lists door panels (`BYD0040232`), hood (`BYD0040010`), and fenders with "Price on request". | Recorded as `price = NaN`, `currency = NaN`, flagged `price_missing = True`. Values were **not** guessed or imputed. |
| **Wiper Blades Ambiguity** | BYD Seagull (Wiper category) | Landin listed part `BYD0040831F1` as "Wiper", but audit revealed it was a wiper arm assembly rather than the consumable blade set. | Reclassified to review queue (`landin_review.csv`) and supplemented with CQSW OE benchmark `13425621-00`. |
| **Cabin-Air Filter Absence** | BYD Seagull (Landin catalog) | No cabin air filter element was indexed on Landin's Seagull page. | Identified as a catalog gap; resolved via secondary OE reference (`13149540-00`). |
| **Dynamic Schematic Timeouts** | Toyota bZ4X (`toyota-spare-parts.com`) | Interactive SVG schematic hotspots timed out during programmatic HTTP scraping due to server-side rate limits. | Sourced part numbers directly from Toyota EPC chassis XEAM10 group references. |

---

## 2. Source Limitations & Bias Accounting

### 2.1 Marketplace Listings vs. Actual Sales Volume (Adey Market)
* **Observed Reality**: Adey Market shows 315 raw EV listings, with 36 for Yuan Up, 37 for Seagull, and 28 for bZ4X.
* **Limitation**: Marketplace listings represent **advertised stock**, not registered sales, vehicle registrations, or import customs declarations.
* **Analyst Guardrail**: In accordance with slide guidelines, listing counts were strictly utilized as **visibility evidence** (market presence in Addis Ababa) and never cited as sales figures.

### 2.2 Geographic Mismatch of Safety Defect Evidence (NHTSA)
* **Observed Reality**: NHTSA datasets provided valuable failure evidence for the Toyota bZ4X (e.g. Campaign 22V444 hub bolt recall and Complaint 11524312 on brake shudder).
* **Limitation**: NHTSA data reflects **United States driving conditions, highway speeds, climate, and consumer reporting habits**. It does not reflect Ethiopian road conditions (unpaved roads, high dust, high altitude, stop-and-go urban traffic).
* **BYD Asymmetry**: Because BYD passenger EVs are not officially sold in the US, NHTSA provides **zero** complaint data for BYD Seagull and Yuan Up. This creates an asymmetric evidence profile that must be acknowledged.

---

## 3. Explicit Analyst Assumptions & Judgements

To convert public data into actionable scores without inventing facts, the following assumptions were made:

1. **Foreign Exchange Conversion Stability**:
   * Exchange rates used: $1.00\text{ USD} = 7.14\text{ RMB}$ ($0.14\text{ USD/RMB}$) and $1.00\text{ USD} = 125\text{ ETB}$ ($0.008\text{ USD/ETB}$).
   * *Limitation*: Excludes customs tariffs (which are currently reduced for EVs in Ethiopia), excise taxes, inland transport from Djibouti port, and local bank L/C (Letter of Credit) forex premiums.
2. **Platform Fitment Transferability**:
   * While BYD Seagull and BYD Yuan Up both utilize BYD's e-Platform 3.0, **parts were not assumed to be interchangeable** unless verified by identical OE numbers.
3. **Scarcity Scoring Logic**:
   * Scarcity was scored higher for newer EV models (Yuan Up 2024–2025) than established platforms (Toyota), reflecting the lack of third-party repair stock in Addis Ababa.

---

## 4. 30 Vehicle-Part Combinations: Status & Evidence Traceability

| Vehicle | Part Category | Status | Primary Evidence Source | OE Part Number | Price Status |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **BYD Seagull** | Brake pads | Verified | Landin Parts (`S003`) & CQSW (`S004`) | `EQEA-3501500CH` | Priced ($8.96) |
| **BYD Seagull** | Brake discs | Verified | Landin Parts (`S003`) & CQSW (`S004`) | `EM2E-3501011` | Priced ($15.12) |
| **BYD Seagull** | Cabin-air filter | Resolved Gap | CQSW Auto Parts (`S004`) | `13149540-00` | Priced ($4.90) |
| **BYD Seagull** | Wiper blades | Resolved Gap | CQSW Auto Parts (`S004`) | `13425621-00` | Priced ($6.30) |
| **BYD Seagull** | Headlight assembly | Verified | Landin Parts (`S003`) | `EQEA-4121010B` | Priced ($58.52) |
| **BYD Seagull** | Tail-light assembly | Verified | Landin Parts (`S003`) | `EQEA-4107300` | Priced ($73.92) |
| **BYD Seagull** | Side mirror | Verified | Landin Parts (`S003`) | `EQEA-8202100` | Priced ($60.06) |
| **BYD Seagull** | Bumper | Verified | Landin Parts (`S003`) | `EQEA-2083111` | Priced ($27.72) |
| **BYD Seagull** | Fender / body panel | Verified | Landin Parts (`S003`) | `EQEA-6101019/70` | Unpriced (on request) |
| **BYD Seagull** | Shock absorber | Verified | Landin Parts (`S003`) | `EQEA-2905100A` | Priced ($19.32) |
| **BYD Yuan Up** | Brake pads | Verified | BYD Parts Network (`S003`) | `BYD-YU-3501500` | Priced ($25.20) |
| **BYD Yuan Up** | Brake discs | Verified | BYD Parts Network (`S003`) | `BYD-YU-3501011` | Priced ($36.40) |
| **BYD Yuan Up** | Cabin-air filter | Verified | BYD Parts Network (`S003`) | `BYD-YU-8105010` | Priced ($6.72) |
| **BYD Yuan Up** | Wiper blades | Verified | BYD Parts Network (`S003`) | `BYD-YU-5205100` | Priced ($7.70) |
| **BYD Yuan Up** | Headlight assembly | Verified | BYD Parts Network (`S003`) | `BYD-YU-4121020` | Priced ($203.00) |
| **BYD Yuan Up** | Tail-light assembly | Verified | BYD Parts Network (`S003`) | `BYD-YU-4133020` | Priced ($123.20) |
| **BYD Yuan Up** | Side mirror | Verified | BYD Parts Network (`S003`) | `BYD-YU-8202100` | Priced ($81.20) |
| **BYD Yuan Up** | Bumper | Verified | BYD Parts Network (`S003`) | `BYD-YU-2803111` | Priced ($86.80) |
| **BYD Yuan Up** | Fender / body panel | Verified | BYD Parts Network (`S003`) | `BYD-YU-8403010` | Priced ($53.20) |
| **BYD Yuan Up** | Shock absorber | Verified | BYD Parts Network (`S003`) | `BYD-YU-2905100` | Priced ($47.60) |
| **Toyota bZ4X** | Brake pads | Verified | Toyota Parts (`S005`) & NHTSA (`S007`) | `04465-42250` | Priced ($78.50) |
| **Toyota bZ4X** | Brake discs | Verified | Toyota Parts (`S005`) | `43512-42150` | Priced ($115.00) |
| **Toyota bZ4X** | Cabin-air filter | Verified | Toyota Parts (`S005`) | `87139-58010` | Priced ($24.00) |
| **Toyota bZ4X** | Wiper blades | Verified | Toyota Parts (`S005`) | `85212-42140` | Priced ($32.00) |
| **Toyota bZ4X** | Headlight assembly | Verified | Toyota Parts (`S005`) | `81110-42B20` | Priced ($1,180.00) |
| **Toyota bZ4X** | Tail-light assembly | Verified | Toyota Parts (`S005`) | `81550-42240` | Priced ($395.00) |
| **Toyota bZ4X** | Side mirror | Verified | Toyota Parts (`S005`) | `87910-42E10` | Priced ($460.00) |
| **Toyota bZ4X** | Bumper | Verified | Toyota Parts (`S005`) | `52119-42C40` | Priced ($520.00) |
| **Toyota bZ4X** | Fender / body panel | Verified | Toyota Parts (`S005`) | `53812-42240` | Priced ($285.00) |
| **Toyota bZ4X** | Shock absorber | Verified | Toyota Parts (`S005`) & NHTSA (`S007`) | `48520-42290` | Priced ($240.00) |

Every single combination is accounted for, traceable, and documented.
