"""Data-integrity contract for the EV spare-parts evidence dataset.

These tests assert the documented properties of the datasets (row counts,
source-registry integrity, evidence classification, and recommendation set).
They are the executable form of the claims made in README.md and
reports/comprehensive_project_report.md.
"""

from __future__ import annotations

import json

import pytest

EXPECTED_VEHICLES = {"BYD Seagull", "BYD Yuan Up", "Toyota bZ4X"}
EXPECTED_CATEGORIES = {
    "Brake pads", "Brake discs", "Cabin-air filter", "Wiper blades",
    "Headlight assembly", "Tail-light assembly", "Side mirror", "Bumper",
    "Fender / body panel", "Shock absorber",
}
EXPECTED_TOP5 = {
    ("BYD Seagull", "Side mirror"),
    ("BYD Seagull", "Brake pads"),
    ("BYD Seagull", "Shock absorber"),
    ("BYD Seagull", "Bumper"),
    ("BYD Seagull", "Headlight assembly"),
}
EXPECTED_OBSERVATION_TYPE_COUNTS = {
    "supplier_catalogue": 45,
    "catalogue_gap": 8,
    "trade_quotation_unverified": 4,
    "safety_context": 2,
}


# ---------------------------------------------------------------------------
# Source registry
# ---------------------------------------------------------------------------
def test_source_log_has_eight_documented_sources(source_log):
    assert len(source_log) == 8
    assert set(source_log["source_id"]) == {f"S{i:03d}" for i in range(1, 9)}


def test_every_source_has_url_and_date(source_log):
    assert source_log["url"].notna().all()
    assert source_log["collection_date"].notna().all()


# ---------------------------------------------------------------------------
# Raw observations
# ---------------------------------------------------------------------------
def test_raw_has_59_rows_and_19_columns(raw_df):
    assert raw_df.shape == (59, 19)


def test_raw_column_names_are_clean(raw_df):
    """No leading/trailing whitespace in column headers (regression guard)."""
    for column in raw_df.columns:
        assert column == column.strip(), f"dirty header: {column!r}"
        assert "  " not in column, f"padded header: {column!r}"


def test_raw_observation_type_breakdown(raw_df):
    counts = raw_df["observation_type"].value_counts().to_dict()
    assert counts == EXPECTED_OBSERVATION_TYPE_COUNTS


def test_raw_source_ids_exist_in_source_log(raw_df, source_log):
    documented = set(source_log["source_id"])
    assert set(raw_df["source_id"]).issubset(documented)


def test_raw_vehicles_and_categories_are_known(raw_df):
    assert set(raw_df["vehicle"]) == EXPECTED_VEHICLES
    assert set(raw_df["part_category"]).issubset(EXPECTED_CATEGORIES)


def test_catalogue_gaps_carry_no_price(raw_df):
    gaps = raw_df[raw_df["observation_type"] == "catalogue_gap"]
    assert len(gaps) == 8
    # Gaps are honest negatives: they must never carry a price.
    assert gaps["price"].isna().all()


def test_yuan_up_has_no_verified_catalogue_listing(raw_df):
    yuan_up = raw_df[raw_df["vehicle"] == "BYD Yuan Up"]
    assert len(yuan_up) == 10
    # Landin (S003) carries zero Yuan Up listings, so no row may claim a verified
    # supplier-catalogue listing. Only honest negatives and unverified quotes remain.
    assert "supplier_catalogue" not in set(yuan_up["observation_type"])
    assert set(yuan_up["observation_type"]) == {
        "catalogue_gap", "trade_quotation_unverified"}


def test_yuan_up_trade_quotations_are_labelled_s008(raw_df):
    yuan_up = raw_df[raw_df["vehicle"] == "BYD Yuan Up"]
    quotes = yuan_up[yuan_up["observation_type"] == "trade_quotation_unverified"]
    assert len(quotes) == 4
    assert set(quotes["source_id"]) == {"S008"}


def test_nhtsa_rows_are_classified_as_safety_context_only(raw_df, source_log):
    nhtsa = raw_df[raw_df["observation_type"] == "safety_context"]
    assert len(nhtsa) == 2
    assert set(nhtsa["source_id"]) == {"S006"}
    assert set(nhtsa["vehicle"]) == {"Toyota bZ4X"}


# ---------------------------------------------------------------------------
# Cleaned observations
# ---------------------------------------------------------------------------
def test_cleaned_has_59_rows_and_23_columns(cleaned_df):
    assert cleaned_df.shape == (59, 23)


def test_cleaned_column_names_are_snake_case(cleaned_df):
    for column in cleaned_df.columns:
        assert column == column.strip()
        assert " " not in column, f"non-snake_case column: {column!r}"


def test_cleaned_preserves_one_to_one_observation_ids(raw_df, cleaned_df):
    assert set(raw_df["observation_id"]) == set(cleaned_df["observation_id"])


def test_cleaned_price_missing_flag_is_boolean_like(cleaned_df):
    values = set(cleaned_df["price_missing"].astype(str).str.strip())
    assert values.issubset({"True", "False"})


# ---------------------------------------------------------------------------
# Scoring matrix
# ---------------------------------------------------------------------------
def test_scoring_matrix_has_30_unique_combinations(scoring_df):
    assert len(scoring_df) == 30
    combos = set(zip(scoring_df["vehicle"], scoring_df["part_category"]))
    assert len(combos) == 30
    assert set(scoring_df["vehicle"]) == EXPECTED_VEHICLES
    assert set(scoring_df["part_category"]) == EXPECTED_CATEGORIES


def test_all_five_factors_are_in_range(scoring_df):
    factors = ["demand_evidence", "market_scarcity", "vehicle_compatibility",
               "sourcing_practicality", "evidence_confidence"]
    for factor in factors:
        assert scoring_df[factor].between(1, 5).all(), factor


def test_priority_scores_are_within_bounds(scoring_df):
    assert scoring_df["priority_score"].between(0, 5).all()


def test_ranks_are_a_unique_one_to_thirty_permutation(scoring_df):
    assert sorted(scoring_df["rank"]) == list(range(1, 31))


def test_top5_recommendations_are_all_byd_seagull(scoring_df):
    top5 = scoring_df.nsmallest(5, "rank")
    assert set(zip(top5["vehicle"], top5["part_category"])) == EXPECTED_TOP5


def test_scoring_results_columns_are_snake_case(scoring_df):
    for column in scoring_df.columns:
        assert " " not in column, f"non-snake_case column: {column!r}"


def test_every_row_has_a_score_justification(scoring_df):
    assert scoring_df["score_justification"].astype(str).str.len().gt(20).all()


# ---------------------------------------------------------------------------
# Notebooks
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("notebook", [
    "01_vehicle_selection.ipynb",
    "02_data_collection.ipynb",
    "03_data_cleaning.ipynb",
    "04_analysis_and_scoring.ipynb",
])
def test_notebook_exists_and_executed_cleanly(repo_root, notebook):
    path = repo_root / "notebooks" / notebook
    assert path.exists(), f"missing notebook: {notebook}"
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = [
        output
        for cell in data.get("cells", [])
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    assert not errors, f"{notebook} contains {len(errors)} error output(s)"
