# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-21

Engineering-hardening release: adds missing engineering standards, automated
validation, and rubric-alignment artifacts. The analytical model, factor scores,
and recommendations are unchanged from v1.0.0.

### Added
- `pyproject.toml` (build metadata + pytest/coverage/ruff/black configuration).
- `.editorconfig`, `Makefile`, and `run_pipeline.py` (one-command reproducible pipeline).
- `CONTRIBUTING.md`, `CHANGELOG.md`, and an MIT `LICENSE`.
- `tests/` — a pytest data-integrity/validation suite (`conftest.py`, `test_data_integrity.py`,
  `test_scoring_model.py`, `test_schema.py`).
- GitHub Actions CI (`.github/workflows/ci.yml`) running the validation suite on every push.
- `RUBRIC.md` and `docs/rubric_compliance.csv` — self-assessment against the grading rubric.
- `docs/data_dictionary.md` — column-level documentation for every dataset.
- `AGENT_HANDOFF.md` — technical architecture, data flow, and hard invariants for AI agents.
- `reports/presentation.md` — presentation script with speaker notes and defense Q&A.

### Changed
- Renamed the pipeline directory `scrapper/` -> `scraper/` everywhere in the repository.
- `data/scoring_results.csv` sensitivity columns renamed to snake_case
  (`score_Scarcity_first`, `score_Equal_weights`, `score_Evidence_focused`) to match `db/schema.sql`.
- `run_pipeline.py` and the report's execution order now include raw-dataset regeneration.
- `db/schema.sql` `scoring_results` now exactly mirrors `data/scoring_results.csv` (14 columns).

### Fixed
- Added the missing `python-pptx` dependency (used by `scraper/generate_presentation.py`).
- Corrected the per-vehicle average scores quoted on presentation slide 7
  (BYD Seagull 3.96, Toyota bZ4X 3.61) to match `data/scoring_results.csv`.
- Corrected the dataset dimensions quoted on presentation slide 5
  (raw 59x19, cleaned 59x23) to match the actual files.
- Corrected stale repository paths in `reports/comprehensive_project_report.md`.
- `scraper/repair_raw_observations.py` now strips stray whitespace from column headers and
  writes deterministic output.

### Removed
- Relocated the untracked `data/ev_parts.db` binary to `refer/legacy/db_reference/`;
  `db/schema.sql` is the single source of truth for the relational schema.
- Dropped the dead `p_top5_monte_carlo` column from `db/schema.sql` — no pipeline stage
  populated it, and the project reports deterministic sensitivity stability, not Monte Carlo.
- Relocated the orphan `reports/figures/monte_carlo_stability.png` to `refer/legacy/`
  (not produced by any pipeline stage and not referenced by any deliverable).

## [1.0.0] - 2026-11-19

Initial post-audit release.

### Added
- 3 vehicles x 10 categories = 30-combination priority scoring matrix
  (`Priority Score = 0.30·D + 0.25·S + 0.20·C + 0.15·P + 0.10·E`).
- 59-row evidence dataset across 8 sources (`S001`–`S008`) with `observation_type` classification.
- 4-scenario sensitivity analysis with 100.0% Top-5 set stability.
- `reports/findings.md`, `reports/limitations.md`, `reports/comprehensive_project_report.md`.
- 300 DPI figures and a 12-slide PowerPoint presentation with speaker notes.
- `REUSE.md` documenting reference-repository attribution.
