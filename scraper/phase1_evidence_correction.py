"""
phase1_evidence_correction.py
-----------------------------
Phase 1 (evidence & data correction) — surgical, idempotent corrections applied to
BOTH the raw and cleaned observation datasets.

Corrections
===========
1. STOCK vs PRICE DECOUPLING (Problem 1)
   A visible price does NOT prove physical stock. The single conflated `availability`
   column is split into three concerns:
     * availability  -> catalogue/listing presence only
                        ('listed_in_catalogue', 'not_listed', 'not_verifiable',
                         'unverified_quotation', 'not_applicable')
     * price_status  -> price visibility ('Priced' / 'Price on request' / 'Not applicable')
     * stock_status  -> stock verification ('Not stated' / 'Not applicable')
   Every legacy 'in_stock' / 'price_on_request' / 'available_on_order' value is
   normalised: an entry being listed is recorded as 'listed_in_catalogue' with
   price_status capturing the price and stock_status = 'Not stated'.
   This makes the main datasets agree with scraper/outputs/landin_verified.csv,
   which already reports stock_status_verified = 'Not stated' for all Landin rows.

2. FRONT-BUMPER OE FLAG (Problem 3)
   OBS001 (Landin Front Bumper, OE EQEA-2083111) does not match the CQSW benchmark
   reference for the same component (EQEA-2803111/92). The number is NOT changed;
   it is flagged for supplier confirmation and removed from any claim of
   cross-source corroboration.

3. NON-REPRODUCIBLE LISTING COUNT (Problem 4)
   The "1,360+ listings" text in the Yuan Up catalogue-gap note is replaced with the
   reproducible count from the collected sample (36 rows in scraper/outputs/adey_cleaned.csv).

Idempotency
===========
Running this script twice produces the same result (guards on the appended note text).

Usage
=====
    python scraper/phase1_evidence_correction.py
"""

import os
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_PATH = os.path.join(ROOT, "data", "raw", "raw_observations.csv")
CLEANED_PATH = os.path.join(ROOT, "data", "cleaned", "cleaned_observations.csv")

LEGACY_STOCK_VALUES = {"in_stock", "price_on_request", "available_on_order"}

OE_FLAG_TEXT = (
    " | OE-VERIFICATION FLAG 2026-11-19: Landin lists the front bumper upper as "
    "EQEA-2083111, but the CQSW benchmark reference for this component is "
    "EQEA-2803111/92. The two references do NOT match, so this OE is NOT "
    "cross-source corroborated and is flagged for supplier confirmation before "
    "ordering. The number is intentionally left unchanged."
)
OE_FLAG_MARKER = "OE-VERIFICATION FLAG 2026-11-19"

YUANUP_COUNT_OLD = "1,360+"
YUANUP_COUNT_NEW = (
    "Upstream catalog gap. Adey sample: 36 Yuan Up listings in the collected "
    "dataset (scraper/outputs/adey_cleaned.csv) — a sampled count, not a verified "
    "marketplace total."
)


def derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise availability and (re)derive price_status / stock_status."""
    avail = df["availability"].astype(str).str.strip()
    price_present = df["price"].astype(str).str.strip().replace({"nan": "", "None": ""}) != ""

    # 1. Collapse legacy stock-implying values into catalogue presence.
    avail = avail.replace(list(LEGACY_STOCK_VALUES), "listed_in_catalogue")

    df = df.copy()
    df["availability"] = avail

    # 2. price_status: only meaningful where the row carries a supplier listing/quote.
    df["price_status"] = "Not applicable"
    listed_mask = avail.isin(["listed_in_catalogue", "unverified_quotation"])
    df.loc[listed_mask & price_present, "price_status"] = "Priced"
    df.loc[listed_mask & ~price_present, "price_status"] = "Price on request"

    # 3. stock_status: never inferred from price; 'Not stated' wherever a listing exists.
    df["stock_status"] = "Not applicable"
    df.loc[listed_mask, "stock_status"] = "Not stated"
    return df


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Place price_status and stock_status immediately after availability."""
    cols = [c for c in df.columns if c not in ("price_status", "stock_status")]
    if "availability" in cols:
        idx = cols.index("availability") + 1
        cols[idx:idx] = ["price_status", "stock_status"]
    else:
        cols += ["price_status", "stock_status"]
    return df[cols]


def apply_corrections(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)

    df = derive_columns(df)
    df = reorder_columns(df)

    # --- Problem 3: flag the front-bumper OE discrepancy (OBS001) ---
    m = df["observation_id"] == "OBS001"
    if m.any():
        note = df.loc[m, "notes"].values[0]
        if OE_FLAG_MARKER not in note:
            df.loc[m, "notes"] = note + OE_FLAG_TEXT

    # --- Problem 4: replace the non-reproducible listing count ---
    if "notes" in df.columns:
        mask_old = df["notes"].str.contains(YUANUP_COUNT_OLD, regex=False)
        df.loc[mask_old, "notes"] = df.loc[mask_old, "notes"].str.replace(
            r"(?:Upstream catalog gap\. )?High vehicle presence on Adey \(1,360\+ listings\) "
            r"contrasts with zero local parts availability\.",
            YUANUP_COUNT_NEW,
            regex=True,
        )

    df.to_csv(path, index=False)
    return df


def report(path: str, df: pd.DataFrame) -> None:
    print(f"\n=== {os.path.relpath(path, ROOT)} ===")
    print(f"rows: {len(df)}  |  columns: {len(df.columns)}")
    print("availability breakdown:")
    print(df["availability"].value_counts().to_string())
    print("price_status breakdown:")
    print(df["price_status"].value_counts().to_string())
    print("stock_status breakdown:")
    print(df["stock_status"].value_counts().to_string())
    if (df["observation_id"] == "OBS001").any():
        note = df.loc[df["observation_id"] == "OBS001", "notes"].values[0]
        print(f"OBS001 flag present: {OE_FLAG_MARKER in note}")
    stale = df["notes"].str.contains(YUANUP_COUNT_OLD, regex=False).sum() if "notes" in df.columns else 0
    print(f"rows still containing '{YUANUP_COUNT_OLD}': {stale}")


def main() -> None:
    for path in (RAW_PATH, CLEANED_PATH):
        if not os.path.exists(path):
            print(f"[skip] not found: {path}")
            continue
        df = apply_corrections(path)
        report(path, df)
    print("\n[✔] Phase-1 evidence correction applied.")


if __name__ == "__main__":
    main()
