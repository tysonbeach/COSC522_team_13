**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.804) on holdout:** accuracy 0.781, balanced accuracy 0.761, precision 0.761, recall 0.660, fatal F1 0.707, macro-F1 0.766, ROC-AUC 0.857, PR-AUC (AP) 0.812 (prevalence 0.400).

**Default settings on holdout:** balanced accuracy 0.758, ROC-AUC 0.853, AP 0.808.

**Tuned decision tree, same holdout:** ROC-AUC 0.824, PR-AUC (AP) 0.778, balanced accuracy 0.736, macro-F1 0.743.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
