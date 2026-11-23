"""Stage 3: turn one year's joined table into the modeling dataset.

Steps: harmonize codes across years (recodes.py), build the cohort (cohort.py), and
save one dataset per year and population. The blocks are column subsets of it (see
config.BLOCKS), so every block models exactly the same occupants. One-hot encoding and
imputation happen later, inside each model's pipeline, fit on training data only.

Outputs (processed/datasets/<POPULATION>/<YEAR>/):
    dataset_<YEAR>.csv              IDs + kept feature columns + FATAL
    features_<YEAR>.json            the column lists and blocks used
    recode_audit_<YEAR>.csv         rows changed per recode rule
    medium_truck_counts_<YEAR>.csv  descriptive count
    population_audit_<YEAR>.csv     population counts and fatal shares
"""

import json

import pandas as pd

from .cohort import build_cohort
from .config import (
    ALL_FEATURE_COLS,
    BLOCKS,
    CRASH_COLS,
    CRASH_KEY,
    DROP_COLS,
    ID_COLS,
    LABEL,
    MEDIUM_TRUCK_BODY_TYPES,
    NUMERIC_COLS,
    POST_COLS,
    PRECRASH_COLS,
    PROJECT_DIR,
)
from .paths import dataset_dir, dataset_path, features_path, joined_path, require
from .recodes import AUDIT_COLUMNS, apply_recodes

APPLY_RECODES = True  # False reproduces the original (pre-harmonization) 2016 results


def load_joined(year):
    df = pd.read_parquet(require(joined_path(year), "02_load.py"))
    if "YEAR" not in df:
        df["YEAR"] = year
    assert df["YEAR"].eq(year).all(), "Unexpected/missing year"
    print(f"Loaded {joined_path(year).name}: {df.shape[0]:,} people x {df.shape[1]} columns")
    return df


def medium_truck_counts(cohort):
    """Occupants and unique vehicles per medium-truck body type."""
    medium = cohort.loc[cohort["BODY_TYP"].isin(MEDIUM_TRUCK_BODY_TYPES)]
    vehicles = medium.drop_duplicates(CRASH_KEY + ["VEH_NO"])
    counts = medium.groupby("BODY_TYP").size().rename("retained_occupants").to_frame()
    counts["unique_vehicles"] = vehicles.groupby("BODY_TYP").size()
    print(f"Medium-truck occupants: {len(medium):,}; unique vehicles: {len(vehicles):,}")
    return counts


def save_outputs(cohort, audit, year, population, population_audit):
    out_dir = dataset_dir(population, year)
    kept_features = [c for c in ALL_FEATURE_COLS if c not in DROP_COLS]
    cohort[ID_COLS + kept_features + [LABEL]].to_csv(dataset_path(population, year), index=False)
    features = {
        "year": year,
        "population": population,
        "id_cols": ID_COLS,
        "label": LABEL,
        "precrash_cols": PRECRASH_COLS,
        "crash_cols": CRASH_COLS,
        "post_cols": POST_COLS,
        "numeric_cols": NUMERIC_COLS,
        "drop_cols": DROP_COLS,
        "blocks": BLOCKS,
    }
    features_path(population, year).write_text(json.dumps(features, indent=2))
    audit.to_csv(out_dir / f"recode_audit_{year}.csv", index=False)
    pd.DataFrame(population_audit).to_csv(out_dir / f"population_audit_{year}.csv", index=False)
    medium_truck_counts(cohort).to_csv(out_dir / f"medium_truck_counts_{year}.csv")

    print(f"Saved {dataset_path(population, year).name}: {len(cohort):,} occupants")
    for block, cols in BLOCKS.items():
        print(f"  block {block}: {len(cols)} features")
    print(f"Dropped columns: {DROP_COLS or 'none'}")
    print("Outputs in", out_dir.relative_to(PROJECT_DIR))


def run(year, population):
    print(f"\n=== Preprocess {year} ({population} population) ===")
    dataset_dir(population, year).mkdir(parents=True, exist_ok=True)
    df = load_joined(year)

    audit = apply_recodes(df, year) if APPLY_RECODES else pd.DataFrame(columns=AUDIT_COLUMNS)
    print(f"Recodes ({'on' if APPLY_RECODES else 'OFF'}):")
    print(audit.drop(columns="reason").to_string(index=False) if len(audit) else "  none")

    population_audit = []
    cohort = build_cohort(df, population, population_audit)
    save_outputs(cohort, audit, year, population, population_audit)


def main(years, population):
    for year in years:
        run(year, population)
