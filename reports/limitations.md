# Limitations — EV Spare-Parts Import Prioritization

**Assignment**: iCog Labs EV Spare-Parts Import Prioritization  
**Last Updated**: 2026-11-19 (fully revised after external reviewer audit)

---

## 1. Evidence Boundaries

### 1.1 59 Rows ≠ 59 Verified Part Listings

The raw dataset contains 59 rows in four categories:

| Type | Count | Implication |
| :--- | :---: | :--- |
| `supplier_catalogue` | 45 | Verified part listings in a named catalogue. These are the evidence base for scores. |
| `catalogue_gap` | 8 | Confirmed negative search results — part not found in Landin. These are valid findings, not errors. |
| `trade_quotation_unverified` | 4 | Prices and trade codes from an unnamed export supplier (S008). These are **unconfirmed** and should not be treated as sourcing confirmations. |
| `safety_context` | 2 | NHTSA defect/recall records — platform context only, not part fitment or demand evidence. |

### 1.2 Toyota Source Is a Third-Party Catalogue

The URL `toyota-spare-parts.com` is a third-party parts aggregator, **not** Toyota Motor Corporation's official electronic parts catalogue (Toyota's EPC is accessed through authorised dealers). Part numbers on this site follow Toyota's genuine part numbering conventions, but independent confirmation via an authorised Toyota dealer EPC is recommended before placing an order.

**Implication for scores**: Toyota bZ4X Compatibility (C) scores are 4 (not 5) and Evidence Confidence (E) scores are 3 (not 5) throughout the scoring model.

### 1.3 Yuan Up Trade Quotations Are Unverified

Four Yuan Up observations (OBS038, OBS039, OBS043, OBS047) came from an unnamed export supplier directory. The part number format (`BYD-YU-XXXXXXX`) is not a confirmed BYD OEM EPC convention. These cannot be used to confirm fitment, pricing, or availability.

**Implication**: Yuan Up Compatibility (C) scores for trade-quotation rows are 2 (unverified trade code), not 3 or higher.

### 1.4 Landin Yuan Up Absence ≠ Market-Wide Shortage

Landin Parts (`landinparts.com/byd/`) confirmed zero Yuan Up listings as of 2026-11-18. This is a **Landin-specific catalogue scarcity observation** — it does not prove that Yuan Up parts are unavailable through every Chinese domestic supplier, through BYD's own service network, or through direct import channels. It documents one important supply-chain data point.

---

## 2. Analyst Assumptions — Not Observed Data

The following scoring inputs are analyst judgements. No local measurement, survey, or statistical dataset was collected to quantify them. They are explicitly labelled here and in `scrapper/generate_scores_defensible.py`.

| Assumption Used in Scoring | Actual Measurement Available | Consequence If Wrong |
| :--- | :--- | :--- |
| Exterior mirrors are the most frequent urban sideswipe-contact replacement item in Addis Ababa | No local repair-shop frequency data collected | Mirror demand rank may be overstated |
| Addis Ababa peri-urban rough roads accelerate suspension damper fatigue | No road quality survey or workshop replacement rate | Shock absorber demand may be overstated |
| Regenerative braking extends brake rotor replacement cycle 2–3× vs ICE | No local EV workshop data | Rotor demand rank may be understated |
| Front bumper covers are frequently needed in Addis roundabout / lane-change incidents | No accident or body-shop data | Bumper demand may be overstated |
| EV cabin air filter change is required more frequently in Addis due to high dust | No local measurement of filter change intervals | Demand assumption may be incorrect |

---

## 3. Scarcity Measures Local Distributor Catalogue Gaps

The Scarcity factor—specifically operationalized as **Local Distributor Catalogue Gap ($S$)**—measures the absence of a part from the investigated catalogues (Landin `S003` confirmed gaps; the Gezat `S002` review was conducted at catalogue/model level with **no per-part search recorded**), compared to overseas supplier availability (`S003` Landin, `S005` third-party catalogue). **Local per-part availability through Gezat is therefore unverified.** No physical inspection of:
- Addis Ababa spare-parts wholesale market (e.g., Merkato automotive sector)
- Toyota authorised dealer parts departments
- BYD service centres or agents in Ethiopia

was conducted. The actual brick-and-mortar physical availability in Addis Ababa shops may differ—higher or lower—than online catalogue absence implies.

---

## 4. Vehicle Market Presence ≠ Fleet Registration Count

Adey Market listing counts (used for Demand scores) represent **active advertised seller inventory** at the time of data collection (2026-11-18). They are not:
- Cumulative registered vehicle counts from ERCA (Ethiopian Revenue and Customs Authority)
- Sales volume data from any authorised distributor
- Confirmed fleet sizes

The listing counts quoted in this project (Seagull 37, Yuan Up 36, bZ4X 28) come from the collected Adey dataset (`scrapper/outputs/adey_cleaned.csv`, 208 rows) and are treated as a **sample**, not a verified marketplace total. A vehicle model with a large number of Adey listings reflects strong secondary-market trading activity but does not directly measure how many vehicles of that model are currently on Ethiopian roads.

---

## 5. Currency Conversion Is an Analyst Benchmark

Catalogue prices are natively quoted in RMB (Landin) and USD (toyota-spare-parts.com). USD conversion of RMB prices uses a fixed rate of **0.14 USD per RMB**, which is an analyst benchmark. This rate is not sourced from a specific exchange date and does not account for:
- Ethiopia's official vs. parallel-market exchange rates
- Forex availability for import LCs
- Banking commissions and transfer costs

**All original RMB prices are retained** in the dataset alongside converted values. Evaluators should refer to the original currency price for commercial planning.

---

## 6. No Landed Cost or Profit Margin Claims

This analysis provides **supplier catalogue prices only** (FOB or EXW pricing). No landed cost calculations include:
- Sea or air freight charges
- Port of Djibouti handling and transit fees to Modjo Dry Port
- Ethiopian Customs duty and VAT (EV parts classified under HS 8708 series)
- Banking charges for letter of credit issuance
- Importer's warehousing and working capital cost

The report does not and cannot claim any profit margin, ROI, or landed cost from catalogue price alone.

---

## 7. NHTSA Recall Data Is US-Market Evidence Only

NHTSA Campaign 22V444 (Toyota bZ4X wheel hub bolt loosening) and NHTSA Complaint ID 11524312 (bZ4X brake shudder) are US-market records. They establish:
- That the bZ4X platform received regulatory attention in the US for wheel hub fastening integrity (22V444).
- That US bZ4X owners reported friction braking shudder (11524312).

They do NOT establish:
- That the same failure modes are prevalent in Ethiopia.
- That Ethiopian bZ4X owners need shock absorbers or brake pads replaced at any particular rate.
- That the NHTSA-associated OEM part numbers are the correct replacement part for the Ethiopian vehicle configuration.

NHTSA records are classified as `safety_context` in `data/raw/raw_observations.csv` and do not contribute to Demand (D), Compatibility (C), or Evidence Confidence (E) scores.

---

## 8. Scoring Is Analyst Judgement, Not Algorithmic Derivation

Factor scores are manually assigned analyst judgements. They are NOT algorithmically calculated from observation row counts or statistical regression. The scoring rubric defining 1–5 thresholds for every factor is documented in `scrapper/generate_scores_defensible.py` with per-row evidence citations. Any competent analyst reading those citations should be able to replicate or challenge each score independently.

---

## 9. Primary Application Definition & Aggregation Rule

Where a category has physically distinct LH/RH components (mirror assembly, headlight assembly, shock absorber strut) or multiple variant listings, the ranking and factor scoring are evaluated on **one primary representative application**:
- **Side mirror**: Left exterior mirror assembly (`EQEA-8202100`) at 429 RMB (\$60.06 USD $\rightarrow$ $P=4$); companion RH mirror (`EQEA-8202109`) at 264 RMB (\$36.96 USD).
- **Brake pads**: Front brake pad set (`EQEA-3501500CH`) at 64 RMB (\$8.96 USD $\rightarrow$ $P=5$); companion rear pad set at 64 RMB.
- **Shock absorber**: Front shock absorber strut LH (`EQEA-2905100A`) at 138 RMB (\$19.32 USD $\rightarrow$ $P=5$); companion RH strut at 138 RMB.
- **Bumper**: Front bumper cover upper fascia (`EQEA-2083111`) at 198 RMB (\$27.72 USD $\rightarrow$ $P=5$); coexisting lower grille is 88 RMB (\$12.32) and rear bumper is 198 RMB in OBS028.
- **Headlight assembly**: Left headlight assembly (`EQEA-4121010B`) at 418 RMB (\$58.52 USD $\rightarrow$ $P=4$); companion RH headlight at 418 RMB.

*Application Aggregation Rule for P*: Sourcing Practicality is evaluated against the verified catalogue price of the specific primary representative application explicitly cited. Coexisting secondary variants or unpriced entries within the same category are documented for transparency, but do not override the verified price of the primary application. An importer would typically stock companion SKUs (e.g., both LH and RH sides), but scoring is strictly anchored to the primary application to prevent artificial score distortion.
