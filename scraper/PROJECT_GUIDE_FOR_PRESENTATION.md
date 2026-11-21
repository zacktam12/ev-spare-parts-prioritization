# Beginner's Guide to the EV Parts Project

This guide explains the code, files, data flow, and presentation language for someone who understands the business question but is new to programming and data analysis.

> **Scope note:** This guide is based on the files currently in the `scraper` folder. No `.ipynb` notebook files or `data/` directory were found inside this folder. However, several scripts refer to notebooks and data in a neighboring project folder. The notebook explanations below describe what the checked-in helper code expects or writes; they are not a line-by-line explanation of notebook cells that are not present here.

## 1. The project in one minute

The project is trying to help an importer decide which electric-vehicle spare-part categories to investigate or import first. It brings together:

1. **Vehicle-market listings** — examples of EVs advertised on Adey Market.
2. **Parts-catalogue evidence** — examples of parts listed by Landin and a Toyota parts catalogue.
3. **Evidence-quality checks** — whether a part identity, vehicle fit, price, or stock status is actually supported.
4. **A prioritization model** — five human-assigned ratings combined using weights.
5. **Presentation material** — charts and a PowerPoint built from the analysis outputs.

The important limitation is that this is a **prioritization aid**, not proof of actual sales, replacement rates, physical stock, or landed import costs.

## 2. Important words, in everyday language

| Term | Plain-language meaning | Example in this project |
|---|---|---|
| **Scraper** | A program that visits a public web page and copies selected information into structured records. | `adey_spider.py` reads vehicle listing cards. |
| **Spider** | One scraper dedicated to a website or kind of page. | `LandinSpider` reads the Landin parts catalogue. |
| **HTML** | The code a website sends to a browser to describe a page. | The spiders select product-card elements from downloaded HTML. |
| **Parsing** | Turning page text or HTML into usable fields. | Extracting a product title, price, and part number. |
| **Record / row** | One item in a table. | One marketplace vehicle listing or one parts observation. |
| **Field / column** | One kind of information stored for each row. | `vehicle`, `price`, or `source_id`. |
| **CSV** | A plain-text table file that can be opened in Excel. The first row normally names the columns. | `outputs/adey_cleaned.csv`. |
| **JSON** | A structured text format that can store records and nested values. | `outputs/adey_cleaned.json`. |
| **Raw data** | Information close to what was collected, before analysis decisions. “Raw” does not guarantee error-free. | `adey_raw.csv` retains more original listing details. |
| **Cleaned / normalized data** | Data filtered and expressed in a consistent shape for analysis. | Candidate EV listings have a consistent make/model field. |
| **Observation** | A single piece of evidence about a vehicle, part, catalogue listing, gap, or safety context. | One supplier listing for a Seagull bumper. |
| **Source ID / provenance** | A label identifying where a claim came from, so it can be checked. | `S003` is used for Landin in the scripts and audit notes. |
| **OE number** | An original-equipment part reference used to identify a vehicle part. It is not automatically proof that every listing fits every year/trim. | A catalogue part number recorded alongside a bumper. |
| **Cross-check / corroboration** | Comparing one source with another. | Comparing a Landin part identity with a CQSW reference. |
| **Catalogue gap** | A part was not found in the catalogue that was searched. This is not proof that the part cannot be bought elsewhere. | No Seagull cabin-air filter found in the Landin catalogue. |
| **Compatibility / fitment** | Whether a part fits a specific vehicle, model year, trim, or chassis. | A supplier says a part fits “SEAGULL 2023.” |
| **Stock status** | Whether the item is physically available to ship now. | The audit correctly says `Not stated` where the source only shows a listing. |
| **Scoring dimension** | One factor used to rate a vehicle-and-part combination. | Demand proxy or sourcing practicality. |
| **Weight** | How much influence a scoring dimension has in the final formula. | Demand has a baseline weight of 30%. |
| **Sensitivity analysis** | Checking whether the ranking changes when the weights change. | Comparing four alternative weight scenarios. |
| **Heatmap** | A table colored by values to make high and low scores easy to compare. | A 3-vehicle by 10-category score matrix. |
| **Reproducibility** | Someone else can follow the same steps and obtain a traceable result. | Saving source URLs, dates, code, and output tables. |

### A few Python symbols you will see

| Code | How to read it |
|---|---|
| `def scrape(...):` | “Define a reusable action called `scrape`.” |
| `class AdeyMarketSpider:` | “Define a class that groups the Adey scraper's behavior and settings.” |
| `self` | The current scraper object. For example, `self.raw_listings` belongs to this run of the scraper. |
| `for card in cards:` | “Repeat the following steps for each card on the page.” |
| `if condition:` | “Only do the following when this test is true.” |
| `return records` | Give the result back to the code that called the function. |
| `row["price"]` | Read the value in the `price` field of a record. |
| `pd.read_csv(path)` | Use the pandas library to load a CSV table. |
| `df.to_csv(path, index=False)` | Save a pandas table as CSV; `index=False` avoids adding a separate row-number column. |

## 3. What is in this folder?

### Main scraper application

| File | What it does |
|---|---|
| `main.py` | Command-line entry point. Selects a scraper, runs it, and saves returned records. |
| `config.py` | Common HTTP settings such as timeout, request delay, retries, and browser-like request headers. |
| `scrapers/__init__.py` | Registry mapping names such as `adey` and `landin` to scraper classes. |
| `scrapers/base_scraper.py` | Shared web-request and HTML-parsing behavior used by the spiders. |
| `scrapers/adey_spider.py` | Collects Adey EV listings, retains raw fields, and creates a candidate-vehicle subset. |
| `scrapers/landin_spider.py` | Collects BYD Seagull part cards, assigns rough categories, and separates uncertain or excluded items. |
| `scrapers/toyota_spider.py` | Attempts to collect parts from Toyota bZ4X catalogue pages. |
| `scrapers/books_spider.py`, `quotes_spider.py`, `dynamic_spider.py` | Example spiders demonstrating different web-page patterns; they are not the core EV evidence pipeline. |
| `storage/exporter.py` | Writes rows to CSV, JSON, or SQLite. |
| `requirements.txt` | Lists some scraper dependencies. It does not list every analysis/presentation dependency referenced by the other scripts. |

### EV evidence, scoring, and presentation scripts

| File | What it does / important note |
|---|---|
| `outputs/adey_raw.csv` / `.json` | Scraped marketplace records with more of the original listing details. |
| `outputs/adey_cleaned.csv` / `.json` | Candidate EV listings with standardized vehicle fields. “Cleaned” means filtered/normalized, not independently verified. |
| `outputs/landin.csv` / `.json` | Landin catalogue extraction snapshot. |
| `outputs/landin_verified.csv` | Audited subset of 35 records described as verified part applications; “verified” here is classification/audit status, not proof of physical stock. Compatibility is still marked supplier-claimed in the file. |
| `outputs/landin_review.csv` | Catalogue items kept for review because they are ambiguous, related hardware, duplicates, or conflicts. |
| `outputs/landin_quality_audit.md` and `outputs/landin_reconciliation_report.md` | Explain how the Landin records were classified and accounted for. These are valuable evidence-quality references. |
| `compile_raw_observations_defensible.py` | Preferred-looking builder for the research observation table. It explicitly aims to preserve gaps and evidence types. |
| `compile_raw_observations.py` | Older/less defensible alternative. It contains example-like Yuan Up values and weaker provenance claims; do not treat it as interchangeable with the defensible builder. |
| `repair_raw_observations.py` | Corrects source attribution and adds machine-readable observation types to a raw-observation file. |
| `phase1_evidence_correction.py` | Separates catalogue presence, price visibility, and stock status; flags a part-number discrepancy and replaces an unsupported marketplace-count claim. |
| `generate_scores_defensible.py` | Holds the five ratings for each of 30 vehicle/category combinations, calculates weighted scores, and compares weight scenarios. |
| `generate_scores.py` | Backwards-compatible forwarding file for the defensible scoring functions. |
| `export_figures.py` | Reads a scoring-results CSV and writes heatmap, ranking, sensitivity, and radar-chart figures. |
| `generate_presentation.py` | Builds a 12-slide PowerPoint and speaker notes. The script expects charts and analysis context files to exist. |
| `update_notebooks.py` | Edits cells in notebooks named `03_data_cleaning.ipynb` and `04_analysis_and_scoring.ipynb`; those notebooks are not in the current `scraper` folder. |

### Referenced items not present inside this folder

The analysis scripts refer to paths such as `data/raw/raw_observations.csv`, `data/cleaned/cleaned_observations.csv`, `data/scoring_results.csv`, `data/source_log.csv`, `notebooks/03_data_cleaning.ipynb`, and `notebooks/04_analysis_and_scoring.ipynb`. These were not found inside the current `scraper` folder. Some scripts calculate paths relative to the parent folder, while others use paths relative to the current working directory. Before running the full workflow, confirm where those sibling folders are and run commands from the intended project root.

The scraper `requirements.txt` currently lists HTTP scraping packages, but the research scripts also import packages such as pandas, NumPy, Matplotlib, Seaborn, `python-pptx`, and `nbformat`. A successful scraper install alone does not guarantee that the analysis, notebook-editing, chart, or PowerPoint scripts can run.

## 4. How the code runs: the scraper path

Think of the scraper path as a small assembly line:

```text
You run main.py
    ↓
main.py looks up a name in SCRAPER_REGISTRY
    ↓
The selected spider downloads pages using BaseScraper
    ↓
The spider extracts fields and creates Python dictionaries (records)
    ↓
DataExporter writes records to CSV, JSON, or SQLite
```

### Step-by-step example: Adey listings

1. `main.py` reads `--scraper adey`.
2. The registry returns `AdeyMarketSpider`.
3. The spider visits general EV and model-specific public pages.
4. It reads page cards and extracts title, price, seller, location, URL, and date.
5. It keeps the broad extraction in `adey_raw` and filters recognized candidate models into `adey_cleaned`.
6. It writes both CSV and JSON files beneath `outputs/`.

The cleaned listing is still only a **marketplace snapshot**. It is not a census of all Ethiopian EVs, proof of completed sales, or proof of the advertised price being paid.

Here is the same idea in a small excerpt from the project, simplified to show the flow:

```python
record = self.parse_card(title, raw_price, raw_meta, listing_url, endpoint_url, collection_date)
self.raw_listings.append(record)

if record["vehicle_make"] and record["vehicle_model"]:
    self.cleaned_listings.append(record)

DataExporter.to_csv(self.cleaned_listings, "outputs/adey_cleaned.csv")
```

Read it as: make a structured record from one web card, keep it in the raw collection, keep it in the candidate collection only if a make and model were recognized, then export the candidate records. The actual spider writes a selected set of fields into its cleaned record before exporting.

### Step-by-step example: Landin catalogue

1. `LandinSpider` downloads the BYD parts page.
2. It limits records to cards whose compatibility text mentions Seagull.
3. It reads product details such as supplier SKU, OE number, price, and product URL.
4. Keyword rules assign a tentative category or send an item to an uncertain/review or excluded group.
5. The spider returns target records and automatically writes its review records.
6. The separately maintained audit files document later human checks, conflicts, and reconciliations.

Keyword classification is a first pass, not engineering approval. The Landin audit gives examples where a title and an OE reference disagreed, so uncertain items should remain in review rather than be silently forced into a category.

### Command-line examples

Run these from the `scraper` folder:

```powershell
python main.py --list
python main.py --scraper adey --format csv
python main.py --scraper landin --format csv
```

The first lists scraper names; the others perform live web requests. The number of pages, file format, and output path can also be supplied through the options in `main.py`. Respect site terms and request limits; a saved output is time-sensitive and should carry its collection date.

## 5. How the evidence is organized

### Three useful levels of data

1. **Marketplace listing** — one advertised vehicle. It can help describe observed online vehicle presence.
2. **Raw observation** — one source-backed fact, such as a part listing, catalogue gap, price, or safety-context record.
3. **Scoring combination** — one vehicle model paired with one target part category. The current scoring module describes 3 vehicles × 10 categories = 30 combinations.

These are different units. For example, 59 raw observations can support 30 scored combinations because several observations can relate to one combination. Do not compare the row count in one file with the row count in another as if they mean the same thing.

### Why the observation table has source and evidence fields

The raw-observation builder is intended to give each row:

- a unique `observation_id` such as `OBS001`;
- the vehicle and part category;
- a description and, when available, an OE number;
- supplier, price, currency, and availability-related fields;
- a `source_id` and source URL;
- collection date and evidence type; and
- notes describing limitations or interpretation.

`source_id` is the link between a claim and a source register (the referenced `data/source_log.csv`). For a presentation, describe it as a traceability label: it lets a reviewer ask, “Where did this claim come from?”

### Do not combine these three ideas

- **Catalogue presence:** a page lists the part.
- **Price visibility:** a price is displayed or a quote is requested.
- **Physical stock:** the supplier has the part ready to ship.

The correction script explicitly separates them. A displayed price does **not** prove stock. The Landin audit says stock was not stated, so say “listed, stock status not stated,” not “in stock.”

### Evidence classes in the defensible builder

The builder distinguishes supplier/parts catalogue entries, catalogue gaps, trade quotations, and safety context. Those classes are not equally strong:

- A named catalogue entry is evidence that a source displayed a part.
- A catalogue gap means the searched source did not display it; another source may carry it.
- An unverified trade quotation is not the same as a verified OEM catalogue listing.
- A safety recall or complaint provides context about a platform or symptom; it does not prove demand for a particular replacement part.

## 6. The intended analysis and notebook path

The helper code points to a workflow like this:

```text
outputs/adey_cleaned.csv + audited parts evidence
                 ↓
compile_raw_observations_defensible.py
                 ↓
data/raw/raw_observations.csv
                 ↓
repair_raw_observations.py and evidence corrections
                 ↓
notebook 03: cleaning, categorization, quality checks
                 ↓
data/cleaned/cleaned_observations.csv
                 ↓
notebook 04 / generate_scores_defensible.py
                 ↓
data/scoring_results.csv
                 ↓
export_figures.py → reports/figures/
                 ↓
generate_presentation.py → PowerPoint
```

This is the **intended/referenced workflow**, not a guarantee that every step currently runs from this folder. Check the actual notebooks, source log, input data, working directory, and required packages before trying to reproduce it.

### What a notebook is

A Jupyter notebook (`.ipynb`) is a document containing ordered cells. A cell can be explanatory text or code. You run code cells to produce tables, printed checks, and charts. The outputs shown in a notebook can be old; rerun cells from top to bottom when you need to verify them. The file `update_notebooks.py` is a helper that replaces selected cells in notebooks 03 and 04; it is not itself a notebook and does not show all the notebook logic.

### What notebook 03 is intended to explain

According to `update_notebooks.py`, notebook 03 includes or is updated to:

- identify cross-checked vehicle/category pairs using distinct source IDs;
- exclude safety-context rows from the cross-check count;
- classify compatibility evidence (for example, supplier claim versus catalogue match);
- save a cleaned CSV and read it back as an export check.

**Cross-checked** should be presented carefully: two sources can support part identity without proving supplier-specific fitment or model-year interchangeability.

### What notebook 04 is intended to explain

According to the helper code, notebook 04:

- loads the scoring table from `generate_scores_defensible.py`;
- calculates weighted scores for four scenarios;
- displays the top five for each scenario; and
- measures how many baseline top-five recommendations remain in each alternative.

The weights are:

| Dimension | Baseline weight | Plain meaning |
|---|---:|---|
| Demand evidence | 30% | Indicative demand proxy based partly on observed vehicle listings and part function; not measured replacement rates. |
| Market scarcity | 25% | Investigated catalogue-gap judgement; not a physical survey proving local unavailability. |
| Vehicle compatibility | 20% | Strength of fitment/part-reference evidence in named sources. |
| Sourcing practicality | 15% | Catalogue listing and indicative unit-price visibility; not freight, tax, or landed cost. |
| Evidence confidence | 10% | How well the claim is supported and cross-checked. |
| **Total** | **100%** | The weights sum to 1.00. |

The formula is:

```text
priority score =
    0.30 × demand evidence
  + 0.25 × market scarcity
  + 0.20 × vehicle compatibility
  + 0.15 × sourcing practicality
  + 0.10 × evidence confidence
```

Each input rating is generally on a 1-to-5 scale. The result is a weighted rating, not a forecast of units sold, revenue, profit, or stockout probability.

### A crucial explanation of the score

In the current code, `get_scoring_data()` contains the vehicle/category ratings and written justifications. `calculate_scores()` applies the formula and sorts the results. Therefore:

- The **ratings are structured analyst judgments**, documented with evidence notes.
- The code **does not automatically derive all five ratings by counting rows** in the raw observation CSV.
- The calculation is reproducible if the ratings and weights stay the same, but the ratings themselves still require transparent human judgment.

Say this directly in a defense. It is more accurate than saying “the algorithm discovered the demand.”

### Sensitivity analysis, simply explained

Sensitivity analysis asks: “If decision-makers care more about scarcity, or evidence confidence, would the recommended top five change?” The code compares:

- Original baseline weights;
- Scarcity-first weights;
- Equal weights; and
- Evidence-focused weights.

If the same recommendations remain near the top, you can say the result was stable **under these tested weight choices**. Do not claim universal robustness or market validation from four scenarios alone.

## 7. What the audit files teach you to say

The Landin reports describe a snapshot reconciliation:

- 83 original scraped rows;
- 35 records in the verified subset;
- 48 of those original rows moved to review;
- 102 additional catalogue review items;
- 150 total review records; and
- 12 unrelated items excluded.

The report's arithmetic is `35 + 150 + 12 = 197` catalogue-universe items, and `35 + 48 = 83` for the original extraction. These are **audit-reported counts for that snapshot**, not permanent counts from a live website.

Useful distinctions from the audit:

- **Verified classification is not the same as verified compatibility.** The reconciliation report says the 35 verified rows have supplier-claimed compatibility.
- **Part identity is not fitment proof.** A second catalogue may confirm the name/identity of a part without proving that a particular supplier SKU fits a given vehicle variant.
- **A conflict is a result.** Four bumper/fender disagreements were retained in review rather than guessed away.
- **No listing is useful evidence when reported honestly.** The absence of a confirmed cabin filter or wiper blade in a searched catalogue can be recorded as a gap, not filled with invented certainty.
- **A price is not stock or landed cost.** Import costs also depend on shipping, insurance, duties, taxes, minimum order quantities, and foreign-exchange conditions.

## 8. Presentation guide: what to say and what each visual means

Use the following sequence as a speaking guide. The PowerPoint generator writes 12 slides and speaker notes; align your final wording with the actual generated deck and the evidence you can show.

### Opening: business problem

**Say:** “The business problem is how to prioritize limited import capital across EV spare parts when local demand and supply evidence are incomplete.”

**Express:** A decision problem under uncertainty—not a claim that the project has measured exact sales.

### Why these vehicles?

The deck describes BYD Seagull, BYD Yuan Up, and Toyota bZ4X as three representative vehicle choices. It cites marketplace sample counts and differing parts-evidence coverage.

**Say:** “We selected three representative models to compare market presence and parts evidence across distinct vehicle types.”

**Express:** The models are the project’s comparison set. Online listing counts indicate observed marketplace presence in the collected sample; they are not the complete fleet population.

### Sources and evidence collection

**Say:** “We collected marketplace listings and catalogue evidence, preserved source URLs and collection dates, and separated direct catalogue listings from gaps, unverified quotations, and safety context.”

**Express:** Where information comes from and how its confidence differs.

### Data cleaning and quality control

**Say:** “We standardized vehicle and part categories, retained uncertain records for review, and avoided treating a visible price as proof of stock.”

**Express:** Cleaning makes data comparable; it must not erase uncertainty or convert a guess into a fact.

### Scoring model

**Say:** “Each vehicle-and-part category receives five documented ratings. We combine them using explicit weights, with demand evidence weighted at 30% in the baseline.”

**Express:** A transparent decision framework. Add: “The ratings are analyst judgments grounded in the collected evidence; they are not automatically calculated from raw listing counts.”

### Heatmap

**How to read it:** Rows are part categories, columns are vehicles, and each cell is a priority score. The color and number let you compare combinations.

**Say:** “The heatmap helps identify which vehicle/category combinations score higher under the baseline assumptions.”

**Do not say:** “The heatmap proves these parts will sell.”

### Ranked list / bar chart

**How to read it:** Each bar represents one vehicle-plus-category combination; longer bars mean higher weighted scores.

**Say:** “This ranking helps shortlist where to investigate first. Before purchasing, we would validate fitment, supplier stock, and landed cost.”

### Sensitivity chart

**How to read it:** The same recommendations are recalculated under different weights.

**Say:** “We tested whether the top-five set changes under four plausible weighting scenarios. This checks model sensitivity, not market truth.”

### Limitations and recommendation

**Say:** “The analysis uses public listings and catalogues, not workshop replacement-rate data or a physical survey of every Addis Ababa parts shop. Stock, freight, and landed costs require supplier confirmation.”

**Express:** You understand what the model can support and what needs further validation.

### Close

**Say:** “The output is a traceable shortlist for supplier and market validation—not an automatic purchase order. The next step is to confirm vehicle fitment by VIN/model year, obtain written stock and quote details, and validate local demand with importers, workshops, or fleet operators.”

## 9. Questions you may be asked

### “Does a high score mean the part will sell quickly?”

No. It means the combination scored highly against the selected evidence dimensions and weights. Actual sales velocity was not measured.

### “How do you know the part is available in Addis Ababa?”

The project investigated public catalogue information, but the scoring notes explicitly state that the local distributor review did not record a per-part search. Physical/local availability is therefore unverified unless separately confirmed.

### “Why use analyst judgments instead of a machine-learning model?”

The current data are sparse and heterogeneous. The transparent weighted framework makes assumptions visible and reviewable. It should not be described as machine learning.

### “Is the supplier's fitment claim independently verified?”

Not automatically. The audit distinguishes a supplier claim from an independent part-identity cross-check. Fitment should be confirmed for the exact model year, trim, chassis, and ideally VIN before ordering.

### “Does a displayed price include delivery and taxes?”

No. It is a catalogue/listing price in the displayed currency. Freight, insurance, duties, taxes, payment terms, and exchange rates are not included unless separately documented.

### “Why keep records that are uncertain?”

Keeping them in a review queue preserves the audit trail and makes unresolved conflicts visible. Deleting them or labeling them as verified would hide uncertainty.

## 10. Cautions before presenting or rerunning

1. **Check the exact files and dates.** Counts in the scripts and PowerPoint are snapshots; website content can change.
2. **Use the defensible observation builder as the conceptual baseline.** The older builder contains examples that the defensible version explicitly corrects.
3. **Review provenance before relying on output.** `repair_raw_observations.py` says it corrects Yuan Up quotation sources and NHTSA source IDs. The defensible builder currently writes NHTSA rows with `S007`, while the repair script says they should be `S006`; this is a concrete reason to inspect the corrected output and source log rather than assume the builder alone is final.
4. **Confirm source IDs against `data/source_log.csv`.** That file is referenced but is not in this folder.
5. **Keep the three status fields separate.** A record can be listed, priced, and still have unknown physical stock.
6. **Confirm missing notebook/data locations.** The notebook updater and analysis scripts use paths that may depend on the working directory.
7. **Check presentation claims against generated outputs.** `export_figures.py` needs `data/scoring_results.csv`; the PowerPoint script expects chart images and other analysis content. Do not claim a chart was regenerated unless you have checked its inputs and date.
8. **Do not present unsupported counts as national market totals.** Adey counts are counts in the collected sample.
9. **Do not claim NHTSA proves replacement demand.** The scoring module explicitly treats NHTSA records as platform safety context, not a demand score input.
10. **Treat scores as prioritization, not procurement approval.** Supplier confirmation and landed-cost analysis are still needed.

## 11. A simple end-to-end explanation to memorize

> “First, we collected public EV marketplace listings and parts-catalogue records. We preserved URLs, dates, and source labels so claims could be traced. Next, we standardized the data and separated verified-looking listings from catalogue gaps, ambiguous records, and safety context. Then we scored 30 vehicle-and-part combinations on demand evidence, catalogue scarcity, compatibility, sourcing practicality, and evidence confidence. Those ratings are documented analyst judgments, combined using explicit weights. We tested alternative weights to see whether the shortlist changes. The result is a transparent shortlist for further supplier and local-market validation—not proof of sales, physical stock, or final landed cost.”

## 12. Quick file navigation

- Scraper entry point: `main.py`
- Shared scraper behavior: `scrapers/base_scraper.py`
- Adey vehicle listings: `scrapers/adey_spider.py` and `outputs/adey_cleaned.csv`
- Landin part extraction: `scrapers/landin_spider.py` and `outputs/landin.csv`
- Landin audit decisions: `outputs/landin_quality_audit.md` and `outputs/landin_reconciliation_report.md`
- Intended raw evidence builder: `compile_raw_observations_defensible.py`
- Provenance repair: `repair_raw_observations.py`
- Availability/price/stock correction: `phase1_evidence_correction.py`
- Scoring and sensitivity logic: `generate_scores_defensible.py`
- Chart generator: `export_figures.py`
- PowerPoint generator and speaker notes: `generate_presentation.py`
- Notebook update helper: `update_notebooks.py`
