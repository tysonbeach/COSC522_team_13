**Model:** XGBoost. **Feature block:** AB_crash (38 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.728) on holdout:** accuracy 0.792, balanced accuracy 0.739, precision 0.695, recall 0.598, fatal F1 0.643, macro-F1 0.748, ROC-AUC 0.855, PR-AUC (AP) 0.724 (prevalence 0.313).

**Default settings on holdout:** balanced accuracy 0.730, ROC-AUC 0.850, AP 0.714.

**Tuned decision tree, same holdout:** ROC-AUC 0.798, PR-AUC (AP) 0.638, balanced accuracy 0.685, macro-F1 0.695.

**Top summed importances:** P_CRASH2, BODY_TYP, HARM_EV, IMPACT1, REST_USE (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
