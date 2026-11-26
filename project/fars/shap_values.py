"""Stage 9: SHAP values of the tuned XGBoost, one analysis per year and feature block.

(The module is not named shap.py so it can never be confused with the shap library,
which is not needed: XGBoost computes exact TreeSHAP itself, booster.predict with
pred_contribs=True, the same path-dependent values as shap.TreeExplainer.)

Protocol:
  1. Refit the tuned XGBoost from best_params_<BLOCK>_<YEAR>.json on the training rows
     (posthoc.py; the refit is checked against the saved holdout metrics).
  2. Explain every holdout occupant. SHAP values are on the model's log-odds scale:
     for each occupant, the bias plus all SHAP values equals the model's log-odds of a
     fatal outcome (checked, to float32 precision). Nothing here selects or tunes
     anything, so explaining the holdout does not leak into model choice.
  3. One-hot columns and missing-indicator columns are summed back to their original
     FARS field. SHAP values are additive, so a field's value for an occupant is the
     total contribution of that field. Field importance = mean |field SHAP|.
  4. Comparison with XGBoost gain importance (saved by stage 7): Spearman correlation
     of the two field rankings.

SHAP describes what this model uses, on this year's holdout: associations within FARS
fatal crashes, not causal effects. Fields that carry the same information (e.g.
EXTRICAT and EJECTION, PERMVIT and VE_FORMS) can split or trade credit between them.

Outputs (processed/results/xgboost_shap/<POPULATION>/<YEAR>/):
    environment_<YEAR>.json, refit_check_<YEAR>.csv
    <BLOCK>/  (file names end _<BLOCK>_<YEAR>)
        shap_by_field_*.csv      mean |SHAP|, mean SHAP, share and rank per field; gain rank
        shap_by_column_*.csv     the same per encoded column (category level, numeric,
                                 missing indicator), with mean SHAP when the column is on
        shap_by_category_*.csv   mean field SHAP per raw category value (categorical fields)
        summary_*.md
        figures/shap_importance_*.png, shap_beeswarm_*.png, shap_dependence_*.png,
                shap_categories_*.png
processed/results/xgboost_shap/<POPULATION>/
    shap_all_years.csv, shap_means.csv, figures/shap_by_year_<BLOCK>.png   refreshed
"""

import warnings

import numpy as np
import pandas as pd
import xgboost
from matplotlib.colors import LinearSegmentedColormap

from . import modeling, posthoc
from .config import BLOCKS, PROJECT_DIR, RESULTS_DIR, SEED
from .figures import plt, save_fig
from .paths import block_dir, results_dir

MODEL = "xgboost_shap"
ADDITIVITY_TOL = 1e-3  # |bias + sum(SHAP) - log-odds|, float32 arithmetic
TOP_FIELDS = 20  # fields in the importance bar chart
TOP_COLUMNS = 15  # encoded columns in the beeswarm
TOP_CATEGORICAL = 3  # categorical fields shown level by level
MIN_LEVEL_N = 30  # smallest category level drawn in the category figure
PLOT_ROWS = 5000  # occupants sampled for scatter figures (tables use every occupant)
BAR = "#257de0"
RAMP = LinearSegmentedColormap.from_list("blue", ["#cce3fd", "#519ced", "#1757ac", "#0e3d7e"])


# ---------------------------------------------------------------------------
# SHAP values
# ---------------------------------------------------------------------------
def shap_matrix(model, X):
    """(encoded matrix, column names, SHAP values, bias) for the rows of X."""
    preprocess = model.named_steps["preprocess"]
    encoded = np.asarray(preprocess.transform(X), dtype=float)
    names = list(preprocess.get_feature_names_out())
    booster = model.named_steps["model"].get_booster()
    matrix = xgboost.DMatrix(encoded)
    contribs = booster.predict(matrix, pred_contribs=True)
    margin = booster.predict(matrix, output_margin=True)
    worst = float(np.abs(contribs.sum(axis=1) - margin).max())
    assert worst <= ADDITIVITY_TOL, f"SHAP values do not add up to the log-odds ({worst})"
    print(f"SHAP additivity: max |bias + sum - log-odds| = {worst:.2e}")
    assert contribs.shape[1] == len(names) + 1
    return encoded, names, contribs[:, :-1], float(contribs[0, -1]), worst


def column_info(names, fields, numeric_fields):
    rows = []
    for name in names:
        field = modeling.original_field(name, fields)
        short = name.split("__", 1)[1]
        if short == "missingindicator_" + field:
            kind, level = "missing_indicator", "missing"
        elif field in numeric_fields:
            kind, level = "numeric", ""
        else:
            kind, level = "category", short.removeprefix(field + "_")
        rows.append({"encoded_feature": name, "field": field, "kind": kind, "level": level})
    return pd.DataFrame(rows)


def gain_by_field(data, block):
    """XGBoost gain importance per field, as saved by stage 7 (None if absent)."""
    path = block_dir(posthoc.SOURCE, data.population, data.year, block)
    path = path / f"feature_importances_{block}_{data.year}.csv"
    if not path.exists():
        return None
    return pd.read_csv(path).groupby("field")["importance"].sum()


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def tidy(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", color="#e5e5e5", linewidth=0.6)
    ax.set_axisbelow(True)


def plot_importance(by_field, title):
    top = by_field.head(TOP_FIELDS).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.5, 0.32 * len(top) + 1.2))
    ax.barh(top.index, top.mean_abs_shap, color=BAR, height=0.7)
    for y, v in enumerate(top.mean_abs_shap):
        ax.text(v, y, f" {v:.3f}", va="center", fontsize=8, color="#444444")
    ax.set_xlabel("Mean |SHAP| (log-odds of fatal), holdout occupants")
    ax.set_title(title, fontsize=10)
    tidy(ax)
    fig.tight_layout()
    return fig


def plot_beeswarm(encoded, values, info, by_column, sample, title):
    top = by_column.head(TOP_COLUMNS).index[::-1]
    rng = np.random.default_rng(SEED)
    fig, ax = plt.subplots(figsize=(8.5, 0.42 * len(top) + 1.4))
    for y, j in enumerate(top):
        x = values[sample, j]
        v = encoded[sample, j]
        lo, hi = np.nanmin(v), np.nanmax(v)
        colour = (v - lo) / (hi - lo) if hi > lo else np.zeros_like(v)
        ax.scatter(
            x,
            y + rng.uniform(-0.3, 0.3, len(x)),
            c=colour,
            cmap=RAMP,
            vmin=0,
            vmax=1,
            s=4,
            alpha=0.6,
            linewidths=0,
            rasterized=True,
        )
    ax.axvline(0, color="#999999", linewidth=0.8)
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels([info.loc[j, "encoded_feature"].split("__", 1)[1] for j in top])
    ax.set_xlabel("SHAP value (log-odds of fatal); right = higher predicted risk")
    sm = plt.cm.ScalarMappable(cmap=RAMP)
    bar = fig.colorbar(sm, ax=ax, pad=0.01, aspect=40)
    bar.set_label("Column value (low -> high; category columns: off -> on)")
    ax.set_title(title, fontsize=10)
    tidy(ax)
    fig.tight_layout()
    return fig


def plot_dependence(X, field_shap, numeric_fields, sample, title):
    fields = [f for f in numeric_fields if f in field_shap.columns]
    fig, axes = plt.subplots(1, len(fields), figsize=(3.6 * len(fields), 3.4), squeeze=False)
    for ax, field in zip(axes[0], fields):
        x = X[field].to_numpy(dtype=float)[sample]
        y = field_shap[field].to_numpy()[sample]
        keep = ~np.isnan(x)
        ax.scatter(x[keep], y[keep], s=4, alpha=0.35, color=BAR, linewidths=0, rasterized=True)
        ax.axhline(0, color="#999999", linewidth=0.8)
        ax.set_xlabel(field)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0][0].set_ylabel("Field SHAP (log-odds)")
    fig.suptitle(title, fontsize=10)
    fig.tight_layout()
    return fig


def plot_categories(by_category, fields, title):
    fig, axes = plt.subplots(1, len(fields), figsize=(4.6 * len(fields), 5), squeeze=False)
    for ax, field in zip(axes[0], fields):
        t = by_category[(by_category.field == field) & (by_category.n >= MIN_LEVEL_N)]
        t = t.sort_values("mean_field_shap")
        colours = np.where(t.mean_field_shap >= 0, "#ec4647", BAR)
        labels = [f"{v} (n={n:,})" for v, n in zip(t.value, t.n)]
        ax.barh(labels, t.mean_field_shap, color=colours, height=0.7)
        ax.axvline(0, color="#999999", linewidth=0.8)
        ax.set_title(f"{field} (code)", fontsize=9)
        ax.set_xlabel("Mean field SHAP (log-odds)")
        tidy(ax)
    fig.suptitle(
        title + f"\nRed raises, blue lowers predicted risk; levels with n >= " f"{MIN_LEVEL_N}",
        fontsize=10,
    )
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
def summary_text(data, block, by_field, bias, worst, rho, check):
    top = by_field.head(10)
    rows = "\n".join(
        f"| {i} | {f} | {r.mean_abs_shap:.4f} | {r.share:.1%} | {r.mean_shap:+.4f} | "
        f"{'' if pd.isna(r.gain_rank) else int(r.gain_rank)} |"
        for i, (f, r) in enumerate(top.iterrows(), start=1)
    )
    reproduced = (
        "reproduced the saved holdout metrics exactly"
        if check["reproduced"]
        else f"differs from the saved holdout AP by {check['ap_difference']:+.4f} "
        "(different platform or library build; see refit_check)"
    )
    rho_text = "not available" if rho is None else f"{rho:.3f}"
    return (
        f"**SHAP for the tuned XGBoost**, {data.population} population, FARS {data.year}, "
        f"block {block} ({len(data.features['blocks'][block])} features).\n\n"
        f"**Refit:** settings {check['params']}; {reproduced}.\n\n"
        f"**Explained:** all {len(data.y_test):,} holdout occupants (exact TreeSHAP from "
        f"XGBoost). Bias (base log-odds) {bias:.3f}; bias + SHAP equals the model's "
        f"log-odds within {worst:.1e}.\n\n"
        "| Rank | Field | Mean abs SHAP | Share | Mean SHAP | Gain rank |\n"
        "|---|---|---|---|---|---|\n" + rows + "\n\n"
        f"**Spearman correlation of field rankings, SHAP vs gain:** {rho_text}.\n\n"
        "Field SHAP sums the field's one-hot and missing-indicator columns. Units are "
        "log-odds of a fatal outcome. Associations within FARS fatal crashes, not causal "
        "effects; related fields can share credit.\n"
    )


def run_block(data, block):
    print(f"\n{'-' * 20} SHAP, FARS {data.year}, block {block} {'-' * 20}")
    out_dir = block_dir(MODEL, data.population, data.year, block)
    fig_dir = out_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    def out(name, ext="csv"):
        return out_dir / f"{name}_{block}_{data.year}.{ext}"

    model, check = posthoc.refit_tuned(data, block)
    _, X_test = data.X(block)
    fields = data.features["blocks"][block]
    numeric_fields, categorical_fields = data.column_types(block)
    encoded, names, values, bias, worst = shap_matrix(model, X_test)
    info = column_info(names, fields, numeric_fields)

    # Per encoded column
    active = np.where(info.kind.to_numpy() == "numeric", True, encoded != 0)
    on = np.where(active, values, np.nan)
    off = np.where(~active, values, np.nan)
    with warnings.catch_warnings():  # a column never on (or never off) -> NaN mean
        warnings.simplefilter("ignore", RuntimeWarning)
        by_column = info.assign(
            n_active=active.sum(axis=0),
            mean_abs_shap=np.abs(values).mean(axis=0),
            mean_shap=values.mean(axis=0),
            mean_shap_when_on=np.nanmean(on, axis=0),
            mean_shap_when_off=np.nanmean(off, axis=0),
        )
    by_column = by_column.sort_values("mean_abs_shap", ascending=False)
    by_column.to_csv(out("shap_by_column"), index=False)

    # Per original field (SHAP is additive, so sum the field's columns)
    field_shap = pd.DataFrame(values, columns=names).T.groupby(info.field.to_numpy()).sum().T
    by_field = pd.DataFrame(
        {"mean_abs_shap": field_shap.abs().mean(), "mean_shap": field_shap.mean()}
    ).sort_values("mean_abs_shap", ascending=False)
    by_field["share"] = by_field.mean_abs_shap / by_field.mean_abs_shap.sum()
    by_field["rank"] = np.arange(1, len(by_field) + 1)
    gain = gain_by_field(data, block)
    rho = None
    if gain is not None:
        by_field["gain_importance"] = gain.reindex(by_field.index)
        by_field["gain_rank"] = by_field.gain_importance.rank(ascending=False, method="min")
        rho = float(by_field["mean_abs_shap"].corr(by_field.gain_importance, method="spearman"))
    else:
        by_field["gain_importance"] = by_field["gain_rank"] = np.nan
    assert set(by_field.index) == set(fields), "SHAP fields differ from the block"
    by_field.rename_axis("field").to_csv(out("shap_by_field"))

    # Per raw category value of each categorical field
    rows = []
    for field in categorical_fields:
        raw = X_test[field].astype(object).where(X_test[field].notna(), "missing")
        g = pd.DataFrame({"value": raw.to_numpy(), "s": field_shap[field].to_numpy()})
        g = g.groupby("value", sort=False).s.agg(["size", "mean"]).reset_index()
        rows.append(g.rename(columns={"size": "n", "mean": "mean_field_shap"}).assign(field=field))
    by_category = pd.concat(rows, ignore_index=True)[["field", "value", "n", "mean_field_shap"]]
    by_category.to_csv(out("shap_by_category"), index=False)

    # Figures (scatter figures use a fixed random sample of occupants)
    rng = np.random.default_rng(SEED)
    sample = np.sort(rng.choice(len(values), min(PLOT_ROWS, len(values)), replace=False))
    label = f"Tuned XGBoost, {data.population} {data.year}, {block}"
    save_fig(
        plot_importance(by_field, f"SHAP field importance: {label}"),
        fig_dir / f"shap_importance_{block}_{data.year}.png",
    )
    save_fig(
        plot_beeswarm(encoded, values, info, by_column, sample, f"SHAP values: {label}"),
        fig_dir / f"shap_beeswarm_{block}_{data.year}.png",
    )
    save_fig(
        plot_dependence(X_test, field_shap, numeric_fields, sample, f"SHAP dependence: {label}"),
        fig_dir / f"shap_dependence_{block}_{data.year}.png",
    )
    top_cat = [f for f in by_field.index if f in categorical_fields][:TOP_CATEGORICAL]
    save_fig(
        plot_categories(by_category, top_cat, f"SHAP by category: {label}"),
        fig_dir / f"shap_categories_{block}_{data.year}.png",
    )

    modeling.show(by_field.head(10))
    summary = summary_text(data, block, by_field, bias, worst, rho, check)
    out("summary", "md").write_text(summary)
    print(summary)
    print("Outputs in", out_dir.relative_to(PROJECT_DIR))
    return check


def plot_by_year(table, block, population, top=15):
    wide = table.pivot(index="field", columns="year", values="mean_abs_shap")
    wide = wide.loc[wide.mean(axis=1).sort_values(ascending=False).index[:top]]
    fig, ax = plt.subplots(figsize=(1.0 * wide.shape[1] + 3.5, 0.38 * len(wide) + 1.5))
    im = ax.imshow(wide.to_numpy(), cmap=RAMP, aspect="auto")
    ax.set_xticks(range(wide.shape[1]))
    ax.set_xticklabels(wide.columns)
    ax.set_yticks(range(len(wide)))
    ax.set_yticklabels(wide.index)
    vmax = np.nanmax(wide.to_numpy())
    for i in range(wide.shape[0]):
        for j in range(wide.shape[1]):
            v = wide.iat[i, j]
            if not np.isnan(v):
                ax.text(
                    j,
                    i,
                    f"{v:.2f}",
                    ha="center",
                    va="center",
                    fontsize=7,
                    color="white" if v > 0.55 * vmax else "#191919",
                )
    fig.colorbar(im, ax=ax, pad=0.01).set_label("Mean |SHAP| (log-odds)")
    ax.set_title(
        f"SHAP field importance by year, tuned XGBoost, {population}, {block}", fontsize=10
    )
    fig.tight_layout()
    return fig


def summarize_years(population):
    """Stack every year's field table (whatever has been run) and summarize by block."""
    rows = []
    for path in sorted((RESULTS_DIR / MODEL / population).glob("*/*/shap_by_field_*.csv")):
        year, block = int(path.parent.parent.name), path.parent.name
        rows.append(pd.read_csv(path).assign(year=year, block=block))
    if not rows:
        return
    stacked = pd.concat(rows, ignore_index=True)
    first = ["year", "block", "field", "rank"]
    stacked = stacked[first + [c for c in stacked.columns if c not in first]]
    out_dir = RESULTS_DIR / MODEL / population
    stacked.to_csv(out_dir / "shap_all_years.csv", index=False)
    g = stacked.groupby(["block", "field"])
    means = pd.DataFrame(
        {
            "years": g.year.nunique(),
            "mean_abs_shap": g.mean_abs_shap.mean(),
            "mean_share": g.share.mean(),
            "mean_rank": g["rank"].mean(),
            "best_rank": g["rank"].min(),
            "worst_rank": g["rank"].max(),
            "years_in_top5": g["rank"].apply(lambda r: int((r <= 5).sum())),
        }
    ).reset_index()
    order = {b: i for i, b in enumerate(BLOCKS)}
    means = means.sort_values(
        ["block", "mean_abs_shap"],
        ascending=[True, False],
        key=lambda s: s.map(order) if s.name == "block" else s,
    )
    means.to_csv(out_dir / "shap_means.csv", index=False)
    for block, table in stacked.groupby("block"):
        save_fig(
            plot_by_year(table, block, population),
            out_dir / "figures" / f"shap_by_year_{block}.png",
        )
    print(f"Across-year SHAP tables refreshed ({stacked.year.nunique()} year(s))")


def run(year, population, blocks=None):
    print(f"\n=== SHAP for tuned XGBoost {year} ({population} population) ===")
    data = posthoc.load_checked(year, population)
    out_dir = results_dir(MODEL, population, year)
    print(posthoc.environment(out_dir, year))
    checks = [run_block(data, block) for block in blocks or BLOCKS]
    posthoc.save_refit_checks(checks, out_dir, year)
    summarize_years(population)


def main(years, population, blocks=None):
    for year in years:
        run(year, population, blocks)
