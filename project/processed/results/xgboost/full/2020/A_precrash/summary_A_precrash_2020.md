**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 70,845 occupants from 33,434 crashes; holdout 14,172 occupants / 6,687 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.804) on holdout:** accuracy 0.781, balanced accuracy 0.765, precision 0.770, recall 0.670, fatal F1 0.717, macro-F1 0.769, ROC-AUC 0.850, PR-AUC (AP) 0.809 (prevalence 0.413).

**Default settings on holdout:** balanced accuracy 0.759, ROC-AUC 0.846, AP 0.802.

**Tuned decision tree, same holdout:** ROC-AUC 0.822, PR-AUC (AP) 0.779, balanced accuracy 0.739, macro-F1 0.744.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
