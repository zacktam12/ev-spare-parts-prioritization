# Presentation Script — EV Spare-Parts Import Prioritization

**Format**: 7-minute defence of [`EV_Spare_Parts_Prioritization_Presentation.pptx`](EV_Spare_Parts_Prioritization_Presentation.pptx) (12 slides)
**Assignment**: iCog Labs Technical Assessment · **Market**: Addis Ababa & regional corridors
**Presenter note**: The slide-by-slide notes below are identical in intent to the speaker notes
embedded in the deck by [`../scraper/generate_presentation.py`](../scraper/generate_presentation.py).

---

## Slide 1 — Title

**Say:** "Good morning. I'm presenting a data-driven decision framework for a critical
commercial problem in Ethiopia: exactly which EV replacement parts an importer should
prioritise under constrained working capital and foreign-exchange rationing. Instead of
relying on assumptions, the framework integrates marketplace evidence, parts catalogues, and
supplier inventories into an explainable, stress-tested scoring model."

**Tone:** state the decision problem under uncertainty — not a claim of measured sales.

---

## Slide 2 — The Ethiopian EV dilemma: policy shift & forex rationing

**Say:** "Ethiopia's 2024 ban on ICE passenger-car imports triggered a surge of EVs into
Addis Ababa. Parts supply has lagged badly, so importers face two risks: stocking parts that
sit on shelves, or stocking parts with unverified fitment. Because forex is rationed, every
dollar of inventory must be justified."

**Key points**
- ICE import prohibition (2024) → rapid EV fleet growth.
- Aftermarket parts support is immature and fragmented.
- Forex/LC rationing makes dead inventory and wrong-fit returns commercially fatal.

---

## Slide 3 — Vehicle selection: 3 representative archetypes

**Say:** "From five candidates we selected three archetypes: BYD Seagull (entry commuter),
BYD Yuan Up (family crossover), and Toyota bZ4X (brand-equity SUV). Selection used marketplace
listing counts from the collected Adey Market sample (`S001`) plus a catalogue/model-level
distributor review (`S002`). Volkswagen ID.4 and Tesla Model 3/Y were excluded for variant
fragmentation and closed service ecosystems respectively."

**Careful phrasing:** listing counts are *observed marketplace presence in a sample*, not
confirmed fleet registrations.

| Vehicle | Segment | Sample listings | Role |
| :--- | :--- | :---: | :--- |
| BYD Seagull | Subcompact hatch | 37 | High-exposure urban commuter |
| BYD Yuan Up | Compact SUV | 36 | Supplier catalogue gap test case |
| Toyota bZ4X | Midsize electric SUV | 28 | Brand-equity benchmark |

---

## Slide 4 — Evidence architecture: 59 observations, 4 types (`S001`–`S008`)

**Say:** "The dataset has 59 observations across four explicitly separated types. Only 45 are
verified supplier catalogue listings — the scoring evidence base. Eight are documented
catalogue gaps, four are unverified trade quotations, and two are NHTSA safety-context
records. Keeping these separate is the backbone of the project's honesty."

| Type | Rows | Treatment |
| :--- | :---: | :--- |
| `supplier_catalogue` | 45 | Verified listing (Landin `S003` / Toyota `S005`) |
| `catalogue_gap` | 8 | Confirmed negative search — a valid finding |
| `trade_quotation_unverified` | 4 | Unnamed export directory (`S008`); scored `P=1, E=1` |
| `safety_context` | 2 | NHTSA (`S006`) — platform context only |

---

## Slide 5 — Data cleaning: taxonomy standardisation & missing-value integrity

**Say:** "Cleaning makes the data comparable without erasing uncertainty. We harmonised part
labels, converted RMB and ETB prices to USD using fixed benchmark rates while retaining the
original amount, preserved unpriced rows as `price_missing = True` rather than zero-filling
them, and excluded NHTSA rows from part cross-checks."

**Pipeline validation**
- Raw observations: **59 rows × 19 columns** in `data/raw/raw_observations.csv`.
- Cleaned observations: **59 rows × 23 columns** in `data/cleaned/cleaned_observations.csv`.
- Cleaned CSV loads with pandas with zero tokenising errors (fully quoted fields).
- All `source_id`s map 1:1 to `data/source_log.csv` (`S003`: 43, `S005`: 10, `S008`: 4, `S006`: 2).

---

## Slide 6 — Scoring methodology

**Say:** "Each of the 30 combinations gets five documented ratings combined with explicit
weights. Demand evidence carries 30% in the baseline because turnover risk dominates under
forex rationing."

`Priority Score = 0.30·D + 0.25·S + 0.20·C + 0.15·P + 0.10·E`

| Factor | Weight | Basis | Range anchor (1 → 5) |
| :--- | :---: | :--- | :--- |
| Demand Evidence (D) | 30% | Adey volume proxy + functional wear class | rare/cosmetic → top-volume/wear |
| Local Distributor Catalogue Gap (S) | 25% | Absence from investigated catalogues | listed → absent from all |
| Vehicle Compatibility (C) | 20% | Verified OE reference in a named catalogue | gap → confirmed OE |
| Catalogue Sourcing Practicality (P) | 15% | Listing + visible unit price bracket | gap/quote → verified <$50 |
| Evidence Confidence (E) | 10% | Independent corroboration | quote/gap → catalogue + cross-check |

**Say (critical):** "The ratings are documented analyst judgements grounded in cited
evidence — they are **not** algorithmically derived from row counts."

---

## Slide 7 — Prioritisation heatmap: 30 combinations

**Show:** `reports/figures/scoring_matrix_heatmap.png`.

**How to read:** rows = part categories, columns = vehicles, cell = priority score.

**Say:** "BYD Seagull averages 3.96 across categories because it has complete supplier pricing
and the strongest local presence. Toyota bZ4X averages 3.61 — honest third-party labelling
(C=4, E=3) places its shock absorber at rank 8 with 3.90. Yuan Up scores lower because of the
Landin catalogue gap and unverified trade quotes."

**Do not say:** "the heatmap proves these parts will sell."

---

## Slide 8 — Top 5 recommendations

**Say:** "All five top combinations are BYD Seagull parts, directly reflecting that Seagull is
the only vehicle with 35 Landin catalogue listings (23 priced, 12 price-on-request; stock not
stated, compatibility supplier-claimed)."

| Rank | Vehicle | Category (primary application) | Score | Catalogue price | OE reference (source) |
| :-: | :--- | :--- | :-: | :--- | :--- |
| #1 | BYD Seagull | Side mirror (LH) | 4.60 | 429 RMB / $60.06 | `EQEA-8202100` / `EQEA-8202109` (`S003`) |
| #2 | BYD Seagull | Brake pads (front set) | 4.45 | 64 RMB / $8.96 | `EQEA-3501500CH` / `EQEA-3502140SS` (`S003`, CQSW `S004`) |
| #3 | BYD Seagull | Shock absorber (front strut LH) | 4.45 | 138 RMB / $19.32 | `EQEA-2905100A` / `EQEA-2905200A` (`S003`) |
| #4 | BYD Seagull | Bumper (front upper fascia) | 4.45 | 198 RMB / $27.72 | `EQEA-2083111` — **flagged for supplier confirmation** (`S003`) |
| #5 | BYD Seagull | Headlight assembly (LH) | 4.30 | 418 RMB / $58.52 | `EQEA-4121010B` / `EQEA-4121020B` (`S003`) |

**Say:** "These are prioritised *categories* with concrete supplier-listed OE applications —
a procurement shortlist, not a purchase order."

---

## Slide 9 — Sensitivity analysis: stability across 4 scenarios

**Show:** `reports/figures/sensitivity_comparison.png`.

**Say:** "We re-scored everything under four weighting perspectives — baseline, scarcity-first,
equal-weights, and evidence-focused. The same five combinations stayed in the top five in every
scenario, a 100% set overlap."

| Scenario | D / S / C / P / E | Top-5 overlap |
| :--- | :--- | :---: |
| Original (baseline) | 30/25/20/15/10 | baseline |
| Scarcity-first | 25/30/20/15/10 | 100% |
| Equal-weights | 20/20/20/20/20 | 100% |
| Evidence-focused | 25/20/20/15/20 | 100% |

**Say (defensible interpretation):** "This demonstrates stability under these selected
scenarios — not universal robustness or proven market demand."

---

## Slide 10 — Strategic import roadmap: two-tier logistics

**Say:** "The ranking converts into a practical roadmap. Phase 1 flies compact, high-turnover
wear items by air to minimise downtime and capital exposure. Phase 2 consolidates heavy struts
and bulky body panels by ocean freight via Djibouti and Modjo Dry Port."

- **Phase 1 — air (fast-turn):** Seagull side mirrors & brake-pad sets (low unit capital).
- **Phase 2 — ocean (heavy stock):** Seagull struts, headlights, bumper covers (LCL/FCL).

---

## Slide 11 — Limitations & honest data boundaries

**Say:** "A defensible analysis states its boundaries."

- **Demand is an indicative proxy** — no Ethiopian workshop replacement rates were measured.
- **No brick-and-mortar survey** — scarcity reflects investigated online catalogue gaps only.
- **Listings ≠ fleet** — Adey counts are advertised seller inventory, not registrations.
- **NHTSA is US-market** — platform context only; not local failure frequency.
- **Yuan Up catalogue gap** — documented as a gap, not filled with invented numbers.
- **FX is a benchmark** — 0.14 USD/RMB; parallel-market dynamics affect landed cost.

---

## Slide 12 — Conclusion & defence cheatsheet

**Say:** "The project delivers a defensible, reproducible, stress-tested shortlist that honours
its data boundaries. Thank you."

**Q: Why did Seagull outrank Yuan Up despite Yuan Up's marketplace presence?**
A: Yuan Up has strong Adey presence, but Landin (`S003`) listed **zero** Yuan Up parts. Seagull
has 35 Landin listings, giving far higher Practicality (P) and Evidence Confidence (E).

**Q: Why is the bZ4X shock absorber only rank 8?**
A: `toyota-spare-parts.com` is a third-party aggregator, not the official Toyota EPC. Labelling
it honestly lowered C to 4 and E to 3, yielding an honest 3.90.

**Q: How sensitive is the ranking to the weights?**
A: The same five combinations stayed in the top five across the four tested scenarios — stability
under these scenarios, not universal robustness.

**Q: Does a high score mean fast sales?**
A: No. It means the combination scored highly on the selected evidence dimensions; sales velocity
was not measured.

**Q: Is the supplier fitment claim independently verified?**
A: Not automatically. Fitment must be confirmed for the exact model year/trim/chassis (ideally
VIN) before ordering. The front bumper OE `EQEA-2083111` is explicitly flagged for confirmation.
