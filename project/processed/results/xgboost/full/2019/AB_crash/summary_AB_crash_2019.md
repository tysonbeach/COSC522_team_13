**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.892) on holdout:** accuracy 0.827, balanced accuracy 0.812, precision 0.807, recall 0.739, fatal F1 0.771, macro-F1 0.816, ROC-AUC 0.915, PR-AUC (AP) 0.889 (prevalence 0.394).

**Default settings on holdout:** balanced accuracy 0.811, ROC-AUC 0.913, AP 0.886.

**Tuned decision tree, same holdout:** ROC-AUC 0.882, PR-AUC (AP) 0.851, balanced accuracy 0.779, macro-F1 0.784.

**Top summed importances:** HARM_EV, P_CRASH2, REST_USE, BODY_TYP, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
