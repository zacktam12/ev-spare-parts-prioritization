# Reference Repository Documentation (REUSE.md)

The assignment identifies three GitHub repositories for reference. This document records what was examined, what was reused or adapted, and what was rejected — as required by the assignment's reuse rules.

> *"Existing code may be reused when cited. Explain what you reused, changed or rejected. Unexplained copied work receives no reasoning or implementation marks."*

---

## 1. Automotive Part Interchange Database

**Repository:** [github.com/3r1nC/automotive-part-interchange-database](https://github.com/3r1nC/automotive-part-interchange-database)

**What it is:** A prototype automotive part interchange system built with Python, SQLite, Pandas, and Streamlit. It demonstrates how OE, OEM, and aftermarket parts can be cross-referenced across vehicle applications using relational database design.

**What was examined:**
- Relational schema: `vehicles`, `parts`, `cross_references`, `fitment` tables
- Sample CSV data: `sample_vehicles.csv`, `sample_parts.csv`, `sample_fitment.csv`, `sample_cross_references.csv`
- The concept of **fitment types**: "Exact Fit" vs "Functional Interchange"
- Streamlit web application (`src/app.py`)

**What was reused/adapted:**
- **Fitment type concept** → Adapted into our `compatibility_statement` and `compatibility_strength` columns in `raw_observations.csv` and `cleaned_observations.csv`. Instead of their binary "Exact Fit / Functional Interchange", we use a richer set: `confirmed_oem`, `catalogue_match`, `generic_listing`, `not_verifiable`, `not_listed`.
- **Relational thinking** → The idea that vehicle → part → fitment evidence should be traceable influenced our dataset design where each row links a vehicle, part category, source, and compatibility evidence.

**What was rejected:**
- **Sample data**: Their data covers Ford, Honda, Lincoln (ICE vehicles). None of it applies to BYD or Toyota EVs.
- **Streamlit application**: Not required by the assignment. Building a web UI would add complexity without contributing to the scoring or recommendation deliverables.
- **SQLite database**: Our dataset is small enough (≤30 vehicle-part combinations) that CSV + Pandas is simpler and more transparent than a database.

---

## 2. FAPI Auto Parts Cross-Reference

**Repository:** [github.com/fapi-dev/auto-parts-cross-reference](https://github.com/fapi-dev/auto-parts-cross-reference)

**What it is:** A sample of a commercial cross-reference database containing 22,550 analog (cross-reference) records, 13,869 part numbers, and 1,506 brands. It demonstrates how equivalent part numbers from different manufacturers are linked.

**What was examined:**
- Database schema: `manufacturer_list`, `product_list`, `analog_list` tables
- The **normalized search** concept: part numbers stored in lowercase, letters+digits only (`ns` column)
- The **rating system**: Each cross-reference has a rating reflecting how many sources confirm vs. dispute it
- SQL query examples for looking up part equivalents

**What was reused/adapted:**
- **Reliability rating concept** → Adapted into our `evidence_confidence` scoring factor (10% weight). Their system rates cross-references by source count; we rate each observation by whether it's cross-checked, from an identifiable manufacturer, and consistent with other sources.
- **Part number normalization idea** → When comparing OEM part numbers across sources, we normalize them (remove spaces, dashes, lowercase) to catch matches like "BYD-SG-BP01" and "BYDSGBP01".

**What was rejected:**
- **The database content**: It's a commercial European/global parts database. The sample data contains brands like Bosch, Mercedes-Benz — none relevant to BYD Seagull or Toyota bZ4X spare parts in Ethiopia.
- **SQL loading approach**: No need to set up MySQL/PostgreSQL for our small dataset.
- **The full dataset**: Licensed for evaluation only, not redistributable, and irrelevant to our specific vehicle-part combinations.

---

## 3. Spare Parts Inventory

**Repository:** [github.com/vivasvana1/SparePartsInventory](https://github.com/vivasvana1/SparePartsInventory)

**What it is:** A comprehensive spare parts inventory system using the M5 Forecasting Competition (Walmart) dataset. It implements demand forecasting (TSB, Croston, Prophet, SARIMAX, ETS), inventory optimization (CPLEX), supply chain simulation (anyLogistix), and Power BI dashboards.

**What was examined:**
- Notebook pipeline: `01_data_preparation.ipynb` → `02_data_preparation.ipynb` → `03_exploratory_data_analysis.ipynb` → `04_demand_forecasting.ipynb` → `05_inventory_optimization.ipynb` → `06_anylogistix_simulation_tables.ipynb`
- Project organization: numbered notebooks, separate `All plots/` directory, structured README with table of contents
- Forecasting methodology: ADI-CV² demand classification framework
- ABC-XYZ classification for inventory prioritization

**What was reused/adapted:**
- **Notebook numbering convention** → We adopted the `01_`, `02_`, `03_`, `04_` prefix pattern for sequential notebooks. This makes the analysis pipeline clear and reproducible.
- **Pipeline organization** → The idea that each notebook should produce outputs that feed the next notebook. Our flow: vehicle selection → data collection → data cleaning → scoring & recommendations.
- **README structure** → Adapted their use of tables, architecture diagrams, and clear section headers for our README.

**What was rejected:**
- **M5 Walmart dataset**: This is US retail demand data, not Ethiopian EV spare parts. It cannot be used as evidence of demand.
- **Demand forecasting models** (TSB, Croston, Prophet, SARIMAX, ETS): The assignment asks for a scoring-based prioritization, not time-series forecasting. We don't have historical demand data to forecast against.
- **CPLEX optimization**: Mathematical programming for inventory levels is out of scope. We're recommending which parts to stock, not optimizing reorder quantities.
- **anyLogistix simulation**: Supply chain network simulation is not required.
- **Power BI dashboards**: Not required by the assignment; Jupyter notebook visualizations are sufficient.
- **ABC-XYZ classification**: While conceptually interesting, we don't have the sales volume data needed to classify parts into ABC categories.

---

## Summary

| Repository | Ideas Borrowed | Data/Code Reused Directly | Reason for Rejection |
|------------|---------------|---------------------------|----------------------|
| Automotive Part Interchange DB | Fitment types, relational structure | None (different vehicles, different context) | ICE vehicles, Streamlit not needed |
| FAPI Cross-Reference | Rating system, number normalization | None (commercial European data) | Not EV-relevant, not Ethiopian market |
| Spare Parts Inventory | Notebook numbering, pipeline pattern, README style | None (Walmart data, forecasting models) | Different problem type, overkill tools |

All three repositories provided **structural and conceptual inspiration** but none provided data or code that could be directly applied to the Ethiopian EV spare parts import question.
