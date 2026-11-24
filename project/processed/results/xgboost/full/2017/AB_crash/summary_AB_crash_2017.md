**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.1, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.891) on holdout:** accuracy 0.830, balanced accuracy 0.816, precision 0.811, recall 0.748, fatal F1 0.778, macro-F1 0.820, ROC-AUC 0.916, PR-AUC (AP) 0.891 (prevalence 0.398).

**Default settings on holdout:** balanced accuracy 0.811, ROC-AUC 0.911, AP 0.887.

**Tuned decision tree, same holdout:** ROC-AUC 0.881, PR-AUC (AP) 0.853, balanced accuracy 0.783, macro-F1 0.789.

**Top summed importances:** HARM_EV, P_CRASH2, BODY_TYP, REST_USE, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
