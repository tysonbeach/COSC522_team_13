**Calibration of the tuned XGBoost**, restricted population, FARS 2016, block AB_crash (38 features).

**Refit:** settings {"model__colsample_bytree": 0.8, "model__learning_rate": 0.05, "model__max_depth": 6, "model__n_estimators": 500, "model__subsample": 0.8}; differs from the saved holdout AP by +0.0015 (different platform or library build; see refit_check).

**Holdout:** 10,522 occupants, observed fatal share 0.314; no-skill Brier 0.2153.

| Method | CV Brier | Brier | Log loss | ECE | Intercept | Slope | Mean predicted | ROC-AUC | AP | Macro-F1 |
|---|---|---|---|---|---|---|---|---|---|---|
| uncalibrated | 0.1400 | 0.1389 | 0.4239 | 0.0133 | 0.053 | 1.045 | 0.309 | 0.8603 | 0.7311 | 0.7470 |
| sigmoid | 0.1400 | 0.1388 | 0.4237 | 0.0122 | 0.034 | 1.008 | 0.310 | 0.8603 | 0.7311 | 0.7492 |
| isotonic | 0.1401 | 0.1391 | 0.4270 | 0.0083 | 0.021 | 0.980 | 0.310 | 0.8597 | 0.7237 | 0.7437 |

**Method chosen by the CV rule (training data only):** uncalibrated. Holdout values are reported for all methods and did not affect the choice.

ECE: mean absolute gap between predicted and observed fatal share over 10 equal-count bins. Intercept/slope: logistic regression of FATAL on logit(probability); 0 and 1 are ideal, slope < 1 means over-confident. Associations within FARS fatal crashes, not causal effects.
