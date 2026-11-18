# Findings — Top 5 EV Spare Parts Import Recommendations

**Assignment**: EV Spare-Parts Import Prioritization (iCog Labs)  
**Target Market**: Ethiopia (Addis Ababa metropolitan & regional corridors)  
**Analysis Date**: 2026-11-18  
**Dataset Reference**: [`data/cleaned/cleaned_observations.csv`](../data/cleaned/cleaned_observations.csv)  
**Scoring Output**: [`data/scoring_results.csv`](../data/scoring_results.csv)  

---

## 1. Executive Summary

A new automotive importer entering the Ethiopian EV replacement parts market faces significant capital constraints and warehouse limitations. Attempting to stock every part for every vehicle risks capital lockup, high holding costs, and unsold inventory.

By analyzing 59 verified public observations across 3 primary candidate vehicles (**BYD Seagull**, **BYD Yuan Up**, and **Toyota bZ4X**) and 10 core spare-part categories, we designed an explainable, 5-factor priority scoring model:

$$\text{Priority Score} = 0.30 \times D + 0.25 \times S + 0.20 \times C + 0.15 \times P + 0.10 \times E$$

We recommend the client prioritize importing **high-frequency urban wear items and vulnerable exterior collision components** for vehicles with established marketplace visibility in Addis Ababa.

---

## 2. Top 5 Recommended Spare Parts for Import

| Rank | Vehicle | Part Category | Priority Score (Max 5.0) | Unit Cost (Est. USD) | OEM Part Number | Primary Sourcing & Demand Rationale |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **#1** | **BYD Seagull** | **Side mirror** | **4.75** | $36.96 – $60.06 | `EQEA-8202100` / `EQEA-8202109` | Highest urban collision damage frequency in congested Addis streets; Landin catalogue verified; high local markup potential. |
| **#2** | **Toyota bZ4X** | **Shock absorber** | **4.60** | $240.00 | `48520-42290` | Severe suspension stress from heavy EV curb weight (>2,000 kg) on Ethiopian gravel/potholed topography; corroborated by NHTSA safety recall #22V444. |
| **#3** | **BYD Yuan Up** | **Side mirror** | **4.55** | $81.20 | `BYD-YU-8202100` | Supported by 1,360+ marketplace listings on Adey Market; motorized camera assembly highly vulnerable to urban sideswipes; acute local scarcity. |
| **#4** | **Toyota bZ4X** | **Brake pads** | **4.50** | $78.50 | `04465-42250` | Direct NHTSA complaint ID 11524312 on low-speed friction braking transition shudder; high stop-and-go wear; universal global availability. |
| **#5** | **BYD Yuan Up** *(Tied)* | **Brake pads** | **4.45** | $25.20 | `BYD-YU-3501500` | Massive expanding urban fleet; friction wear item; low volumetric shipping weight allows low-cost sea/air consolidation. |
| **#5** | **BYD Seagull** *(Tied)* | **Brake pads** | **4.45** | $8.96 | `EQEA-3501500CH` / `EQEA-3502140SS` | Ultra-low unit cost (64 RMB); high turn rate among commuter EV owners; verified by Landin and CQSW OE benchmarks. |
| **#5** | **BYD Yuan Up** *(Tied)* | **Cabin-air filter** | **4.45** | $6.72 | `BYD-YU-8105010` | Mandatory routine service consumable (every 5,000–10,000 km) given severe dust levels in Addis Ababa; high margin consumable. |

---

## 3. Supporting Evidence by Recommended Component

### 1. BYD Seagull — Side Mirror Assembly (`Score: 4.75`)
* **Demand (5/5)**: Side mirrors represent the highest replacement incidence in dense Addis Ababa traffic, where sideswipes in minibus taxi lanes and tight parking are routine.
* **Scarcity (4/5)**: No local mirror fabrication or glass replacement capability exists for modern electric vehicles in Ethiopia; owners face weeks of downtime waiting for private air parcels.
* **Compatibility (5/5)**: Verified OEM part numbers `EQEA-8202100` (LH) and `EQEA-8202109` (RH) confirmed on Landin Parts catalogue.
* **Sourcing Practicality (5/5)**: Fully priced at ¥264 RMB ($36.96) to ¥429 RMB ($60.06), with active stock availability. Compact shipping footprint.

### 2. Toyota bZ4X — Front Shock Absorber Strut (`Score: 4.60`)
* **Demand (5/5)**: Electric vehicles carry heavy traction battery packs, increasing dynamic axle loading. Ethiopian road topography (unpaved corridors, speed humps, potholes) significantly shortens damper lifespan. Supported by NHTSA safety documentation noting suspension/hub fastening stresses.
* **Scarcity (4/5)**: Traditional Toyota ICE shock absorbers (e.g. RAV4 or Corolla) are incompatible with the dedicated e-TNGA bZ4X platform.
* **Compatibility (5/5)**: Official Toyota EPC part number `48520-42290` verified for the 2023 XEAM10 series.
* **Sourcing Practicality (4/5)**: Priced at $240.00 USD through Toyota genuine parts networks.

### 3. BYD Yuan Up — Side Mirror Assembly (`Score: 4.55`)
* **Demand (5/5)**: Adey Market data demonstrates over 1,360 listings for the BYD Yuan Up / Atto 2 series, confirming rapid adoption. Side mirrors are front-line collision wear items.
* **Scarcity (5/5)**: Because the Yuan Up is a late 2024–2025 release, local spare-parts supply in Addis Ababa is near zero.
* **Compatibility (4/5)**: OEM application spec `BYD-YU-8202100` verified against BYD overseas catalog.
* **Sourcing Practicality (4/5)**: Procured from overseas export suppliers at ~$81.20 USD.

### 4. Toyota bZ4X — Front Brake Pad Set (`Score: 4.50`)
* **Demand (5/5)**: Documented via NHTSA Consumer Complaint ID 11524312 citing friction-to-regenerative braking shudder. Heavy vehicle mass drives accelerated friction material wear.
* **Scarcity (3/5)**: Toyota parts distributors operate in Ethiopia, but dedicated EV compound ceramic pads remain scarce.
* **Compatibility (5/5)**: Confirmed OE `04465-42250` from Toyota official parts manual.
* **Sourcing Practicality (5/5)**: Highly accessible globally ($78.50 USD), compact freight profile.

### 5. High-Velocity Wear Consumables: BYD Brake Pads & Cabin Filters (`Score: 4.45`)
* **Strategic Role**: Low-risk inventory anchors. At $4.90–$8.96 unit costs, the importer can stock 100+ units with negligible working capital exposure, providing immediate cash flow while higher-ticket collision parts turnover.

---

## 4. Sensitivity Analysis & Recommendation Robustness

We tested four distinct weighting scenarios in [`notebooks/04_analysis_and_scoring.ipynb`](../notebooks/04_analysis_and_scoring.ipynb):
1. **Original Model** (30% Demand, 25% Scarcity, 20% Fitment, 15% Sourcing, 10% Confidence)
2. **Scarcity-First Model** (25% Demand, 30% Scarcity, 20% Fitment, 15% Sourcing, 10% Confidence)
3. **Equal-Weights Model** (20% each across all 5 factors)
4. **Evidence-Focused Model** (25% Demand, 20% Scarcity, 20% Fitment, 15% Sourcing, 20% Confidence)

### Key Stability Findings:
* **BYD Seagull Side Mirror** maintained **Rank #1 across all 4 scenarios** (Scores: 4.75, 4.70, 4.80, 4.80).
* **Toyota bZ4X Shock Absorber** maintained **Rank #2 across all 4 scenarios** (Scores: 4.60, 4.55, 4.60, 4.65).
* **Toyota bZ4X Brake Pads** and **BYD Yuan Up Side Mirror** remained inside the **Top 5 across all 4 scenarios**.
* The overall recommendation has **80% to 100% stability**, demonstrating that our top-priority list is robust against subjective weighting shifts.

---

## 5. Strategic Import Guidance for the Client

1. **Initial Procurement Split**:
   * **60% Fast-Moving Consumables**: BYD Seagull/Yuan Up brake pads and cabin-air filters (immediate turnover, low risk, low capital).
   * **40% High-Margin Urban Collision & Suspension Assemblies**: BYD Seagull side mirrors, Yuan Up side mirrors, and Toyota bZ4X shock absorbers.
2. **Freight Optimization**:
   * Consumables (pads, filters, mirrors) should be air-freighted or grouped in LCL (Less-than-Container Load) air crates for quick initial market entry.
   * Large body panels and bumper fascias (fenders, bumpers) should be deferred to full 20ft/40ft sea container shipments due to high volumetric air-freight penalties.
