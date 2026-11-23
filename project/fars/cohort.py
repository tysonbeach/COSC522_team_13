"""Who is modeled: the label, the occupant filter, and unknown-code exclusions."""

import pandas as pd

from .config import (
    ALL_FEATURE_COLS, CRASH_KEY, ID_COLS, LABEL, MOTORCYCLE_BODY_TYPES, UNKNOWN_CODES,
)


def add_label(df):
    """Keep known injury severities (INJ_SEV 0-4) and add FATAL (1 = INJ_SEV 4)."""
    df = df.loc[df["INJ_SEV"].between(0, 4)].copy()
    df[LABEL] = (df["INJ_SEV"] == 4).astype(int)
    print(f"Known outcome:           {len(df):,} people")
    return df


def keep_occupants(df):
    """Vehicle occupants only (PER_TYP 1 = driver, 2 = passenger)."""
    df = df.loc[df["PER_TYP"].isin([1, 2])].copy()
    print(f"Drivers and passengers:  {len(df):,} people")
    return df


def drop_numeric_unknowns(df):
    """Drop rows whose numeric columns hold an UNKNOWN_CODES value; print an audit."""
    excluded = pd.Series(False, index=df.index)
    audit = []
    for col, codes in UNKNOWN_CODES.items():
        mask = df[col].isin(codes)
        audit.append(
            {
                "field": col,
                "matched_rows": int(mask.sum()),
                "additional_excluded": int((mask & ~excluded).sum()),
            }
        )
        excluded |= mask
    kept = df.loc[~excluded].copy()
    print(f"Known numeric values:    {len(kept):,} people ({excluded.sum():,} excluded)")
    print(pd.DataFrame(audit).to_string(index=False))
    fatal_shares = pd.DataFrame(
        {
            "occupants": [len(df), len(kept), int(excluded.sum())],
            "fatal_share": [df[LABEL].mean(), kept[LABEL].mean(), df.loc[excluded, LABEL].mean()],
        },
        index=["before numeric exclusions", "retained", "excluded"],
    )
    print(fatal_shares.round(4).to_string())
    return kept


def apply_population(df, population, audit=None):
    """Restricted: exclude motorcycles, then crashes with one modeled occupant.

    Counts are computed after the earlier cohort filters and across all vehicles
    using CRASH_KEY. This does not imply the occupant was physically alone or fatal.
    Audit crash counts can overlap between motorcycle and retained occupant groups.
    """
    if population not in ("full", "restricted"):
        raise ValueError(f"Unknown population: {population}")
    kept = df
    stages = [("before", df)]
    if population == "restricted":
        motorcycle = df["BODY_TYP"].isin(MOTORCYCLE_BODY_TYPES)
        kept = df.loc[~motorcycle].copy()
        stages.extend([("excluded_motorcycle", df.loc[motorcycle]),
                       ("after_motorcycle", kept)])
        counts = kept.groupby(CRASH_KEY)[LABEL].transform("size")
        single = counts.eq(1)
        stages.append(("excluded_single_modeled_occupant", kept.loc[single]))
        kept = kept.loc[~single].copy()
    stages.append(("retained", kept))
    rows = []
    for stage, group in stages:
        rows.append({
            "population": population,
            "stage": stage,
            "occupants": len(group),
            "crashes": len(group[CRASH_KEY].drop_duplicates()),
            "fatal_share": group[LABEL].mean(),
        })
    if audit is not None:
        audit.extend(rows)
    print(f"Population: {population}")
    print(pd.DataFrame(rows).round(4).to_string(index=False))
    return kept


def build_cohort(df, population, population_audit=None):
    """The modeled occupants: ID columns, every feature column, and FATAL."""
    df = df[ID_COLS + ALL_FEATURE_COLS]
    df = add_label(df)
    df = keep_occupants(df)
    df = drop_numeric_unknowns(df)
    return apply_population(df, population, population_audit)
