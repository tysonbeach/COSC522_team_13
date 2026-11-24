**Model:** XGBoost. **Feature block:** A_precrash (25 features).

**Data:** 78,678 occupants from 36,586 crashes; holdout 15,933 occupants / 7,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.813) on holdout:** accuracy 0.784, balanced accuracy 0.765, precision 0.758, recall 0.672, fatal F1 0.713, macro-F1 0.770, ROC-AUC 0.854, PR-AUC (AP) 0.806 (prevalence 0.399).

**Default settings on holdout:** balanced accuracy 0.763, ROC-AUC 0.850, AP 0.800.

**Tuned decision tree, same holdout:** ROC-AUC 0.830, PR-AUC (AP) 0.778, balanced accuracy 0.744, macro-F1 0.750.

**Top summed importances:** REST_USE, BODY_TYP, SEAT_POS, HOUR, RELJCT2 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
