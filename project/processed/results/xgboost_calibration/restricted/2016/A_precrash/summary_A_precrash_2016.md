**Calibration of the tuned XGBoost**, restricted population, FARS 2016, block A_precrash (25 features).

**Refit:** settings {"model__colsample_bytree": 0.8, "model__learning_rate": 0.05, "model__max_depth": 6, "model__n_estimators": 200, "model__subsample": 0.8}; differs from the saved holdout AP by -0.0019 (different platform or library build; see refit_check).

**Holdout:** 10,522 occupants, observed fatal share 0.314; no-skill Brier 0.2153.

| Method | CV Brier | Brier | Log loss | ECE | Intercept | Slope | Mean predicted | ROC-AUC | AP | Macro-F1 |
|---|---|---|---|---|---|---|---|---|---|---|
| uncalibrated | 0.1640 | 0.1635 | 0.4949 | 0.0172 | 0.072 | 1.065 | 0.309 | 0.7992 | 0.6355 | 0.6867 |
| sigmoid | 0.1640 | 0.1634 | 0.4946 | 0.0154 | 0.042 | 1.005 | 0.307 | 0.7992 | 0.6355 | 0.6902 |
| isotonic | 0.1642 | 0.1634 | 0.4964 | 0.0121 | 0.030 | 0.982 | 0.307 | 0.7991 | 0.6311 | 0.6932 |

**Method chosen by the CV rule (training data only):** uncalibrated. Holdout values are reported for all methods and did not affect the choice.

ECE: mean absolute gap between predicted and observed fatal share over 10 equal-count bins. Intercept/slope: logistic regression of FATAL on logit(probability); 0 and 1 are ideal, slope < 1 means over-confident. Associations within FARS fatal crashes, not causal effects.
