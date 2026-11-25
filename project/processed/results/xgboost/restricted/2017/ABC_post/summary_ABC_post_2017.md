**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 52,957 occupants from 16,636 crashes; holdout 10,627 occupants / 3,328 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.783) on holdout:** accuracy 0.824, balanced accuracy 0.783, precision 0.736, recall 0.675, fatal F1 0.705, macro-F1 0.789, ROC-AUC 0.893, PR-AUC (AP) 0.786 (prevalence 0.311).

**Default settings on holdout:** balanced accuracy 0.781, ROC-AUC 0.889, AP 0.775.

**Tuned decision tree, same holdout:** ROC-AUC 0.852, PR-AUC (AP) 0.713, balanced accuracy 0.745, macro-F1 0.750.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, EXTRICAT, DEFORMED (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
