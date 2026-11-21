"""Behavioural tests for the authoritative scoring engine.

These tests lock in the analytical contract: the weighted formula, the exact
factor weights, the 30-row matrix, the 4-scenario sensitivity analysis, and the
documented Top-5 result. They also verify that the committed
data/scoring_results.csv is byte-for-byte consistent with the engine output.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

FACTOR_COLUMNS = [
    "demand_evidence",
    "market_scarcity",
    "vehicle_compatibility",
    "sourcing_practicality",
    "evidence_confidence",
]


def _weighted(df: pd.DataFrame, weights: dict[str, float]) -> pd.Series:
    return (
        weights["demand_evidence"] * df["demand_evidence"]
        + weights["market_scarcity"] * df["market_scarcity"]
        + weights["vehicle_compatibility"] * df["vehicle_compatibility"]
        + weights["sourcing_practicality"] * df["sourcing_practicality"]
        + weights["evidence_confidence"] * df["evidence_confidence"]
    )


def test_baseline_weights_match_documented_formula(scoring_module):
    w = scoring_module.WEIGHTS["Original"]
    assert w == {
        "demand_evidence": 0.30,
        "market_scarcity": 0.25,
        "vehicle_compatibility": 0.20,
        "sourcing_practicality": 0.15,
        "evidence_confidence": 0.10,
    }


def test_four_scenarios_are_defined_and_sum_to_one(scoring_module):
    assert set(scoring_module.WEIGHTS) == {
        "Original", "Scarcity-first", "Equal weights", "Evidence-focused"}
    for name, weights in scoring_module.WEIGHTS.items():
        assert abs(sum(weights.values()) - 1.0) < 1e-9, name


def test_calculate_scores_returns_thirty_rows(scoring_module):
    result = scoring_module.calculate_scores()
    assert len(result) == 30
    assert result["rank"].tolist() == list(range(1, 31))


def test_priority_score_equals_weighted_formula(scoring_module):
    df = scoring_module.calculate_scores()
    expected = _weighted(df, scoring_module.WEIGHTS["Original"])
    assert np.allclose(df["priority_score"], expected, atol=1e-9)


def test_committed_csv_matches_engine_output(scoring_module, scoring_df):
    """The on-disk scoring_results.csv must match a fresh engine run."""
    fresh = scoring_module.calculate_scores()
    merged = scoring_df.merge(
        fresh, on=["vehicle", "part_category"], suffixes=("_csv", "_engine"))
    assert len(merged) == 30
    assert np.allclose(merged["priority_score_csv"], merged["priority_score_engine"], atol=1e-9)
    for factor in FACTOR_COLUMNS:
        assert (merged[f"{factor}_csv"] == merged[f"{factor}_engine"]).all(), factor


def test_rank_order_is_monotonic_non_increasing(scoring_module):
    df = scoring_module.calculate_scores().sort_values("rank")
    scores = df["priority_score"].to_numpy()
    assert np.all(np.diff(scores) <= 1e-9)


def test_top_recommendation_is_byd_seagull_side_mirror(scoring_module):
    df = scoring_module.calculate_scores()
    top = df.sort_values("rank").iloc[0]
    assert (top["vehicle"], top["part_category"]) == ("BYD Seagull", "Side mirror")
    assert abs(top["priority_score"] - 4.60) < 0.005


def test_toyota_bz4x_shock_absorber_is_rank_8(scoring_module):
    df = scoring_module.calculate_scores()
    row = df[(df["vehicle"] == "Toyota bZ4X") & (df["part_category"] == "Shock absorber")]
    assert len(row) == 1
    assert int(row.iloc[0]["rank"]) == 8
    assert abs(row.iloc[0]["priority_score"] - 3.90) < 0.005


def test_per_vehicle_mean_scores_match_report(scoring_module):
    df = scoring_module.calculate_scores()
    means = df.groupby("vehicle")["priority_score"].mean()
    assert abs(means["BYD Seagull"] - 3.955) < 0.01
    assert abs(means["BYD Yuan Up"] - 2.860) < 0.01
    assert abs(means["Toyota bZ4X"] - 3.610) < 0.01


def test_scenario_columns_present_and_bounded(scoring_module, scoring_df):
    expected_columns = {
        "score_Original",
        "score_Scarcity_first",
        "score_Equal_weights",
        "score_Evidence_focused",
    }
    assert expected_columns.issubset(scoring_df.columns)
    for column in expected_columns:
        assert scoring_df[column].between(0, 5).all(), column


def test_equal_weights_scenario_uses_five_times_twenty_percent(scoring_module, scoring_df):
    equal = 0.2 * scoring_df[FACTOR_COLUMNS].sum(axis=1)
    assert np.allclose(scoring_df["score_Equal_weights"], equal, atol=1e-9)


def test_sensitivity_analysis_reports_full_top5_stability(scoring_module):
    df = scoring_module.calculate_scores()
    _, stability = scoring_module.run_sensitivity_analysis(df)
    assert set(stability) == {
        "Original", "Scarcity-first", "Equal weights", "Evidence-focused"}
    for name, info in stability.items():
        assert info["overlap"] == 5, name
        assert info["stability_pct"] == 100.0, name


def test_sensitivity_table_has_five_ranks(scoring_module):
    df = scoring_module.calculate_scores()
    sens_df, _ = scoring_module.run_sensitivity_analysis(df)
    assert sens_df.shape == (5, 4)
    assert list(sens_df.index) == [f"Rank {i}" for i in range(1, 6)]


# ---------------------------------------------------------------------------
# Monte-Carlo robustness (Dirichlet weight draws)
# ---------------------------------------------------------------------------
def test_monte_carlo_returns_all_thirty_combinations(scoring_module):
    mc, _ = scoring_module.run_monte_carlo()
    assert len(mc) == 30
    assert mc["p_top5"].between(0.0, 1.0).all()
    # Every draw elects exactly MC_TOP_N winners, so inclusion probabilities sum to N.
    assert abs(mc["p_top5"].sum() - scoring_module.MC_TOP_N) < 1e-9


def test_monte_carlo_is_deterministic_for_a_fixed_seed(scoring_module):
    first, _ = scoring_module.run_monte_carlo()
    second, _ = scoring_module.run_monte_carlo()
    pd.testing.assert_frame_equal(first, second)


def test_monte_carlo_top_four_recommendations_are_robust(scoring_module):
    """Robustness finding: the top 4 hold; only the 5th slot is contested."""
    mc, _ = scoring_module.run_monte_carlo()
    baseline = mc[mc["rank"] <= scoring_module.MC_TOP_N]
    assert (baseline["p_top5"] >= 0.80).sum() == 4


def test_monte_carlo_summary_reports_contested_fifth_slot(scoring_module):
    _, summary = scoring_module.run_monte_carlo()
    assert summary["n_sim"] == scoring_module.N_MONTE_CARLO
    assert summary["seed"] == scoring_module.MC_SEED
    assert summary["baseline_top5_all_robust"] is False
    assert 0.40 <= summary["baseline_top5_min_p"] <= 0.50
    assert summary["n_combinations_ever_top5"] >= scoring_module.MC_TOP_N


# ---------------------------------------------------------------------------
# One-way factor-dropout robustness (addresses the unverified Scarcity input)
# ---------------------------------------------------------------------------
def test_factor_dropout_tests_every_factor(scoring_module):
    dropout_df, _ = scoring_module.run_factor_dropout()
    assert list(dropout_df.index) == scoring_module.FACTOR_COLUMNS
    assert len(dropout_df) == len(scoring_module.FACTOR_COLUMNS)


def test_factor_dropout_is_deterministic(scoring_module):
    first, _ = scoring_module.run_factor_dropout()
    second, _ = scoring_module.run_factor_dropout()
    pd.testing.assert_frame_equal(first, second)


def test_removing_scarcity_preserves_the_top_five(scoring_module):
    """The recommendation must not hinge on the unverified Gezat S002 review."""
    dropout_df, summary = scoring_module.run_factor_dropout()
    assert int(dropout_df.loc["market_scarcity", "overlap"]) == scoring_module.MC_TOP_N
    assert summary["scarcity_dropout_overlap"] == scoring_module.MC_TOP_N


def test_factor_dropout_only_demand_is_load_bearing(scoring_module):
    """Dropping any single factor keeps at least 4 of 5; only Demand moves the set."""
    dropout_df, summary = scoring_module.run_factor_dropout()
    assert summary["min_overlap"] == scoring_module.MC_TOP_N - 1
    below_full = dropout_df[dropout_df["overlap"] < scoring_module.MC_TOP_N]
    assert list(below_full.index) == ["demand_evidence"]


def test_committed_factor_dropout_csv_matches_engine_output(scoring_module, factor_dropout_csv):
    fresh, _ = scoring_module.run_factor_dropout()
    assert list(factor_dropout_csv.index) == list(fresh.index)
    assert (factor_dropout_csv["overlap"] == fresh["overlap"]).all()
    assert np.allclose(
        factor_dropout_csv["stability_pct"], fresh["stability_pct"], atol=1e-9)
