# Development and modeling guide

These instructions apply throughout this repository, to teammates and their coding
assistants. Read [PROJECT_LOG.md](PROJECT_LOG.md) before starting work: its Current
step and latest dated handoff describe the active task. This guide holds stable
working conventions; the log holds changing status, results, and decisions. If the
code, guide, and log disagree, inspect the evidence and raise the discrepancy before
changing the study protocol.

## Skill notifications

Before each skill use, notify the user in commentary with only the skill's name.
Do not add an explanation, description, or other text to the skill notification.

## Development structure

- Put reusable implementation in `project/fars/`. Keep numbered scripts in
  `project/scripts/` as thin entry points using the shared CLI conventions.
- Reuse `config.py` for feature blocks, exclusions, years, and seed; `paths.py` for
  file locations; `cohort.py` for population rules; `recodes.py` for harmonization;
  and `modeling.py` for splits, preprocessing pipelines, evaluation, and shared plots.
  Model modules should contain model-specific estimators, tuning grids, and outputs.
- Follow existing names and patterns. Preserve CRLF line endings in Python files
  and the Black line length of 100 configured in `pyproject.toml`. Avoid unrelated
  reformatting or moving files as part of a modeling change.
- Treat `project/notebooks/` as historical work, not the production pipeline.
  In `decision_tree_v2.ipynb`, code cells 1–11 belong to Tyson and must remain
  untouched unless explicitly requested.
- Inspect Git status before editing. Preserve teammates' staged, unstaged, and
  untracked work. Work on a personal branch and submit a PR into `main`; do not
  commit or push unless requested. Use `codex/` for new assistant-created branches
  unless the teammate supplies another name.

## Study and population rules

The question is which occupants survive within crashes that killed at least one
person. FARS 2016–2023 records are joined at person, vehicle, and crash levels, with
one row per modeled driver/passenger. `FATAL=1` is fatal injury; `FATAL=0` is a known
nonfatal outcome. Findings are associations within fatal crashes, not causal effects
or estimates for all road crashes.

- Maintain both `full` and `restricted` populations. `restricted` is the current
  refined population; `full` remains the comparison population.
- Apply shared cohort cleaning first. For `restricted`, remove motorcycle occupants
  with `BODY_TYP` 80–89, then remove crashes with only one remaining modeled occupant.
  Count occupants across vehicles by `YEAR`, `STATE`, and `ST_CASE`. ATVs (90) and
  snowmobiles (91) are outside the motorcycle exclusion.
- Preserve speed exclusions `VSPD_LIM` 0, 98, 99. Code 0 does not mean 0 mph; its
  representation is a deferred study decision. Do not reintroduce the `NUMOCCS`
  row-exclusion rule.
- Preserve the three nested blocks: `A_precrash`, `AB_crash`, `ABC_post`. Current
  effective counts are 25, 38, and 44 features. `PERSONS`, `PEDS`, `NUMOCCS`, and
  `PERNOTMVIT` are dropped; `PERMVIT` and `VE_FORMS` remain. `VE_TOTAL` is outside
  the blocks. Read actual definitions from `config.py`; do not duplicate them.
- Preserve harmonization rules and per-year audits. The multicollinearity stage
  reports associations; it does not automatically remove predictors.
- Discuss changes to cohort definitions, labels, exclusions, recodes, feature blocks,
  splits, or model-selection rules before implementing them, unless the current
  request already authorizes the specific change.

## Modeling protocol

- Use the shared 80/20 crash-grouped holdout split with seed 522, and five-fold
  `StratifiedGroupKFold` within training data. No crash may cross train/test or
  training/validation boundaries.
- Use identical population-specific occupants, holdout assignments, and CV folds
  across feature blocks and model families. Compare generated assignments against
  the existing decision-tree split manifest before comparing models. Do not silently
  replace a mismatched manifest. Full and restricted have separate splits.
- Fit imputation, encoding, and any learned preprocessing only on training data,
  inside the pipeline and CV folds. Keep IDs and labels out of predictors.
- Select hyperparameters by mean CV average precision (`refit="ap"`). Do not tune
  against the holdout or select settings based on its scores. Score the selected
  model on holdout under the agreed protocol.
- Preserve the current no-class-weight setup unless a change is explicitly agreed.
  Document model-specific tuning grids before examining holdout results.
- Report accuracy, balanced accuracy, fatal precision/recall/F1, `macro_f1`, ROC-AUC,
  average precision, and confusion counts through shared evaluation. Existing `f1`
  means fatal-class F1; `macro_f1` equally averages nonfatal and fatal F1. Preserve
  the existing prediction rule; any threshold tuning belongs on training data.
- Report holdout fatal prevalence as the no-skill AP reference. Different raw AP
  values can reflect different prevalence. Full/restricted score differences do not
  isolate a causal motorcycle effect.
- Generate comparable final results on the agreed machine in the `cosc522` conda
  environment. Do not mix teammate-machine outputs into the final comparison;
  library/platform differences can change fitted trees. Record environment versions.

## Outputs and validation

Use the helpers in `paths.py` and the established layout:

```text
project/processed/
  datasets/<POPULATION>/<YEAR>/
  reports/<REPORT>/<POPULATION>/<YEAR>/<BLOCK>/
  results/<MODEL>/<POPULATION>/<YEAR>/
    holdout_split_<YEAR>_seed522.csv
    <BLOCK>/<name>_<BLOCK>_<YEAR>.<extension>
    <BLOCK>/figures/
```

- Keep model families and populations in separate output directories. Include block
  and year in result filenames. Reuse established metric column names and provide
  a readable summary beside tables and figures.
- Track results, reports, feature metadata, cohort/recode audits, and small summary
  tables according to `.gitignore`. Keep raw data, joined parquet files, and dataset
  CSVs ignored. Do not stage generated files indiscriminately.
- After a modeling change, validate one year before running all eight. Check feature
  membership, cohort audit reconciliation, identity/label alignment, crash separation,
  split consistency, finite metrics, and required output files. Exercise relevant
  edge cases when changing cohort or metric logic.
- Regenerate affected preprocessing outputs when cohort, recodes, or features change.
  Label stale results clearly until their models have been rerun. Do not claim a
  check or run completed without observing its outcome.
- Reporting-only metrics may be reconstructed exactly from saved sufficient data
  (for example, macro-F1 from TN/FP/FN/TP). Verify the calculation and preserve all
  existing metrics. Never invent unavailable predictions or model results.

## Running and handing off work

From the repository root:

```bash
conda activate cosc522
# One-year pilot, restricted population; currently runs preprocessing + decision trees.
python project/scripts/run.py 2016 --population restricted
# All years; --mc also generates the multicollinearity reports.
python project/scripts/run.py full --population restricted --mc
python project/scripts/run.py full --population full --mc
```

Here the positional `full` means all configured years; `--population full` selects
the full cohort. Consult each script's `--help` and the log's How to run section.
As new model entry points are added, document their commands in the project log.

At handoff, update `PROJECT_LOG.md`: Last updated, Current step when it changes, and
one dated Log entry describing the change, checks actually performed, output paths,
remaining limitations, and the concrete next step. Keep stable instructions here
and current numeric results in the log. Tell the teammate which files changed and
whether results were regenerated. Keep pending work explicit; never mark a planned
model or analysis complete because its scaffolding exists.
