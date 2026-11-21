#!/usr/bin/env python
"""
run_pipeline.py
---------------
Single-command orchestrator for the EV Spare-Parts Prioritization pipeline.

Runs every stage from the repository root so relative data paths resolve
consistently, and fails loudly (non-zero exit) if any stage fails.

Usage
-----
    python run_pipeline.py                # raw data -> scores -> figures -> deck
    python run_pipeline.py --test         # pipeline, then the pytest validation suite
    python run_pipeline.py --notebooks    # pipeline, then re-execute the 4 notebooks
    python run_pipeline.py --list         # list the stages and exit

Stage order
-----------
1. Rebuild the defensible raw observation dataset (59 rows).
2. Apply provenance corrections and normalise column headers.
3. Compute the 30-row priority scoring matrix and 4-scenario sensitivity analysis.
4. Export publication figures to reports/figures/.
5. Generate the 12-slide PowerPoint presentation.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (stage label, script path relative to ROOT, human description)
STAGES: list[tuple[str, str, str]] = [
    ("raw", "scraper/compile_raw_observations_defensible.py",
     "Rebuild the defensible raw observation dataset (59 rows)"),
    ("repair", "scraper/repair_raw_observations.py",
     "Apply provenance corrections and normalise column headers"),
    ("scores", "scraper/generate_scores_defensible.py",
     "Compute the 30-row scoring matrix and sensitivity analysis"),
    ("figures", "scraper/export_figures.py",
     "Export 300 DPI publication figures"),
    ("presentation", "scraper/generate_presentation.py",
     "Generate the 12-slide PowerPoint presentation"),
]

NOTEBOOKS: list[str] = [
    "notebooks/01_vehicle_selection.ipynb",
    "notebooks/02_data_collection.ipynb",
    "notebooks/03_data_cleaning.ipynb",
    "notebooks/04_analysis_and_scoring.ipynb",
]


def _banner(text: str) -> None:
    print("\n" + "=" * 78)
    print(text)
    print("=" * 78, flush=True)


def run_command(argv: list[str], description: str) -> None:
    """Run a subprocess from the repository root, aborting on failure."""
    _banner(f">>> {description}\n    $ {' '.join(argv)}")
    started = time.perf_counter()
    proc = subprocess.run(argv, cwd=ROOT)
    elapsed = time.perf_counter() - started
    if proc.returncode != 0:
        print(f"\n[FAIL] {description} exited with code {proc.returncode} "
              f"after {elapsed:.1f}s", file=sys.stderr)
        raise SystemExit(proc.returncode)
    print(f"[OK] {description} ({elapsed:.1f}s)")


def run_stages(selected: list[str] | None = None) -> None:
    stages = STAGES
    if selected:
        wanted = set(selected)
        stages = [s for s in STAGES if s[0] in wanted]
        unknown = wanted - {s[0] for s in STAGES}
        if unknown:
            raise SystemExit(f"Unknown stage(s): {', '.join(sorted(unknown))}")

    for label, script, description in stages:
        run_command([sys.executable, script], f"[{label}] {description}")


def run_notebooks() -> None:
    for nb in NOTEBOOKS:
        run_command(
            [sys.executable, "-m", "jupyter", "nbconvert",
             "--to", "notebook", "--execute", "--inplace", nb],
            f"[notebook] Execute {nb}",
        )


def run_tests() -> None:
    run_command([sys.executable, "-m", "pytest"], "[test] pytest validation suite")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the end-to-end EV spare-parts prioritization pipeline.",
    )
    parser.add_argument("--test", action="store_true",
                        help="Run the pytest validation suite after the pipeline.")
    parser.add_argument("--notebooks", action="store_true",
                        help="Re-execute all Jupyter notebooks after the pipeline.")
    parser.add_argument("--only", nargs="+", metavar="STAGE",
                        help="Run only the named stage(s): " +
                             ", ".join(s[0] for s in STAGES))
    parser.add_argument("--list", action="store_true",
                        help="List the pipeline stages and exit.")
    args = parser.parse_args()

    if args.list:
        print("Pipeline stages (run in this order):")
        for i, (label, script, description) in enumerate(STAGES, start=1):
            print(f"  {i}. [{label}] {description}\n      -> {script}")
        return

    started = time.perf_counter()
    run_stages(selected=args.only)

    if args.notebooks:
        run_notebooks()
    if args.test:
        run_tests()

    _banner(f"PIPELINE COMPLETE in {time.perf_counter() - started:.1f}s")


if __name__ == "__main__":
    main()
