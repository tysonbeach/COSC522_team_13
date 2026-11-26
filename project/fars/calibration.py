"""Stage 8: calibration of the tuned XGBoost, one analysis per year and feature block.

Question: when the tuned XGBoost says an occupant has a 30% chance of dying, do about
30% of such occupants die? Ranking metrics (ROC-AUC, AP) cannot answer this.

Protocol (training data only for anything learned; the holdout is scored once):
  1. Refit the tuned XGBoost from best_params_<BLOCK>_<YEAR>.json on the training rows
     (posthoc.py; the refit is checked against the saved holdout metrics).
  2. Out-of-fold (OOF) training probabilities: the same tuned settings are fitted on
     four of the five saved grouped CV folds and predict the fifth, so every training
     occupant gets a probability from a model that never saw their crash.
  3. Three probability versions, all applied to the same refit model:
        uncalibrated  the model's own probabilities
        sigmoid       Platt scaling: logistic regression of FATAL on logit(probability)
        isotonic      isotonic regression of FATAL on probability (monotone steps)
     The calibration maps are fitted on the OOF training probabilities (the scheme of
     scikit-learn's CalibratedClassifierCV with ensemble=False) and then applied to the
     refit model's holdout probabilities.
  4. Method comparison without the holdout: cross-fitting over the OOF probabilities
     (fit each map on four folds' OOF probabilities, score it on the fifth). The
     pre-declared rule picks the lowest mean CV Brier score; a method must beat a
     simpler one (uncalibrated < sigmoid < isotonic) by more than SELECT_TOL to be
     chosen. The holdout table reports all three methods; it does not change the choice.
  5. Holdout: Brier score, log loss, expected calibration error (ECE, 10 equal-count
     bins), maximum bin error, calibration intercept and slope (logistic regression of
     FATAL on logit(probability); ideal 0 and 1), mean predicted risk against the
     observed fatal share, plus the shared metrics from modeling.evaluate. The
     prediction rule is unchanged: fatal when the probability is above 0.5, as
     XGBClassifier.predict does.

Calibration is about the holdout year and population only. A model that is well
calibrated here need not be calibrated in another year or state group (the transfer
tests), and none of this is causal.

Outputs (processed/results/xgboost_calibration/<POPULATION>/<YEAR>/):
    environment_<YEAR>.json, refit_check_<YEAR>.csv
    <BLOCK>/  (file names end _<BLOCK>_<YEAR>)
        calibration_cv_*.csv        cross-fitted OOF metrics per method and fold summary
        calibration_holdout_*.csv   holdout calibration + shared metrics per method
        reliability_bins_*.csv      holdout reliability table (10 equal-count bins)
        selected_method_*.json      method chosen by the CV rule, with its CV Brier
        summary_*.md
        figures/reliability_*.png
processed/results/xgboost_calibration/<POPULATION>/
    calibration_all_years.csv, calibration_means.csv   refreshed after every run
"""

import json

import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import cross_val_predict

from . import modeling, posthoc
from .config import BLOCKS, N_JOBS, PROJECT_DIR, RESULTS_DIR
from .figures import plt, save_fig
from .paths import block_dir, results_dir

MODEL = "xgboost_calibration"
METHODS = ["uncalibrated", "sigmoid", "isotonic"]  # simplest first (tie-break order)
N_BINS = 10  # equal-count bins for ECE and the reliability table
SELECT_TOL = 1e-4  # CV Brier improvement needed to prefer a more complex method
EPS = 1e-6  # probabilities clipped to [EPS, 1 - EPS] before logit / log loss
COLORS = {"uncalibrated": "#257de0", "sigmoid": "#f47230", "isotonic": "#00b894"}
MARKERS = {"uncalibrated": "o", "sigmoid": "s", "isotonic": "^"}


# ---------------------------------------------------------------------------
# Calibration maps: fit(p, y) on training probabilities, transform(p) -> new p
# ---------------------------------------------------------------------------
def logit(p):
    p = np.clip(np.asarray(p, dtype=float), EPS, 1 - EPS)
    return np.log(p / (1 - p))


class Identity:
    def fit(self, p, y):
        return self

    def transform(self, p):
        return np.asarray(p, dtype=float)


class Sigmoid:
    """Platt scaling on the log-odds scale, unpenalized."""

    def fit(self, p, y):
        self.lr = LogisticRegression(C=np.inf, max_iter=1000).fit(logit(p)[:, None], y)
        return self

    def transform(self, p):
        return self.lr.predict_proba(logit(p)[:, None])[:, 1]


class Isotonic:
    def fit(self, p, y):
        self.iso = IsotonicRegression(y_min=0, y_max=1, out_of_bounds="clip").fit(p, y)
        return self

    def transform(self, p):
        return self.iso.predict(np.asarray(p, dtype=float))


MAPS = {"uncalibrated": Identity, "sigmoid": Sigmoid, "isotonic": Isotonic}


class Calibrated:
    """A fitted pipeline followed by a calibration map, usable by modeling.evaluate."""

    classes_ = np.array([0, 1])

    def __init__(self, model, calibration_map):
        self.model, self.map = model, calibration_map

    def predict_proba(self, X):
        p = self.map.transform(self.model.predict_proba(X)[:, 1])
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] > 0.5).astype(int)  # XGBClassifier's rule


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def reliability_bins(y, p, n_bins=N_BINS):
    """Equal-count bins (ties split by order) with mean predicted and observed fatal share."""
    y, p = np.asarray(y), np.asarray(p, dtype=float)
    order = pd.Series(p).rank(method="first").to_numpy()
    bins = pd.qcut(order, n_bins, labels=False)
    table = (
        pd.DataFrame({"bin": bins + 1, "p": p, "y": y})
        .groupby("bin")
        .agg(
            n=("y", "size"),
            p_min=("p", "min"),
            p_max=("p", "max"),
            mean_predicted=("p", "mean"),
            observed=("y", "mean"),
        )
        .reset_index()
    )
    table["gap"] = table["observed"] - table["mean_predicted"]
    return table


def calibration_line(y, p):
    """Intercept and slope of a logistic regression of y on logit(p); ideal 0 and 1."""
    lr = LogisticRegression(C=np.inf, max_iter=1000).fit(logit(p)[:, None], y)
    return float(lr.intercept_[0]), float(lr.coef_[0, 0])


def calibration_metrics(y, p):
    y, p = np.asarray(y), np.asarray(p, dtype=float)
    bins = reliability_bins(y, p)
    intercept, slope = calibration_line(y, p)
    return {
        "n": len(y),
        "observed_fatal_share": y.mean(),
        "mean_predicted": p.mean(),
        "brier": brier_score_loss(y, p),
        "brier_no_skill": y.mean() * (1 - y.mean()),  # always predicting the fatal share
        "log_loss": log_loss(y, np.clip(p, EPS, 1 - EPS), labels=[0, 1]),
        "ece": float((bins.n * bins.gap.abs()).sum() / bins.n.sum()),
        "max_bin_error": float(bins.gap.abs().max()),
        "calibration_intercept": intercept,
        "calibration_slope": slope,
        "roc_auc": roc_auc_score(y, p),
        "pr_auc_ap": average_precision_score(y, p),
    }


# ---------------------------------------------------------------------------
# Training-only steps
# ---------------------------------------------------------------------------
def oof_probabilities(data, block):
    """Fatal probability for every training occupant from the fold that held it out."""
    X_train, _ = data.X(block)
    proba = cross_val_predict(
        posthoc.make_tuned(data, block),
        X_train,
        data.y_train,
        cv=data.cv_splits,
        method="predict_proba",
        n_jobs=N_JOBS,
    )
    return proba[:, 1]


def cross_fitted(data, p_oof):
    """Each method's maps fitted on four folds' OOF probabilities, scored on the fifth."""
    y = data.y_train.to_numpy()
    rows = []
    for fold, (_, val_i) in enumerate(data.cv_splits, start=1):
        fit_mask = np.ones(len(y), dtype=bool)
        fit_mask[val_i] = False
        for method in METHODS:
            m = MAPS[method]().fit(p_oof[fit_mask], y[fit_mask])
            rows.append(
                {
                    "fold": fold,
                    "method": method,
                    **calibration_metrics(y[val_i], m.transform(p_oof[val_i])),
                }
            )
    folds = pd.DataFrame(rows)
    stats = folds.drop(columns="fold").groupby("method", sort=False)
    table = stats.mean().add_prefix("cv_").join(stats.std(ddof=1).add_prefix("cv_sd_"))
    return table.loc[METHODS]


def select_method(cv_table):
    """Lowest mean CV Brier; a more complex method must win by more than SELECT_TOL."""
    chosen = METHODS[0]
    for method in METHODS[1:]:
        if cv_table.loc[method, "cv_brier"] < cv_table.loc[chosen, "cv_brier"] - SELECT_TOL:
            chosen = method
    return chosen


# ---------------------------------------------------------------------------
# Figure and summary
# ---------------------------------------------------------------------------
def plot_reliability(bins_by_method, p_uncal, data, block):
    fig, (ax, hist_ax) = plt.subplots(
        2, 1, figsize=(6.5, 7.5), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )
    ax.plot([0, 1], [0, 1], color="#999999", linestyle="--", linewidth=1, label="Perfect")
    for method, bins in bins_by_method.items():
        ax.plot(
            bins.mean_predicted,
            bins.observed,
            color=COLORS[method],
            linewidth=2,
            marker=MARKERS[method],
            markersize=6,
            label=method,
        )
    ax.set_ylabel("Observed fatal share in bin")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(color="#e5e5e5", linewidth=0.6)
    ax.legend(frameon=False)
    ax.set_title(
        f"Holdout reliability, tuned XGBoost, {data.population} {data.year}, {block}\n"
        f"({N_BINS} equal-count bins; maps fitted on OOF training probabilities)",
        fontsize=10,
    )
    hist_ax.hist(
        p_uncal,
        bins=40,
        range=(0, 1),
        color=COLORS["uncalibrated"],
        edgecolor="white",
        linewidth=0.5,
    )
    hist_ax.set_xlabel("Predicted fatal probability")
    hist_ax.set_ylabel("Occupants\n(uncalibrated)")
    for a in (ax, hist_ax):
        a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def summary_text(data, block, cv_table, holdout, chosen, check):
    def line(method):
        h = holdout.loc[method]
        return (
            f"| {method} | {cv_table.loc[method, 'cv_brier']:.4f} | {h.brier:.4f} | "
            f"{h.log_loss:.4f} | {h.ece:.4f} | {h.calibration_intercept:.3f} | "
            f"{h.calibration_slope:.3f} | {h.mean_predicted:.3f} | {h.roc_auc:.4f} | "
            f"{h.pr_auc_ap:.4f} | {h.macro_f1:.4f} |"
        )

    reproduced = (
        "reproduced the saved holdout metrics exactly"
        if check["reproduced"]
        else f"differs from the saved holdout AP by {check['ap_difference']:+.4f} "
        "(different platform or library build; see refit_check)"
    )
    return (
        f"**Calibration of the tuned XGBoost**, {data.population} population, FARS "
        f"{data.year}, block {block} ({len(data.features['blocks'][block])} features).\n\n"
        f"**Refit:** settings {check['params']}; {reproduced}.\n\n"
        f"**Holdout:** {len(data.y_test):,} occupants, observed fatal share "
        f"{data.y_test.mean():.3f}; no-skill Brier "
        f"{holdout.loc['uncalibrated', 'brier_no_skill']:.4f}.\n\n"
        "| Method | CV Brier | Brier | Log loss | ECE | Intercept | Slope | Mean predicted "
        "| ROC-AUC | AP | Macro-F1 |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(line(m) for m in METHODS)
        + f"\n\n**Method chosen by the CV rule (training data only):** {chosen}. "
        "Holdout values are reported for all methods and did not affect the choice.\n\n"
        "ECE: mean absolute gap between predicted and observed fatal share over "
        f"{N_BINS} equal-count bins. Intercept/slope: logistic regression of FATAL on "
        "logit(probability); 0 and 1 are ideal, slope < 1 means over-confident. "
        "Associations within FARS fatal crashes, not causal effects.\n"
    )


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
def run_block(data, block):
    print(f"\n{'-' * 20} Calibration, FARS {data.year}, block {block} {'-' * 20}")
    out_dir = block_dir(MODEL, data.population, data.year, block)
    out_dir.mkdir(parents=True, exist_ok=True)

    def out(name, ext="csv"):
        return out_dir / f"{name}_{block}_{data.year}.{ext}"

    model, check = posthoc.refit_tuned(data, block)
    _, X_test = data.X(block)
    y_train, y_test = data.y_train.to_numpy(), data.y_test

    p_oof = oof_probabilities(data, block)
    cv_table = cross_fitted(data, p_oof)
    oof_raw = pd.DataFrame(calibration_metrics(y_train, p_oof), index=["oof_uncalibrated"])
    pd.concat([cv_table, oof_raw.add_prefix("pooled_")], axis=1).rename_axis("method").to_csv(
        out("calibration_cv")
    )
    chosen = select_method(cv_table)
    modeling.show(cv_table[["cv_brier", "cv_sd_brier", "cv_log_loss", "cv_ece"]])

    maps = {m: MAPS[m]().fit(p_oof, y_train) for m in METHODS}
    models = {m: Calibrated(model, maps[m]) for m in METHODS}
    shared, _, scores = modeling.evaluate(models, X_test, y_test)
    calib = pd.DataFrame({m: calibration_metrics(y_test, scores[m]) for m in METHODS}).T
    holdout = calib.join(shared.drop(columns=["roc_auc", "pr_auc_ap"]))
    holdout.rename_axis("method").to_csv(out("calibration_holdout"))
    modeling.show(holdout[["brier", "log_loss", "ece", "calibration_slope", "roc_auc"]])

    bins = {m: reliability_bins(y_test, scores[m]) for m in METHODS}
    pd.concat([b.assign(method=m) for m, b in bins.items()]).to_csv(
        out("reliability_bins"), index=False
    )
    selected = {
        "selected_method": chosen,
        "rule": f"lowest mean CV Brier; more complex method must win by > {SELECT_TOL}",
        "cv_brier": cv_table["cv_brier"].to_dict(),
    }
    out("selected_method", "json").write_text(json.dumps(selected, indent=2))
    save_fig(
        plot_reliability(bins, scores["uncalibrated"], data, block),
        out_dir / "figures" / f"reliability_{block}_{data.year}.png",
    )
    summary = summary_text(data, block, cv_table, holdout, chosen, check)
    out("summary", "md").write_text(summary)
    print(summary)
    print("Outputs in", out_dir.relative_to(PROJECT_DIR))
    return check


def summarize_years(population):
    """Stack every year's holdout table (whatever has been run) and average by block."""
    rows = []
    for path in sorted((RESULTS_DIR / MODEL / population).glob("*/*/calibration_holdout_*.csv")):
        year, block = int(path.parent.parent.name), path.parent.name
        table = pd.read_csv(path)
        selected = json.loads((path.parent / f"selected_method_{block}_{year}.json").read_text())[
            "selected_method"
        ]
        rows.append(table.assign(year=year, block=block, selected=table.method == selected))
    if not rows:
        return
    stacked = pd.concat(rows, ignore_index=True)
    first = ["year", "block", "method", "selected"]
    stacked = stacked[first + [c for c in stacked.columns if c not in first]]
    out_dir = RESULTS_DIR / MODEL / population
    stacked.to_csv(out_dir / "calibration_all_years.csv", index=False)
    cols = [
        "brier",
        "brier_no_skill",
        "log_loss",
        "ece",
        "max_bin_error",
        "calibration_intercept",
        "calibration_slope",
        "mean_predicted",
        "observed_fatal_share",
        "roc_auc",
        "pr_auc_ap",
        "macro_f1",
    ]
    means = stacked.groupby(["block", "method"])[cols].mean()
    means["years"] = stacked.groupby(["block", "method"]).year.nunique()
    means["times_selected"] = stacked.groupby(["block", "method"]).selected.sum()
    order = {b: i for i, b in enumerate(BLOCKS)}
    means = means.reset_index().sort_values(
        ["block", "method"],
        key=lambda s: (
            s.map(order) if s.name == "block" else s.map({m: i for i, m in enumerate(METHODS)})
        ),
    )
    means.to_csv(out_dir / "calibration_means.csv", index=False)
    print(f"Across-year calibration tables refreshed ({stacked.year.nunique()} year(s))")


def run(year, population, blocks=None):
    print(f"\n=== Calibration of tuned XGBoost {year} ({population} population) ===")
    data = posthoc.load_checked(year, population)
    out_dir = results_dir(MODEL, population, year)
    print(posthoc.environment(out_dir, year))
    checks = [run_block(data, block) for block in blocks or BLOCKS]
    posthoc.save_refit_checks(checks, out_dir, year)
    summarize_years(population)


def main(years, population, blocks=None):
    for year in years:
        run(year, population, blocks)
