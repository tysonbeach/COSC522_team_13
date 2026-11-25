**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 80,213 occupants from 37,097 crashes; holdout 16,149 occupants / 7,420 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.803) on holdout:** accuracy 0.774, balanced accuracy 0.756, precision 0.750, recall 0.663, fatal F1 0.704, macro-F1 0.761, ROC-AUC 0.848, PR-AUC (AP) 0.802 (prevalence 0.406).

**Default settings on holdout:** balanced accuracy 0.756, ROC-AUC 0.845, AP 0.797.

**Tuned decision tree, same holdout:** ROC-AUC 0.823, PR-AUC (AP) 0.770, balanced accuracy 0.737, macro-F1 0.743.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
