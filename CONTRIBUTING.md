# Contributing

Thanks for your interest in this project. This repository is an analytical
decision-support pipeline, so the most important contribution rule is
**evidential honesty**: every number must be traceable to a documented source.

## Environment setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Requires Python >= 3.11 (developed and verified on Python 3.14).

## Running the pipeline

The recommended entry point is the orchestrator, which runs every stage from the
repository root and fails loudly if any stage fails:

```powershell
python run_pipeline.py            # raw data -> scores -> figures -> presentation
python run_pipeline.py --test     # same, then run the validation suite
python run_pipeline.py --list     # show the stages without running them
```

Individual stages can also be run directly (see `Makefile` or `README.md`).

## Running the tests

```powershell
python -m pytest            # full validation suite
python -m pytest -v         # verbose
python -m pytest --cov=scraper --cov-report=term-missing
```

The suite in `tests/` is the executable contract for the dataset. It enforces row
counts, source-registry integrity, the scoring formula, the sensitivity scenarios,
and the SQL schema. **A change that breaks the tests is a change that breaks the
project's core claims.**

## Data-integrity rules (non-negotiable)

These rules protect the defensibility of the analysis. Do not violate them:

1. **Never invent OEM part numbers.** If a part was not verified in a named
   catalogue, it stays a `catalogue_gap`.
2. **Never zero-fill or guess missing prices.** Unpriced rows stay `price_missing = True`.
3. **Never describe `toyota-spare-parts.com` as Toyota's official EPC.** It is a
   third-party aggregator.
4. **Never attribute Yuan Up parts to Landin (`S003`).** Landin carries zero Yuan Up
   listings — this is a confirmed empirical finding.
5. **Never use NHTSA (`S006`) rows to support compatibility, confidence, or cross-check
   status.** They are `safety_context` only.
6. **Never bundle multiple SKUs at one ranking position.** One rank = one
   side-specific application.
7. **Always label demand and scarcity scores as analyst judgements.** No local
   replacement rate was measured.

## Code style

- Python: 4-space indentation, `ruff` and `black` configured for a 120-character line
  length (see `pyproject.toml`).
- Whitespace: enforced by `.editorconfig`; Python and Markdown use LF line endings.
- Keep pipeline scripts runnable from the repository root; resolve paths relative to
  the repository, not the current working directory, where practical.

## Commit conventions

Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes:

```
feat:     new capability
fix:      bug fix
docs:     documentation only
data:     dataset changes
test:     tests
chore:    tooling, dependencies, CI
```

Example: `fix: correct slide-7 per-vehicle average scores`

## Pull-request checklist

- [ ] `python -m pytest` passes.
- [ ] `python run_pipeline.py` completes without error.
- [ ] Any new number in a report/figure is reproducible from a script in `scraper/`.
- [ ] `CHANGELOG.md` updated under `Unreleased` or a new version heading.
- [ ] Data-integrity rules above were respected.
