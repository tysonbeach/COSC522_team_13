**Calibration of the tuned XGBoost**, restricted population, FARS 2016, block ABC_post (44 features).

**Refit:** settings {"model__colsample_bytree": 0.8, "model__learning_rate": 0.05, "model__max_depth": 6, "model__n_estimators": 500, "model__subsample": 0.8}; differs from the saved holdout AP by -0.0014 (different platform or library build; see refit_check).

**Holdout:** 10,522 occupants, observed fatal share 0.314; no-skill Brier 0.2153.

| Method | CV Brier | Brier | Log loss | ECE | Intercept | Slope | Mean predicted | ROC-AUC | AP | Macro-F1 |
|---|---|---|---|---|---|---|---|---|---|---|
| uncalibrated | 0.1221 | 0.1208 | 0.3742 | 0.0126 | 0.018 | 1.029 | 0.313 | 0.8954 | 0.7855 | 0.7929 |
| sigmoid | 0.1222 | 0.1208 | 0.3741 | 0.0119 | 0.017 | 1.011 | 0.312 | 0.8954 | 0.7855 | 0.7930 |
| isotonic | 0.1221 | 0.1207 | 0.3748 | 0.0092 | 0.012 | 0.997 | 0.312 | 0.8953 | 0.7794 | 0.7977 |

**Method chosen by the CV rule (training data only):** uncalibrated. Holdout values are reported for all methods and did not affect the choice.

ECE: mean absolute gap between predicted and observed fatal share over 10 equal-count bins. Intercept/slope: logistic regression of FATAL on logit(probability); 0 and 1 are ideal, slope < 1 means over-confident. Associations within FARS fatal crashes, not causal effects.
