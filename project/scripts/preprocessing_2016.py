# %% [markdown]
# # Script 2: 2016 preprocessing + multicollinearity check
#
# Preprocessing steps are taken unchanged from `decision_tree.ipynb` (cells up to
# "Data ready"): FATAL label, occupant filter, numeric unknown-code exclusions.
# One-hot encoding is still deferred to the sklearn Pipeline in script 3.
#
# New: a multicollinearity check on the modeled (BASE) features, using the right
# measure for each pair of column types:
#   numeric  x numeric      -> |Pearson r| (+ VIF for the numeric set)
#   category x category     -> bias-corrected Cramer's V
#   numeric  x category     -> correlation ratio (eta)
# All three are on a 0-1 scale, so they share one heatmap. The label FATAL is never used.
#
# Input:  processed/preprocessed/fars_2016_person.csv   (from script 1)
# Output: processed/decision_tree/full_set_filtered_unscaled_2016.csv
#         processed/decision_tree/features_2016.json     (feature lists read by script 3)
#         processed/decision_tree/multicollinearity/*.csv, *.png
#
# Run from anywhere, e.g. the repo root:  python project/scripts/preprocessing_2016.py

# %%
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

YEAR = 2016
LOAD_FORMAT = "parquet"   # must match SAVE_FORMAT in script 1
CHECK_TIERS = "base"  # "base" (modeled features) or "all" (base + impact + post)

# Thresholds used only to FLAG pairs; nothing is dropped automatically.
HIGH_ASSOC = 0.80     # |r|, Cramer's V, or eta at or above this = high
MODERATE_ASSOC = 0.50
HIGH_VIF = 5.0

# After reviewing the report, list any BASE columns the team agrees to remove.
# Script 3 models exactly BASE_COLS minus DROP_COLS.
DROP_COLS = []

# Paths are anchored to this file (project/scripts/), so outputs land in project/
# no matter which directory the script is run from.
try:
    PROJECT_DIR = Path(__file__).resolve().parent.parent
except NameError:  # running cell by cell in Jupyter / VS Code, where __file__ is undefined
    PROJECT_DIR = next(p for p in (Path.cwd(), Path.cwd().parent, Path.cwd() / "project")
                       if (p / "scripts" / "init_load.py").exists())
IN_PATH = PROJECT_DIR / "processed" / "preprocessed" / f"fars_{YEAR}_person.{LOAD_FORMAT}"
RESULT_DIR = PROJECT_DIR / "processed" / "decision_tree"
MC_DIR = RESULT_DIR / "multicollinearity"
MC_DIR.mkdir(parents=True, exist_ok=True)

# %% Load
if not IN_PATH.exists():
    raise FileNotFoundError(f"Missing {IN_PATH}. Run scripts/init_load.py first.")
df = pd.read_parquet(IN_PATH) if LOAD_FORMAT == "parquet" else pd.read_csv(IN_PATH, low_memory=False)
if "YEAR" not in df:
    df["YEAR"] = YEAR
assert df["YEAR"].eq(YEAR).all(), "Unexpected/missing year"
print(f"Loaded {IN_PATH.name}: {df.shape[0]:,} people x {df.shape[1]} columns")

# %% Feature groups (unchanged)
ID_COLS = ["ST_CASE", "VEH_NO", "PER_NO", "YEAR", "STATE", "INJ_SEV"]
BASE_COLS = [
    "AGE", "SEX", "PER_TYP", "SEAT_POS", "REST_USE", "BODY_TYP", "MOD_YEAR",
    "NUMOCCS", "TOW_VEH", "L_STATUS", "VSPD_LIM", "VALIGN", "VPROFILE",
    "VSURCOND", "VTRAFWAY", "VNUM_LAN", "VTRAFCON", "VTCONT_F", "HOUR",
    "DAY_WEEK", "MONTH", "RUR_URB", "FUNC_SYS", "LGT_COND", "WEATHER",
    "RELJCT2",
]
IMPACT_COLS = [
    "IMPACT1", "P_CRASH1", "P_CRASH2", "PCRASH4", "PCRASH5", "SPEEDREL",
    "DR_DRINK", "HARM_EV", "MAN_COLL", "REL_ROAD", "VE_FORMS", "PEDS",
    "PERNOTMVIT", "PERSONS", "PERMVIT", "DRUNK_DR",
]
POST_COLS = ["AIR_BAG", "EJECTION", "EXTRICAT", "ROLLOVER", "DEFORMED", "FIRE_EXP"]
NUMERIC_COLS = ["AGE", "MOD_YEAR", "NUMOCCS", "VSPD_LIM", "VE_FORMS",
                "PEDS", "PERNOTMVIT", "PERSONS", "PERMVIT"]

FULL_SET = df[ID_COLS + BASE_COLS + IMPACT_COLS + POST_COLS].copy()

# %% Step 1: binary label FATAL (keep known injury levels 0-4)
FULL_SET = FULL_SET.loc[FULL_SET["INJ_SEV"].between(0, 4)].copy()
FULL_SET["FATAL"] = (FULL_SET["INJ_SEV"] == 4).astype(int)
print(f"Step 1: {len(FULL_SET):,} people remain")

# %% Step 2: vehicle occupants only (PER_TYP 1 = driver, 2 = passenger)
FULL_SET = FULL_SET.loc[FULL_SET["PER_TYP"].isin([1, 2])].copy()
print(f"Step 2: {len(FULL_SET):,} people remain")

# %% Step 3: encoding is deferred to the Pipeline in script 3 (fit on training folds only)

# %% Step 4: drop rows with unknown codes in numeric columns (legacy rules retained)
UNKNOWN_CODES = {
    "AGE":      [998, 999],
    "MOD_YEAR": [9998, 9999],
    "NUMOCCS":  [97, 98, 99],  # legacy: 97/98 are valid counts in 2016
    "VSPD_LIM": [0, 98, 99],   # legacy: 0 is a substantive category, not unknown
}
cohort_before = FULL_SET.copy()
excluded = pd.Series(False, index=FULL_SET.index)
audit = []
for col, codes in UNKNOWN_CODES.items():
    mask = FULL_SET[col].isin(codes)
    audit.append({"field": col, "matched_rows": int(mask.sum()),
                  "additional_excluded": int((mask & ~excluded).sum())})
    excluded |= mask
FULL_SET = FULL_SET.loc[~excluded].copy()
print(f"Step 4: {len(FULL_SET):,} people remain; {excluded.sum():,} excluded by numeric codes")
print(pd.DataFrame(audit).to_string(index=False))
print(pd.DataFrame({
    "occupants": [len(cohort_before), len(FULL_SET), int(excluded.sum())],
    "fatal_share": [cohort_before.FATAL.mean(), FULL_SET.FATAL.mean(),
                    cohort_before.loc[excluded, "FATAL"].mean()],
}, index=["before numeric exclusions", "retained", "excluded"]).round(4).to_string())

# %% [markdown]
# ## Step 5 (new): multicollinearity check
#
# Measured on the retained cohort's feature columns only (no label). For a decision
# tree, collinearity does not hurt predictions, but it splits importance between
# redundant columns and makes the importance chart harder to interpret. It matters
# more for the logistic regression, so the same tables can be reused there.

# %%
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
    """Eta: share of a numeric column's spread explained by a categorical column (0-1)."""
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
        rows.append({"field": col, "R2_on_others": r2,
                     "VIF": np.inf if r2 >= 1 else 1 / (1 - r2)})
    return pd.DataFrame(rows).set_index("field").sort_values("VIF", ascending=False)


check_cols = BASE_COLS if CHECK_TIERS == "base" else BASE_COLS + IMPACT_COLS + POST_COLS
num_cols = [c for c in check_cols if c in NUMERIC_COLS]
cat_cols = [c for c in check_cols if c not in NUMERIC_COLS]
X_check = FULL_SET[check_cols]
cats = X_check[cat_cols].fillna(-1)  # actual NaN = its own category, as in script 3

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
    pair_rows.append({"field_1": a, "field_2": b, "measure": measure, "association": value})

pairs = pd.DataFrame(pair_rows).sort_values("association", ascending=False)
pairs["flag"] = np.select([pairs.association >= HIGH_ASSOC, pairs.association >= MODERATE_ASSOC],
                          ["HIGH", "moderate"], "")
vif = vif_table(X_check[num_cols])
vif["flag"] = np.where(vif.VIF >= HIGH_VIF, "HIGH", "")

constant = [c for c in check_cols if X_check[c].nunique(dropna=False) < 2]
if constant:
    print(f"WARNING: constant columns (no association defined, gray in heatmap): {constant}")

pairs.to_csv(MC_DIR / f"pairwise_association_{YEAR}.csv", index=False)
assoc.to_csv(MC_DIR / f"association_matrix_{YEAR}.csv")
vif.to_csv(MC_DIR / f"vif_numeric_{YEAR}.csv")

print(f"\nVIF for numeric {CHECK_TIERS} features (>= {HIGH_VIF} flagged):")
print(vif.round(3).to_string())
flagged = pairs[pairs.flag != ""]
print(f"\nPairs with association >= {MODERATE_ASSOC} ({len(flagged)} of {len(pairs)}):")
print(flagged.round(3).to_string(index=False) if len(flagged) else "  none")

# %% Heatmap of the mixed association matrix
fig, ax = plt.subplots(figsize=(0.45 * len(check_cols) + 3, 0.45 * len(check_cols) + 2))
cmap = plt.get_cmap("viridis").copy()
cmap.set_bad("lightgray")  # undefined, e.g. a constant column
im = ax.imshow(assoc.to_numpy(dtype=float), vmin=0, vmax=1, cmap=cmap)
ax.set_xticks(range(len(check_cols)), check_cols, rotation=90, fontsize=8)
ax.set_yticks(range(len(check_cols)), check_cols, fontsize=8)
for i in range(len(check_cols)):
    for j in range(len(check_cols)):
        v = assoc.iat[i, j]
        if i != j and pd.notna(v) and v >= MODERATE_ASSOC:
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6,
                    color="black" if v > 0.6 else "white")
fig.colorbar(im, ax=ax, fraction=0.035, label="|r| / Cramer's V / eta")
ax.set_title(f"FARS {YEAR} {CHECK_TIERS} features: pairwise association (values >= {MODERATE_ASSOC} shown)")
fig.tight_layout()
fig.savefig(MC_DIR / f"association_heatmap_{YEAR}.png", dpi=150)
plt.show() if INTERACTIVE else plt.close(fig)

# %% Save the cohort and the feature lists script 3 will model
unknown_drops = set(DROP_COLS) - set(BASE_COLS)
assert not unknown_drops, f"DROP_COLS not in BASE_COLS: {unknown_drops}"
BASE_FEATURES = [c for c in BASE_COLS if c not in DROP_COLS]

out_path = RESULT_DIR / f"full_set_filtered_unscaled_{YEAR}.csv"
FULL_SET.to_csv(out_path, index=False)
features = {"year": YEAR, "id_cols": ID_COLS, "base_cols": BASE_COLS,
            "impact_cols": IMPACT_COLS, "post_cols": POST_COLS,
            "numeric_cols": NUMERIC_COLS, "drop_cols": DROP_COLS,
            "base_features": BASE_FEATURES}
(RESULT_DIR / f"features_{YEAR}.json").write_text(json.dumps(features, indent=2))
print(f"\nSaved {out_path.name}: {FULL_SET.shape[0]:,} rows x {FULL_SET.shape[1]} columns")
print(f"Modeled features for script 3: {len(BASE_FEATURES)} (dropped: {DROP_COLS or 'none'})")