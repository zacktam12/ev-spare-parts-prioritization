"""
generate_scores.py
------------------
Authoritative alias forwarding directly to generate_scores_defensible.py.
Ensures backwards compatibility with any legacy imports.
"""

from scrapper.generate_scores_defensible import (
    get_scoring_data,
    calculate_scores,
    run_sensitivity_analysis,
    WEIGHTS
)

if __name__ == "__main__":
    df = calculate_scores()
    print(f"Generated {len(df)} defensible scores via generate_scores.py alias.")
