**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 72,553 occupants from 32,715 crashes; holdout 14,497 occupants / 6,543 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.892) on holdout:** accuracy 0.829, balanced accuracy 0.817, precision 0.808, recall 0.755, fatal F1 0.781, macro-F1 0.820, ROC-AUC 0.914, PR-AUC (AP) 0.891 (prevalence 0.402).

**Default settings on holdout:** balanced accuracy 0.815, ROC-AUC 0.912, AP 0.889.

**Tuned decision tree, same holdout:** ROC-AUC 0.881, PR-AUC (AP) 0.853, balanced accuracy 0.785, macro-F1 0.789.

**Top summed importances:** P_CRASH2, HARM_EV, REST_USE, PCRASH5, BODY_TYP (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
