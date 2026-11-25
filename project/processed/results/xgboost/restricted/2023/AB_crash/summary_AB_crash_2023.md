**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.728) on holdout:** accuracy 0.790, balanced accuracy 0.735, precision 0.694, recall 0.587, fatal F1 0.636, macro-F1 0.745, ROC-AUC 0.856, PR-AUC (AP) 0.732 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.733, ROC-AUC 0.851, AP 0.722.

**Tuned decision tree, same holdout:** ROC-AUC 0.797, PR-AUC (AP) 0.633, balanced accuracy 0.681, macro-F1 0.691.

**Top summed importances:** P_CRASH2, HARM_EV, BODY_TYP, REST_USE, IMPACT1 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
