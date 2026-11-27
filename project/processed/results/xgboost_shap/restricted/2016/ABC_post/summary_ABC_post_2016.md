**SHAP for the tuned XGBoost**, restricted population, FARS 2016, block ABC_post (44 features).

**Refit:** settings {"model__colsample_bytree": 0.8, "model__learning_rate": 0.05, "model__max_depth": 6, "model__n_estimators": 500, "model__subsample": 0.8}; differs from the saved holdout AP by -0.0014 (different platform or library build; see refit_check).

**Explained:** all 10,522 holdout occupants (exact TreeSHAP from XGBoost). Bias (base log-odds) -0.807; bias + SHAP equals the model's log-odds within 1.0e-05.

| Rank | Field | Mean abs SHAP | Share | Mean SHAP | Gain rank |
|---|---|---|---|---|---|
| 1 | AGE | 0.4644 | 9.6% | -0.0357 | 37 |
| 2 | EXTRICAT | 0.4131 | 8.6% | -0.0498 | 6 |
| 3 | PERMVIT | 0.3934 | 8.1% | -0.0346 | 29 |
| 4 | REST_USE | 0.3681 | 7.6% | -0.0575 | 10 |
| 5 | EJECTION | 0.3550 | 7.4% | -0.0838 | 5 |
| 6 | BODY_TYP | 0.3351 | 6.9% | -0.0599 | 2 |
| 7 | DEFORMED | 0.3219 | 6.7% | -0.1069 | 4 |
| 8 | HARM_EV | 0.2909 | 6.0% | -0.1865 | 3 |
| 9 | IMPACT1 | 0.1945 | 4.0% | -0.0064 | 7 |
| 10 | AIR_BAG | 0.1675 | 3.5% | -0.0195 | 12 |

**Spearman correlation of field rankings, SHAP vs gain:** 0.405.

Field SHAP sums the field's one-hot and missing-indicator columns. Units are log-odds of a fatal outcome. Associations within FARS fatal crashes, not causal effects; related fields can share credit.
