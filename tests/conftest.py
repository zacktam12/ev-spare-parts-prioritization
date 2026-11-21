"""Shared pytest fixtures and path constants for the validation suite."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def _load_module(name: str, relpath: str):
    """Import a standalone pipeline script by file path."""
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"Could not load module {name} from {relpath}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def scoring_module():
    """The authoritative scoring engine (WEIGHTS, calculate_scores, sensitivity)."""
    return _load_module("generate_scores_defensible", "scraper/generate_scores_defensible.py")


@pytest.fixture(scope="session")
def raw_df() -> pd.DataFrame:
    return pd.read_csv(DATA / "raw" / "raw_observations.csv")


@pytest.fixture(scope="session")
def cleaned_df() -> pd.DataFrame:
    return pd.read_csv(DATA / "cleaned" / "cleaned_observations.csv")


@pytest.fixture(scope="session")
def source_log() -> pd.DataFrame:
    return pd.read_csv(DATA / "source_log.csv")


@pytest.fixture(scope="session")
def scoring_df() -> pd.DataFrame:
    return pd.read_csv(DATA / "scoring_results.csv")
