**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 56,226 occupants from 18,000 crashes; holdout 11,299 occupants / 3,600 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 200, 'model__subsample': 0.8}; mean CV AP 0.644) on holdout:** accuracy 0.760, balanced accuracy 0.682, precision 0.661, recall 0.474, fatal F1 0.552, macro-F1 0.694, ROC-AUC 0.799, PR-AUC (AP) 0.646 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.687, ROC-AUC 0.793, AP 0.639.

**Tuned decision tree, same holdout:** ROC-AUC 0.766, PR-AUC (AP) 0.600, balanced accuracy 0.662, macro-F1 0.674.

**Top summed importances:** BODY_TYP, REST_USE, SEAT_POS, HOUR, VTRAFCON (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
