"""Script 2: preprocessing + multicollinearity check for one FARS year.

Preprocessing steps are taken from `decision_tree.ipynb` (cells up to "Data ready"):
FATAL label, occupant filter, numeric unknown-code exclusions. One-hot encoding is
deferred to the sklearn Pipeline in decision_tree.py (fit on training folds only).

Year-to-year code harmonization (RECODES below) makes every year 2016-2023 use the
same codes, based on fars_variable_lists.xlsx and the FARS Analytical User's Manual.
DRUNK_DR (dropped from the accident file in 2021) is rebuilt from DR_DRINK.

Multicollinearity check on the modeled (BASE) features, using the right measure for
each pair of column types:
    numeric  x numeric   -> |Pearson r| (+ VIF for the numeric set)
    category x category  -> bias-corrected Cramer's V
    numeric  x category  -> correlation ratio (eta)
All three are on a 0-1 scale, so they share one heatmap. The label FATAL is never used.

Input:  processed/preprocessed/fars_<YEAR>_person.parquet   (from init_load.py)
Output (all in processed/decision_tree/<YEAR>/preprocessing/):
        full_set_filtered_unscaled_<YEAR>.csv   (cohort read by decision_tree.py)
        features_<YEAR>.json                    (feature lists read by decision_tree.py)
        recode_audit_<YEAR>.csv                 (rows changed per recode rule)
        multicollinearity/*.csv, *.png

Run from anywhere, e.g. the repo root:  python project/scripts/preprocessing.py 2019
(no year = 2016). From Jupyter, import this file and call main(2019).
"""

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

import matplotlib

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    matplotlib.use("Agg")  # no plot windows when run as a plain script
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
DEFAULT_YEAR = 2016
VALID_YEARS = range(2016, 2024)
LOAD_FORMAT = "parquet"  # must match SAVE_FORMAT in init_load.py
CHECK_TIERS = "base"  # "base" (modeled features) or "all" (base + impact + post)
APPLY_RECODES = True  # False reproduces the original (pre-harmonization) 2016 results

# Thresholds used only to FLAG pairs; nothing is dropped automatically.
HIGH_ASSOC = 0.80  # |r|, Cramer's V, or eta at or above this = high
MODERATE_ASSOC = 0.50
HIGH_VIF = 5.0

# After reviewing the report, list any BASE columns the team agrees to remove.
# decision_tree.py models exactly BASE_COLS minus DROP_COLS.
DROP_COLS = []

# Paths are anchored to this file (project/scripts/), so outputs land in project/
# no matter which directory the script is run from.
try:
    PROJECT_DIR = Path(__file__).resolve().parent.parent
except (
    NameError
):  # running cell by cell in Jupyter / VS Code, where __file__ is undefined
    PROJECT_DIR = next(
        p
        for p in (Path.cwd(), Path.cwd().parent, Path.cwd() / "project")
        if (p / "scripts" / "init_load.py").exists()
    )
PREPROCESSED_DIR = PROJECT_DIR / "processed" / "preprocessed"
DECISION_TREE_DIR = PROJECT_DIR / "processed" / "decision_tree"

# ---------------------------------------------------------------------------
# Feature groups
# ---------------------------------------------------------------------------
ID_COLS = ["ST_CASE", "VEH_NO", "PER_NO", "YEAR", "STATE", "INJ_SEV"]
BASE_COLS = [
    "AGE",
    "SEX",
    "PER_TYP",
    "SEAT_POS",
    "REST_USE",
    "BODY_TYP",
    "MOD_YEAR",
    "NUMOCCS",
    "TOW_VEH",
    "L_STATUS",
    "VSPD_LIM",
    "VALIGN",
    "VPROFILE",
    "VSURCOND",
    "VTRAFWAY",
    "VNUM_LAN",
    "VTRAFCON",
    "VTCONT_F",
    "HOUR",
    "DAY_WEEK",
    "MONTH",
    "RUR_URB",
    "FUNC_SYS",
    "LGT_COND",
    "WEATHER",
    "RELJCT2",
]
IMPACT_COLS = [
    "IMPACT1",
    "P_CRASH1",
    "P_CRASH2",
    "PCRASH4",
    "PCRASH5",
    "SPEEDREL",
    "DR_DRINK",
    "HARM_EV",
    "MAN_COLL",
    "REL_ROAD",
    "VE_FORMS",
    "PEDS",
    "PERNOTMVIT",
    "PERSONS",
    "PERMVIT",
    "DRUNK_DR",
]
POST_COLS = ["AIR_BAG", "EJECTION", "EXTRICAT", "ROLLOVER", "DEFORMED", "FIRE_EXP"]
NUMERIC_COLS = [
    "AGE",
    "MOD_YEAR",
    "NUMOCCS",
    "VSPD_LIM",
    "VE_FORMS",
    "PEDS",
    "PERNOTMVIT",
    "PERSONS",
    "PERMVIT",
]

# Step 4: rows with these codes in numeric columns are dropped (legacy rules retained).
UNKNOWN_CODES = {
    "AGE": [998, 999],
    "MOD_YEAR": [9998, 9999],
    "NUMOCCS": [97, 98, 99],  # legacy: 97/98 are valid counts in 2016
    "VSPD_LIM": [0, 98, 99],  # legacy: 0 is a substantive category, not unknown
}

# ---------------------------------------------------------------------------
# Year-to-year code harmonization
#
# Each rule maps codes a year used onto the code later years use for the same thing,
# so all years share one coding. A rule only fires for its own years (last = None
# means "and every later year"). Sources: fars_variable_lists.xlsx, plus a full check
# of all 26 modeled (BASE) columns against the FARS Analytical User's Manual 1975-2024
# (page numbers below are the manual's printed page numbers).
#
# Where FARS added a new code, the cases it covers were filed under an older code in
# earlier years, so the new code is merged back into that older code.
#
# JUDGMENT CALLS. Two rules (marked "JUDGMENT CALL" in their reason, which also
# appears in recode_audit_<YEAR>.csv) map a new code whose earlier home cannot be
# pinned down from the manual or the data:
#   - VTRAFWAY 7 -> 9: "two-way divided, unknown median type" (2022+) was previously
#     coded 2, 3, or 9 depending on the report; 9 (unknown) is the closest single code.
#     About 450-500 occupants per year.
#   - REST_USE 6 -> 97: "racing-style harness" (2019+) was most likely coded 97 (Other)
#     before; it may instead have been 8 (restraint used, type unknown). 2-11 per year.
# Both affect few enough people that either choice barely moves the results.
# ---------------------------------------------------------------------------
# (column, first year, last year, {old code: new code}, reason)
RECODES = [
    (
        "REST_USE",
        2016,
        2016,
        {0: 20, 7: 20},
        "Not Applicable (0) and None Used (7) became None Used/Not Applicable (20) in "
        "2017",
    ),
    (
        "REST_USE",
        2016,
        2018,
        {5: 20, 16: 20, 17: 20, 19: 20, 29: 20},
        "helmet codes moved to HELM_USE in 2019; riders are coded 20 from 2019 (manual "
        "p. 304)",
    ),
    (
        "BODY_TYP",
        2016,
        2016,
        {30: 34, 31: 34},
        "Compact (30) and Standard (31) Pickup became Light Pickup (34) in 2017",
    ),
    (
        "BODY_TYP",
        2016,
        2017,
        {32: 34},
        "Pickup With Slide-in Camper (32) retired after 2017 (manual p. 137)",
    ),
    (
        "AIR_BAG",
        2016,
        2016,
        {0: 20},
        "Not Applicable (0) is coded Not Deployed (20) from 2017",
    ),
    (
        "ROLLOVER",
        2016,
        2021,
        {1: 3, 2: 3, 9: 3},
        "tripped/untripped/unknown-type rollovers collapsed into Rollover (3) in 2022",
    ),
    (
        "ROLLOVER",
        2022,
        None,
        {8: 0},
        "Not Applicable (8) split off from No Rollover (0) in 2022; merged back",
    ),
    (
        "DEFORMED",
        2022,
        None,
        {7: 8},
        "Damage Reported, Extent Unknown (7) split off from Not Reported (8) in 2022; "
        "merged back",
    ),
    # --- from the full manual check of the modeled columns ---
    (
        "BODY_TYP",
        2017,
        None,
        {84: 88},
        "Motor Scooter (84) split off from Other Motored Cycle (88) in 2017 (manual p. "
        "139)",
    ),
    (
        "BODY_TYP",
        2017,
        None,
        {85: 82, 86: 82, 87: 82},
        "autocycle/three-wheel codes 85-87 split off from Three-Wheel Motorcycle (82) "
        "in 2017 (manual p. 139)",
    ),
    (
        "BODY_TYP",
        2017,
        None,
        {96: 97},
        "off-highway utility vehicles (96) split off from Other Vehicle Type (97) in "
        "2017 (manual p. 140)",
    ),
    (
        "SEAT_POS",
        2019,
        None,
        {56: 55},
        "Appended to a Motor Vehicle for Motion (56) split off from Riding on Vehicle "
        "Exterior (55) in 2019 (manual p. 302)",
    ),
    (
        "TOW_VEH",
        2022,
        None,
        {7: 1},
        "Trailing Unit Other than a Trailer (7) split off in 2022; before 2022 any "
        "trailing unit was 1 (manual pp. 144-145)",
    ),
    (
        "VTCONT_F",
        2016,
        None,
        {2: 1, 4: 1},
        "Not Functioning (1), Functioning Improperly (2) and the 2019+ combined code "
        "(4) merged into 1 "
        "in all years, since 4 cannot be split back (manual p. 232)",
    ),
    (
        "VTRAFWAY",
        2022,
        None,
        {7: 9},
        "JUDGMENT CALL: Divided, Unknown Median Type (7, 2022+) was coded 2, 3 or 9 "
        "before; "
        "mapped to 9 (unknown) as the closest single code (manual p. 223)",
    ),
    (
        "REST_USE",
        2019,
        None,
        {6: 97},
        "JUDGMENT CALL: Racing-Style Harness (6, 2019+) most likely coded Other (97) "
        "before; "
        "could have been 8 (type unknown) (manual p. 304)",
    ),
]
AUDIT_COLUMNS = ["column", "years", "mapping", "rows_changed", "reason"]


# ---------------------------------------------------------------------------
# Command line and output folders
# ---------------------------------------------------------------------------
def preprocessing_dir(year):
    """processed/decision_tree/<YEAR>/preprocessing/ (read by decision_tree.py)."""
    return DECISION_TREE_DIR / str(year) / "preprocessing"


def multicollinearity_dir(year):
    return preprocessing_dir(year) / "multicollinearity"


def parse_year():
    """Year from the command line (DEFAULT_YEAR in Jupyter, which has its own argv)."""
    if INTERACTIVE:
        return DEFAULT_YEAR
    parser = argparse.ArgumentParser(
        description="FARS preprocessing + multicollinearity check for one year"
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        default=DEFAULT_YEAR,
        choices=VALID_YEARS,
        metavar="YEAR",
        help="FARS year, 2016-2023 (default: %(default)s)",
    )
    return parser.parse_args().year


# ---------------------------------------------------------------------------
# Load and harmonize
# ---------------------------------------------------------------------------
def load_year(year):
    """Read the person-level table that init_load.py saved for this year."""
    in_path = PREPROCESSED_DIR / f"fars_{year}_person.{LOAD_FORMAT}"
    if not in_path.exists():
        raise FileNotFoundError(f"Missing {in_path}. Run scripts/init_load.py first.")
    if LOAD_FORMAT == "parquet":
        df = pd.read_parquet(in_path)
    else:
        df = pd.read_csv(in_path, low_memory=False)
    if "YEAR" not in df:
        df["YEAR"] = year
    assert df["YEAR"].eq(year).all(), "Unexpected/missing year"
    print(f"Loaded {in_path.name}: {df.shape[0]:,} people x {df.shape[1]} columns")
    return df


def rebuild_drunk_dr(people):
    """DRUNK_DR = number of drinking drivers in the crash, i.e. vehicles with
    DR_DRINK == 1 per ST_CASE. Matches the published DRUNK_DR exactly for 2016-2020."""
    vehicles = people.dropna(subset=["DR_DRINK"]).drop_duplicates(["ST_CASE", "VEH_NO"])
    per_crash = vehicles["DR_DRINK"].eq(1).groupby(vehicles["ST_CASE"]).sum()
    return people["ST_CASE"].map(per_crash).fillna(0).astype(int)


def rule_applies(year, first, last):
    """True if a RECODES rule for first..last (None = open-ended) covers year."""
    return first <= year and (last is None or year <= last)


def apply_recodes(df, year):
    """Apply this year's RECODES rules (and the DRUNK_DR rebuild) to df in place.
    Returns an audit table with one row per rule that fired."""
    audit = []
    for col, first, last, mapping, reason in RECODES:
        if not rule_applies(year, first, last):
            continue
        hit = df[col].isin(list(mapping))
        df.loc[hit, col] = df.loc[hit, col].map(mapping)
        audit.append(
            {
                "column": col,
                "years": f"{first}-{last or 'later'}",
                "mapping": str(mapping),
                "rows_changed": int(hit.sum()),
                "reason": reason,
            }
        )

    rebuilt = rebuild_drunk_dr(df)
    if "DRUNK_DR" in df:
        mismatches = int((rebuilt != df["DRUNK_DR"]).sum())
        print(f"DRUNK_DR present; rebuild check: {mismatches:,} mismatching rows")
    else:
        df["DRUNK_DR"] = rebuilt
        audit.append(
            {
                "column": "DRUNK_DR",
                "years": "2021-later",
                "mapping": "rebuilt from DR_DRINK",
                "rows_changed": len(df),
                "reason": "DRUNK_DR removed from the accident file in 2021",
            }
        )
    return pd.DataFrame(audit, columns=AUDIT_COLUMNS)


def save_recode_audit(audit, year):
    audit.to_csv(preprocessing_dir(year) / f"recode_audit_{year}.csv", index=False)
    print(f"Recodes for {year} ({'on' if APPLY_RECODES else 'OFF'}):")
    print(
        audit.drop(columns="reason").to_string(index=False) if len(audit) else "  none"
    )


# ---------------------------------------------------------------------------
# Cohort: label, occupant filter, numeric unknown codes
# ---------------------------------------------------------------------------
def build_cohort(df):
    """Steps 1-4: FATAL label, vehicle occupants only, drop numeric unknown codes."""
    full_set = df[ID_COLS + BASE_COLS + IMPACT_COLS + POST_COLS].copy()

    # Step 1: binary label FATAL (keep known injury levels 0-4)
    full_set = full_set.loc[full_set["INJ_SEV"].between(0, 4)].copy()
    full_set["FATAL"] = (full_set["INJ_SEV"] == 4).astype(int)
    print(f"Step 1: {len(full_set):,} people remain")

    # Step 2: vehicle occupants only (PER_TYP 1 = driver, 2 = passenger)
    full_set = full_set.loc[full_set["PER_TYP"].isin([1, 2])].copy()
    print(f"Step 2: {len(full_set):,} people remain")

    # Step 3: encoding is deferred to the Pipeline in decision_tree.py

    # Step 4: drop rows with unknown codes in numeric columns
    return drop_numeric_unknowns(full_set)


def drop_numeric_unknowns(full_set):
    """Drop rows whose numeric columns hold an UNKNOWN_CODES value; print an audit."""
    cohort_before = full_set.copy()
    excluded = pd.Series(False, index=full_set.index)
    audit = []
    for col, codes in UNKNOWN_CODES.items():
        mask = full_set[col].isin(codes)
        audit.append(
            {
                "field": col,
                "matched_rows": int(mask.sum()),
                "additional_excluded": int((mask & ~excluded).sum()),
            }
        )
        excluded |= mask
    full_set = full_set.loc[~excluded].copy()
    print(
        f"Step 4: {len(full_set):,} people remain; {excluded.sum():,} excluded by "
        "numeric codes"
    )
    print(pd.DataFrame(audit).to_string(index=False))
    print(
        pd.DataFrame(
            {
                "occupants": [len(cohort_before), len(full_set), int(excluded.sum())],
                "fatal_share": [
                    cohort_before.FATAL.mean(),
                    full_set.FATAL.mean(),
                    cohort_before.loc[excluded, "FATAL"].mean(),
                ],
            },
            index=["before numeric exclusions", "retained", "excluded"],
        )
        .round(4)
        .to_string()
    )
    return full_set


# ---------------------------------------------------------------------------
# Step 5: multicollinearity check
#
# Measured on the retained cohort's feature columns only (no label). For a decision
# tree, collinearity does not hurt predictions, but it splits importance between
# redundant columns and makes the importance chart harder to interpret. It matters
# more for the logistic regression, so the same tables can be reused there.
# ---------------------------------------------------------------------------
def cramers_v(a, b):
    """Bias-corrected Cramer's V (Bergsma 2013) between two categorical series."""
    table = pd.crosstab(a, b).to_numpy()
    n = table.sum()
    r, k = table.shape
    if r < 2 or k < 2:
        return np.nan
    expected = table.sum(1, keepdims=True) * table.sum(0, keepdims=True) / n
    chi2 = ((table - expected) ** 2 / expected).sum()
    phi2 = max(0.0, chi2 / n - (k - 1) * (r - 1) / (n - 1))
    r_c = r - (r - 1) ** 2 / (n - 1)
    k_c = k - (k - 1) ** 2 / (n - 1)
    denom = min(k_c - 1, r_c - 1)
    return np.sqrt(phi2 / denom) if denom > 0 else np.nan


def correlation_ratio(categories, values):
    """Eta: share of a numeric column's spread explained by a categorical one (0-1)."""
    ok = values.notna()
    categories, values = categories[ok], values[ok]
    total = ((values - values.mean()) ** 2).sum()
    if total == 0:
        return np.nan
    group = values.groupby(categories)
    between = (group.count() * (group.mean() - values.mean()) ** 2).sum()
    return np.sqrt(between / total)


def vif_table(numeric_df):
    """VIF_j = 1 / (1 - R^2_j), regressing each numeric column on the others."""
    data = numeric_df.dropna()
    rows = []
    for col in data.columns:
        others = data.drop(columns=col)
        if others.shape[1] == 0:
            continue
        r2 = LinearRegression().fit(others, data[col]).score(others, data[col])
        rows.append(
            {
                "field": col,
                "R2_on_others": r2,
                "VIF": np.inf if r2 >= 1 else 1 / (1 - r2),
            }
        )
    return pd.DataFrame(rows).set_index("field").sort_values("VIF", ascending=False)


def check_columns():
    """Columns included in the multicollinearity check (set by CHECK_TIERS)."""
    return BASE_COLS if CHECK_TIERS == "base" else BASE_COLS + IMPACT_COLS + POST_COLS


def association_tables(full_set, check_cols):
    """Mixed-type association matrix, ranked pair table, and numeric VIF table."""
    num_cols = [c for c in check_cols if c in NUMERIC_COLS]
    cat_cols = [c for c in check_cols if c not in NUMERIC_COLS]
    X_check = full_set[check_cols]
    cats = X_check[cat_cols].fillna(
        -1
    )  # actual NaN = its own category, as in decision_tree.py

    assoc = pd.DataFrame(np.eye(len(check_cols)), index=check_cols, columns=check_cols)
    pair_rows = []
    for a, b in combinations(check_cols, 2):
        if a in num_cols and b in num_cols:
            value, measure = abs(X_check[a].corr(X_check[b])), "|Pearson r|"
        elif a in cat_cols and b in cat_cols:
            value, measure = cramers_v(cats[a], cats[b]), "Cramer's V"
        else:
            num, cat = (a, b) if a in num_cols else (b, a)
            value, measure = correlation_ratio(cats[cat], X_check[num]), "eta"
        assoc.loc[a, b] = assoc.loc[b, a] = value
        pair_rows.append(
            {"field_1": a, "field_2": b, "measure": measure, "association": value}
        )

    pairs = pd.DataFrame(pair_rows).sort_values("association", ascending=False)
    pairs["flag"] = np.select(
        [pairs.association >= HIGH_ASSOC, pairs.association >= MODERATE_ASSOC],
        ["HIGH", "moderate"],
        "",
    )
    vif = vif_table(X_check[num_cols])
    vif["flag"] = np.where(vif.VIF >= HIGH_VIF, "HIGH", "")

    constant = [c for c in check_cols if X_check[c].nunique(dropna=False) < 2]
    if constant:
        print(
            "WARNING: constant columns (no association defined, gray in heatmap): "
            f"{constant}"
        )
    return assoc, pairs, vif


def save_association_tables(assoc, pairs, vif, year):
    mc_dir = multicollinearity_dir(year)
    pairs.to_csv(mc_dir / f"pairwise_association_{year}.csv", index=False)
    assoc.to_csv(mc_dir / f"association_matrix_{year}.csv")
    vif.to_csv(mc_dir / f"vif_numeric_{year}.csv")

    print(f"\nVIF for numeric {CHECK_TIERS} features (>= {HIGH_VIF} flagged):")
    print(vif.round(3).to_string())
    flagged = pairs[pairs.flag != ""]
    print(
        f"\nPairs with association >= {MODERATE_ASSOC} ({len(flagged)} of "
        f"{len(pairs)}):"
    )
    print(flagged.round(3).to_string(index=False) if len(flagged) else "  none")


def plot_association_heatmap(assoc, check_cols, year):
    """Heatmap of the mixed association matrix; values >= MODERATE_ASSOC are printed."""
    fig, ax = plt.subplots(
        figsize=(0.45 * len(check_cols) + 3, 0.45 * len(check_cols) + 2)
    )
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("lightgray")  # undefined, e.g. a constant column
    im = ax.imshow(assoc.to_numpy(dtype=float), vmin=0, vmax=1, cmap=cmap)
    ax.set_xticks(range(len(check_cols)), check_cols, rotation=90, fontsize=8)
    ax.set_yticks(range(len(check_cols)), check_cols, fontsize=8)
    for i in range(len(check_cols)):
        for j in range(len(check_cols)):
            v = assoc.iat[i, j]
            if i != j and pd.notna(v) and v >= MODERATE_ASSOC:
                ax.text(
                    j,
                    i,
                    f"{v:.2f}",
                    ha="center",
                    va="center",
                    fontsize=6,
                    color="black" if v > 0.6 else "white",
                )
    fig.colorbar(im, ax=ax, fraction=0.035, label="|r| / Cramer's V / eta")
    ax.set_title(
        f"FARS {year} {CHECK_TIERS} features: pairwise association (values >= "
        f"{MODERATE_ASSOC} shown)"
    )
    fig.tight_layout()
    fig.savefig(
        multicollinearity_dir(year) / f"association_heatmap_{year}.png", dpi=150
    )
    plt.show() if INTERACTIVE else plt.close(fig)


# ---------------------------------------------------------------------------
# Save the cohort and the feature lists decision_tree.py will model
# ---------------------------------------------------------------------------
def save_cohort(full_set, year):
    unknown_drops = set(DROP_COLS) - set(BASE_COLS)
    assert not unknown_drops, f"DROP_COLS not in BASE_COLS: {unknown_drops}"
    base_features = [c for c in BASE_COLS if c not in DROP_COLS]

    out_path = preprocessing_dir(year) / f"full_set_filtered_unscaled_{year}.csv"
    full_set.to_csv(out_path, index=False)
    features = {
        "year": year,
        "id_cols": ID_COLS,
        "base_cols": BASE_COLS,
        "impact_cols": IMPACT_COLS,
        "post_cols": POST_COLS,
        "numeric_cols": NUMERIC_COLS,
        "drop_cols": DROP_COLS,
        "base_features": base_features,
    }
    (preprocessing_dir(year) / f"features_{year}.json").write_text(
        json.dumps(features, indent=2)
    )
    print(
        f"\nSaved {out_path.name}: {full_set.shape[0]:,} rows x {full_set.shape[1]} "
        "columns"
    )
    print(
        f"Modeled features for decision_tree.py: {len(base_features)} (dropped: "
        f"{DROP_COLS or 'none'})"
    )
    print("Outputs in", preprocessing_dir(year).relative_to(PROJECT_DIR))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(year=None):
    year = parse_year() if year is None else year
    print(f"FARS year: {year}")
    multicollinearity_dir(year).mkdir(parents=True, exist_ok=True)

    df = load_year(year)
    if APPLY_RECODES:
        audit = apply_recodes(df, year)
    else:
        audit = pd.DataFrame(columns=AUDIT_COLUMNS)
    save_recode_audit(audit, year)

    full_set = build_cohort(df)

    check_cols = check_columns()
    assoc, pairs, vif = association_tables(full_set, check_cols)
    save_association_tables(assoc, pairs, vif, year)
    plot_association_heatmap(assoc, check_cols, year)

    save_cohort(full_set, year)


if __name__ == "__main__":
    main()
