**SHAP for the tuned XGBoost**, restricted population, FARS 2016, block AB_crash (38 features).

**Refit:** settings {"model__colsample_bytree": 0.8, "model__learning_rate": 0.05, "model__max_depth": 6, "model__n_estimators": 500, "model__subsample": 0.8}; differs from the saved holdout AP by +0.0015 (different platform or library build; see refit_check).

**Explained:** all 10,522 holdout occupants (exact TreeSHAP from XGBoost). Bias (base log-odds) -0.807; bias + SHAP equals the model's log-odds within 8.1e-06.

| Rank | Field | Mean abs SHAP | Share | Mean SHAP | Gain rank |
|---|---|---|---|---|---|
| 1 | REST_USE | 0.5463 | 13.6% | -0.0915 | 5 |
| 2 | AGE | 0.4521 | 11.3% | -0.0203 | 31 |
| 3 | PERMVIT | 0.3915 | 9.8% | -0.0373 | 23 |
| 4 | BODY_TYP | 0.3605 | 9.0% | -0.0584 | 2 |
| 5 | HARM_EV | 0.3311 | 8.3% | -0.1968 | 3 |
| 6 | P_CRASH2 | 0.2122 | 5.3% | -0.0973 | 1 |
| 7 | PCRASH5 | 0.2057 | 5.1% | +0.0021 | 8 |
| 8 | IMPACT1 | 0.1950 | 4.9% | -0.0470 | 4 |
| 9 | VSPD_LIM | 0.1658 | 4.1% | -0.0118 | 37 |
| 10 | MOD_YEAR | 0.1360 | 3.4% | -0.0176 | 38 |

**Spearman correlation of field rankings, SHAP vs gain:** 0.297.

Field SHAP sums the field's one-hot and missing-indicator columns. Units are log-odds of a fatal outcome. Associations within FARS fatal crashes, not causal effects; related fields can share credit.
