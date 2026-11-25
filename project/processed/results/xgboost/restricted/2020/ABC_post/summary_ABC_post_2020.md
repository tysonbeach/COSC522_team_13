**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.792) on holdout:** accuracy 0.821, balanced accuracy 0.781, precision 0.735, recall 0.675, fatal F1 0.703, macro-F1 0.788, ROC-AUC 0.892, PR-AUC (AP) 0.786 (prevalence 0.315).

**Default settings on holdout:** balanced accuracy 0.777, ROC-AUC 0.888, AP 0.779.

**Tuned decision tree, same holdout:** ROC-AUC 0.853, PR-AUC (AP) 0.717, balanced accuracy 0.752, macro-F1 0.759.

**Top summed importances:** EXTRICAT, P_CRASH2, HARM_EV, BODY_TYP, EJECTION (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
