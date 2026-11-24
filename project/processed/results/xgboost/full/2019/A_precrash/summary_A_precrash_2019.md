**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.795) on holdout:** accuracy 0.780, balanced accuracy 0.758, precision 0.755, recall 0.655, fatal F1 0.701, macro-F1 0.764, ROC-AUC 0.848, PR-AUC (AP) 0.794 (prevalence 0.394).

**Default settings on holdout:** balanced accuracy 0.754, ROC-AUC 0.842, AP 0.786.

**Tuned decision tree, same holdout:** ROC-AUC 0.814, PR-AUC (AP) 0.754, balanced accuracy 0.729, macro-F1 0.735.

**Top summed importances:** REST_USE, SEAT_POS, BODY_TYP, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
