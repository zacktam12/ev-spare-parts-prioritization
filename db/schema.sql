-- ==============================================================================
-- Schema: EV Spare-Parts Prioritization Decision Framework
-- Target Market: Addis Ababa, Ethiopia
-- Assessment: iCog Labs Technical Assignment
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. Source Provenance Registry
CREATE TABLE IF NOT EXISTS sources (
    source_id           TEXT PRIMARY KEY,
    source_name         TEXT NOT NULL,
    source_url          TEXT NOT NULL,
    source_type         TEXT NOT NULL CHECK (source_type IN
                          ('marketplace', 'distributor_catalogue', 'supplier_catalogue', 'trade_directory', 'regulator', 'benchmark')),
    market_scope        TEXT NOT NULL CHECK (market_scope IN ('Ethiopia', 'Regional', 'Global', 'China', 'US')),
    collection_date     DATE NOT NULL,
    notes               TEXT
);

-- 2. Vehicle Candidate Registry
CREATE TABLE IF NOT EXISTS vehicle_models (
    vehicle_id          TEXT PRIMARY KEY,
    make                TEXT NOT NULL,
    model               TEXT NOT NULL,
    category            TEXT NOT NULL,
    adey_listings       INTEGER NOT NULL DEFAULT 0,
    selection_status    TEXT NOT NULL CHECK (selection_status IN ('SELECTED', 'EXCLUDED')),
    rationale           TEXT NOT NULL
);

-- 3. Spare-Part Taxonomy (10 Functional Categories)
CREATE TABLE IF NOT EXISTS part_categories (
    category_id         TEXT PRIMARY KEY,
    category_name       TEXT NOT NULL UNIQUE,
    wear_classification TEXT NOT NULL CHECK (wear_classification IN ('wear_item', 'collision_repair', 'body_exterior', 'lighting', 'suspension')),
    logistics_tier      TEXT NOT NULL CHECK (logistics_tier IN ('Phase_1_Air_FastTurn', 'Phase_2_Ocean_HeavyStock'))
);

-- 4. Cleaned Empirical Observations (59 Sourced Records)
CREATE TABLE IF NOT EXISTS observations (
    observation_id          TEXT PRIMARY KEY,
    vehicle                 TEXT NOT NULL REFERENCES vehicle_models(vehicle_id),
    model_year              TEXT,
    part_category           TEXT NOT NULL REFERENCES part_categories(category_id),
    part_description        TEXT NOT NULL,
    oem_part_number         TEXT,
    supplier                TEXT NOT NULL,
    price                   REAL,
    currency                TEXT,
    availability            TEXT,
    price_status            TEXT NOT NULL,
    stock_status            TEXT,
    compatibility_statement TEXT,
    source_id               TEXT NOT NULL REFERENCES sources(source_id),
    source_url              TEXT,
    collection_date         DATE NOT NULL,
    evidence_type           TEXT NOT NULL,
    notes                   TEXT,
    observation_type        TEXT NOT NULL CHECK (observation_type IN
                              ('supplier_catalogue', 'catalogue_gap', 'trade_quotation_unverified', 'safety_context')),
    price_usd               REAL,
    price_missing           BOOLEAN NOT NULL CHECK (price_missing IN (0, 1, 'True', 'False')),
    is_cross_checked        BOOLEAN NOT NULL CHECK (is_cross_checked IN (0, 1, 'True', 'False')),
    compatibility_strength  TEXT NOT NULL
);

-- 5. Multi-Factor Scoring Matrix (30 Evaluated Combinations)
CREATE TABLE IF NOT EXISTS scoring_results (
    vehicle                 TEXT NOT NULL REFERENCES vehicle_models(vehicle_id),
    part_category           TEXT NOT NULL REFERENCES part_categories(category_id),
    demand_evidence         INTEGER NOT NULL CHECK (demand_evidence BETWEEN 1 AND 5),
    market_scarcity         INTEGER NOT NULL CHECK (market_scarcity BETWEEN 1 AND 5),
    vehicle_compatibility   INTEGER NOT NULL CHECK (vehicle_compatibility BETWEEN 1 AND 5),
    sourcing_practicality   INTEGER NOT NULL CHECK (sourcing_practicality BETWEEN 1 AND 5),
    evidence_confidence     INTEGER NOT NULL CHECK (evidence_confidence BETWEEN 1 AND 5),
    score_justification     TEXT NOT NULL,
    priority_score          REAL NOT NULL,
    score_Original          REAL NOT NULL,
    score_Scarcity_first    REAL NOT NULL,
    score_Equal_weights     REAL NOT NULL,
    score_Evidence_focused  REAL NOT NULL,
    rank                    INTEGER NOT NULL,
    p_top5_monte_carlo      REAL,
    PRIMARY KEY (vehicle, part_category)
);

-- 6. Performance Indexes for Rapid Querying
CREATE INDEX IF NOT EXISTS idx_obs_vehicle ON observations(vehicle);
CREATE INDEX IF NOT EXISTS idx_obs_category ON observations(part_category);
CREATE INDEX IF NOT EXISTS idx_obs_source ON observations(source_id);
CREATE INDEX IF NOT EXISTS idx_scoring_rank ON scoring_results(rank);
