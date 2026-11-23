"""Stage 4 (report only): pairwise association between the features of each block.

Uses the right measure for each pair of column types, all on a 0-1 scale so they share
one heatmap:
    numeric  x numeric   -> |Pearson r|   (+ VIF for the numeric set)
    category x category  -> bias-corrected Cramer's V
    numeric  x category  -> correlation ratio (eta)
The label is never used. Nothing is dropped automatically: pairs are only flagged, and
the team decides on config.DROP_COLS. For a tree, collinearity does not hurt
predictions, but it splits importance between redundant columns.

Outputs (processed/reports/multicollinearity/<POPULATION>/<YEAR>/<BLOCK>/):
    pairwise_association_*.csv, association_matrix_*.csv, vif_numeric_*.csv,
    association_heatmap_*.png
"""

import json
from itertools import combinations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from .config import BLOCKS
from .figures import plt, save_fig
from .paths import dataset_path, features_path, report_dir, require

HIGH_ASSOC = 0.80  # |r|, Cramer's V, or eta at or above this = high
MODERATE_ASSOC = 0.50
HIGH_VIF = 5.0


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
        rows.append({"field": col, "R2_on_others": r2, "VIF": np.inf if r2 >= 1 else 1 / (1 - r2)})
    vif = pd.DataFrame(rows).set_index("field").sort_values("VIF", ascending=False)
    vif["flag"] = np.where(vif.VIF >= HIGH_VIF, "HIGH", "")
    return vif


def association_tables(df, cols, numeric_cols):
    """Mixed-type association matrix and the ranked, flagged pair table."""
    num_cols = [c for c in cols if c in numeric_cols]
    cats = df[[c for c in cols if c not in numeric_cols]].fillna(-1)  # NaN = own category

    assoc = pd.DataFrame(np.eye(len(cols)), index=cols, columns=cols)
    pair_rows = []
    for a, b in combinations(cols, 2):
        if a in num_cols and b in num_cols:
            value, measure = abs(df[a].corr(df[b])), "|Pearson r|"
        elif a not in num_cols and b not in num_cols:
            value, measure = cramers_v(cats[a], cats[b]), "Cramer's V"
        else:
            num, cat = (a, b) if a in num_cols else (b, a)
            value, measure = correlation_ratio(cats[cat], df[num]), "eta"
        assoc.loc[a, b] = assoc.loc[b, a] = value
        pair_rows.append({"field_1": a, "field_2": b, "measure": measure, "association": value})

    pairs = pd.DataFrame(pair_rows).sort_values("association", ascending=False)
    pairs["flag"] = np.select(
        [pairs.association >= HIGH_ASSOC, pairs.association >= MODERATE_ASSOC],
        ["HIGH", "moderate"],
        "",
    )
    constant = [c for c in cols if df[c].nunique(dropna=False) < 2]
    if constant:
        print(f"WARNING: constant columns (no association defined, gray in heatmap): {constant}")
    return assoc, pairs


def plot_heatmap(assoc, title):
    """Heatmap of the association matrix; values >= MODERATE_ASSOC are printed."""
    cols = list(assoc.columns)
    size = 0.45 * len(cols)
    fig, ax = plt.subplots(figsize=(size + 3, size + 2))
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("lightgray")  # undefined, e.g. a constant column
    im = ax.imshow(assoc.to_numpy(dtype=float), vmin=0, vmax=1, cmap=cmap)
    ax.set_xticks(range(len(cols)), cols, rotation=90, fontsize=8)
    ax.set_yticks(range(len(cols)), cols, fontsize=8)
    for i in range(len(cols)):
        for j in range(len(cols)):
            v = assoc.iat[i, j]
            if i != j and pd.notna(v) and v >= MODERATE_ASSOC:
                color = "black" if v > 0.6 else "white"
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6, color=color)
    fig.colorbar(im, ax=ax, fraction=0.035, label="|r| / Cramer's V / eta")
    ax.set_title(title)
    fig.tight_layout()
    return fig


def run(year, population):
    print(f"\n=== Multicollinearity {year} ({population} population) ===")
    df = pd.read_csv(require(dataset_path(population, year), "03_preprocess.py"), low_memory=False)
    numeric_cols = json.loads(features_path(population, year).read_text())["numeric_cols"]

    for block, cols in BLOCKS.items():
        print(f"\n--- Block {block} ({len(cols)} features)")
        out_dir = report_dir("multicollinearity", population, year, block)
        out_dir.mkdir(parents=True, exist_ok=True)
        assoc, pairs = association_tables(df, cols, numeric_cols)
        vif = vif_table(df[[c for c in cols if c in numeric_cols]])

        tag = f"{block}_{year}"
        pairs.to_csv(out_dir / f"pairwise_association_{tag}.csv", index=False)
        assoc.to_csv(out_dir / f"association_matrix_{tag}.csv")
        vif.to_csv(out_dir / f"vif_numeric_{tag}.csv")
        title = (
            f"FARS {year}, block {block}: pairwise association (values >= {MODERATE_ASSOC} shown)"
        )
        save_fig(plot_heatmap(assoc, title), out_dir / f"association_heatmap_{tag}.png")

        print(f"VIF for numeric features (>= {HIGH_VIF} flagged):")
        print(vif.round(3).to_string())
        flagged = pairs[pairs.flag != ""]
        print(f"Pairs with association >= {MODERATE_ASSOC} ({len(flagged)} of {len(pairs)}):")
        print(flagged.round(3).to_string(index=False) if len(flagged) else "  none")


def main(years, population):
    for year in years:
        run(year, population)
