# EV Spare-Parts Import Prioritization

A data-driven recommendation system that identifies which EV replacement parts a new importer should prioritize for the Ethiopian market.

## Business Context

A client wants to import EV replacement parts into Ethiopia but cannot stock every part for every vehicle. This project turns incomplete public information into a defensible import recommendation by:

1. Selecting three EV models with strong Ethiopian marketplace presence
2. Investigating 10 spare-part categories across those vehicles (30 combinations)
3. Building a traceable dataset from public online evidence
4. Scoring each vehicle-part combination using a weighted priority formula
5. Recommending the five highest-priority parts to import first

## Selected Vehicles

| Vehicle | Justification |
|---------|---------------|
| BYD Seagull | Multiple listings on Adey Market; listed on Gezat Electric catalogue |
| BYD Yuan Up | 1,360+ listings on Adey Market; listed on Gezat Electric catalogue |
| Toyota bZ4X | Listed on both Adey Market and Gezat; Toyota brand recognition in Ethiopia |

## Part Categories Investigated

Brake pads · Brake discs · Cabin-air filters · Wiper blades · Headlights · Tail lights · Side mirrors · Bumpers · Fenders/body panels · Shock absorbers

## Project Structure

```
ev-spare-parts-prioritization/
│
├── README.md                           ← You are here
├── requirements.txt                    ← Python dependencies
├── REUSE.md                            ← Reference repository documentation
│
├── data/
│   ├── raw/
│   │   └── raw_observations.csv        ← One row per source observation
│   ├── cleaned/
│   │   └── cleaned_observations.csv    ← Standardized, deduplicated data
│   └── source_log.csv                  ← Every URL visited with dates
│
├── notebooks/
│   ├── 01_vehicle_selection.ipynb       ← Vehicle selection with evidence
│   ├── 02_data_collection.ipynb        ← Data gathering documentation
│   ├── 03_data_cleaning.ipynb          ← Cleaning logic and transformations
│   └── 04_analysis_and_scoring.ipynb   ← Scoring formula, sensitivity, top 5
│
└── reports/
    ├── findings.md                     ← Final recommendations summary
    └── limitations.md                  ← Gaps, assumptions, missing data
```

## Scoring Method

Each vehicle-part combination is scored using five weighted factors:

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| Demand evidence | 30% | Evidence that the part may be needed |
| Market scarcity | 25% | Supply gap or limited availability |
| Vehicle compatibility | 20% | Strength of verified fitment evidence |
| Sourcing practicality | 15% | Ease of obtaining and importing the part |
| Evidence confidence | 10% | Reliability and cross-checking of evidence |

**Formula:**  
`Priority Score = (0.30 × Demand) + (0.25 × Scarcity) + (0.20 × Compatibility) + (0.15 × Practicality) + (0.10 × Confidence)`

Each factor is rated on a 1–5 scale. A sensitivity analysis tests whether changing the weights changes the ranking.

## How to Run

1. Clone this repository
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1        # Windows PowerShell
   pip install -r requirements.txt
   ```
3. Open the notebooks in order (01 → 02 → 03 → 04) in VS Code or Jupyter

## Data Sources

All sources are logged in [`data/source_log.csv`](data/source_log.csv) with URLs and collection dates.

Key sources:
- [Adey Market EV listings](https://adey-market.com/categories/cars?type=cars_electric)
- [Gezat Electric catalogue](https://ev.gezat.et/)
- [Landin BYD Parts](https://www.landinparts.com/byd/)
- [NHTSA datasets](https://www.nhtsa.gov/nhtsa-datasets-and-apis)

## License

MIT
