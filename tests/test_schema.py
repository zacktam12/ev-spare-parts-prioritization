"""Validation tests for the SQLite relational schema (db/schema.sql).

The schema is a deliverable in its own right, so these tests prove that it
executes cleanly, creates the expected tables and indexes, is idempotent, and
actually enforces its CHECK constraints.
"""

from __future__ import annotations

import sqlite3

import pytest

EXPECTED_TABLES = {
    "sources",
    "vehicle_models",
    "part_categories",
    "observations",
    "scoring_results",
}
EXPECTED_INDEXES = {
    "idx_obs_vehicle",
    "idx_obs_category",
    "idx_obs_source",
    "idx_scoring_rank",
}


@pytest.fixture()
def schema_sql(repo_root) -> str:
    return (repo_root / "db" / "schema.sql").read_text(encoding="utf-8")


@pytest.fixture()
def conn(schema_sql) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.executescript(schema_sql)
    yield connection
    connection.close()


def _object_names(conn: sqlite3.Connection, kind: str) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = ?", (kind,)
    ).fetchall()
    return {name for (name,) in rows}


def test_schema_creates_all_tables(conn):
    assert EXPECTED_TABLES.issubset(_object_names(conn, "table"))


def test_schema_creates_all_indexes(conn):
    assert EXPECTED_INDEXES.issubset(_object_names(conn, "index"))


def test_schema_is_idempotent(schema_sql):
    connection = sqlite3.connect(":memory:")
    connection.executescript(schema_sql)
    connection.executescript(schema_sql)  # must not raise
    assert EXPECTED_TABLES.issubset(_object_names(connection, "table"))
    connection.close()


def test_foreign_keys_are_enabled_by_schema(conn):
    enabled = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    assert enabled == 1


def test_observations_has_expected_column_count(conn):
    columns = conn.execute("PRAGMA table_info(observations)").fetchall()
    assert len(columns) == 23


def test_scoring_results_has_expected_column_count(conn):
    columns = conn.execute("PRAGMA table_info(scoring_results)").fetchall()
    assert len(columns) == 14


def test_invalid_observation_type_is_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO observations "
            "(observation_id, vehicle, part_category, part_description, supplier, "
            " price_status, source_id, collection_date, evidence_type, "
            " observation_type, price_missing, is_cross_checked, compatibility_strength) "
            "VALUES ('X1','V','C','d','s','Priced','S001','2026-11-18','t',"
            "        'NOT_A_TYPE', 1, 1, 'weak')"
        )


def test_out_of_range_factor_is_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO scoring_results "
            "(vehicle, part_category, demand_evidence, market_scarcity, "
            " vehicle_compatibility, sourcing_practicality, evidence_confidence, "
            " score_justification, priority_score, score_Original, "
            " score_Scarcity_first, score_Equal_weights, score_Evidence_focused, rank) "
            "VALUES ('V','C', 9, 3, 3, 3, 3, 'x', 3.0, 3.0, 3.0, 3.0, 3.0, 1)"
        )


def test_invalid_source_type_is_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO sources (source_id, source_name, source_url, source_type, "
            "market_scope, collection_date) "
            "VALUES ('S999','n','u','not_a_type','Global','2026-11-18')"
        )
