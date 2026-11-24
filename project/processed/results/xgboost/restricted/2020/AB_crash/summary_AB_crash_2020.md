**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 50,488 occupants from 16,464 crashes; holdout 10,242 occupants / 3,293 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.733) on holdout:** accuracy 0.788, balanced accuracy 0.734, precision 0.693, recall 0.588, fatal F1 0.636, macro-F1 0.744, ROC-AUC 0.855, PR-AUC (AP) 0.725 (prevalence 0.315).

**Default settings on holdout:** balanced accuracy 0.729, ROC-AUC 0.849, AP 0.714.

**Tuned decision tree, same holdout:** ROC-AUC 0.793, PR-AUC (AP) 0.631, balanced accuracy 0.681, macro-F1 0.691.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, REST_USE, IMPACT1 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
