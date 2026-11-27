**SHAP for the tuned XGBoost**, restricted population, FARS 2016, block A_precrash (25 features).

**Refit:** settings {"model__colsample_bytree": 0.8, "model__learning_rate": 0.05, "model__max_depth": 6, "model__n_estimators": 200, "model__subsample": 0.8}; differs from the saved holdout AP by -0.0019 (different platform or library build; see refit_check).

**Explained:** all 10,522 holdout occupants (exact TreeSHAP from XGBoost). Bias (base log-odds) -0.805; bias + SHAP equals the model's log-odds within 3.6e-06.

| Rank | Field | Mean abs SHAP | Share | Mean SHAP | Gain rank |
|---|---|---|---|---|---|
| 1 | REST_USE | 0.5697 | 22.0% | -0.0862 | 2 |
| 2 | AGE | 0.4202 | 16.2% | -0.0216 | 21 |
| 3 | BODY_TYP | 0.3791 | 14.6% | -0.0528 | 1 |
| 4 | MOD_YEAR | 0.1738 | 6.7% | -0.0153 | 24 |
| 5 | PER_TYP | 0.1521 | 5.9% | +0.0115 | 16 |
| 6 | VSPD_LIM | 0.1352 | 5.2% | -0.0053 | 25 |
| 7 | RELJCT2 | 0.1280 | 4.9% | -0.0077 | 5 |
| 8 | TOW_VEH | 0.0846 | 3.3% | -0.0133 | 7 |
| 9 | RUR_URB | 0.0835 | 3.2% | -0.0032 | 12 |
| 10 | SEAT_POS | 0.0775 | 3.0% | -0.0070 | 3 |

**Spearman correlation of field rankings, SHAP vs gain:** 0.246.

Field SHAP sums the field's one-hot and missing-indicator columns. Units are log-odds of a fatal outcome. Associations within FARS fatal crashes, not causal effects; related fields can share credit.
