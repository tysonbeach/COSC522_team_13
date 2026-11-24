**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 76,403 occupants from 35,203 crashes; holdout 15,423 occupants / 7,041 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.1, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.894) on holdout:** accuracy 0.833, balanced accuracy 0.819, precision 0.815, recall 0.752, fatal F1 0.783, macro-F1 0.823, ROC-AUC 0.920, PR-AUC (AP) 0.896 (prevalence 0.400).

**Default settings on holdout:** balanced accuracy 0.818, ROC-AUC 0.917, AP 0.893.

**Tuned decision tree, same holdout:** ROC-AUC 0.889, PR-AUC (AP) 0.860, balanced accuracy 0.785, macro-F1 0.791.

**Top summed importances:** HARM_EV, P_CRASH2, REST_USE, BODY_TYP, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
