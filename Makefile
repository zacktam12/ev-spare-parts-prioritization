# EV Spare-Parts Prioritization — task shortcuts.
# Windows users without GNU make can run the same steps via `python run_pipeline.py`.

PYTHON ?= python
VENV   ?= .venv

.DEFAULT_GOAL := help
.PHONY: help setup pipeline raw scores figures deck notebooks test coverage lint format clean all

help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## Create the virtual environment and install dependencies.
	$(PYTHON) -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

pipeline: raw scores figures deck ## Run the full pipeline end-to-end.

raw: ## Rebuild data/raw/raw_observations.csv (59 rows).
	$(PYTHON) scraper/compile_raw_observations_defensible.py
	$(PYTHON) scraper/repair_raw_observations.py

scores: ## Recompute data/scoring_results.csv (30 rows) and sensitivity analysis.
	$(PYTHON) scraper/generate_scores_defensible.py

figures: ## Regenerate reports/figures/*.png at 300 DPI.
	$(PYTHON) scraper/export_figures.py

deck: ## Regenerate reports/EV_Spare_Parts_Prioritization_Presentation.pptx.
	$(PYTHON) scraper/generate_presentation.py

notebooks: ## Execute all four notebooks in place.
	$(PYTHON) -m jupyter nbconvert --to notebook --execute --inplace notebooks/01_vehicle_selection.ipynb
	$(PYTHON) -m jupyter nbconvert --to notebook --execute --inplace notebooks/02_data_collection.ipynb
	$(PYTHON) -m jupyter nbconvert --to notebook --execute --inplace notebooks/03_data_cleaning.ipynb
	$(PYTHON) -m jupyter nbconvert --to notebook --execute --inplace notebooks/04_analysis_and_scoring.ipynb

test: ## Run the pytest validation suite.
	$(PYTHON) -m pytest

coverage: ## Run the validation suite with a coverage report.
	$(PYTHON) -m pytest --cov=scraper --cov-report=term-missing

lint: ## Lint the codebase with ruff.
	$(PYTHON) -m ruff check .

format: ## Format the codebase with black.
	$(PYTHON) -m black .

clean: ## Remove caches and transient build artefacts.
	-$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
	-$(PYTHON) -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.ruff_cache', 'htmlcov']]"
	-$(PYTHON) -c "import pathlib; [p.unlink() for p in ['.coverage'] if pathlib.Path(p).exists()]"

all: pipeline test ## Run the pipeline and the tests.
