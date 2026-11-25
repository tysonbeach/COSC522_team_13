**Model:** XGBoost. **Feature block:** ABC_post (44 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__colsample_bytree': 0.8, 'model__learning_rate': 0.05, 'model__max_depth': 6, 'model__n_estimators': 500, 'model__subsample': 0.8}; mean CV AP 0.915) on holdout:** accuracy 0.855, balanced accuracy 0.846, precision 0.822, recall 0.806, fatal F1 0.814, macro-F1 0.848, ROC-AUC 0.938, PR-AUC (AP) 0.914 (prevalence 0.394).

**Default settings on holdout:** balanced accuracy 0.842, ROC-AUC 0.935, AP 0.910.

**Tuned decision tree, same holdout:** ROC-AUC 0.911, PR-AUC (AP) 0.881, balanced accuracy 0.817, macro-F1 0.819.

**Top summed importances:** HARM_EV, REST_USE, EXTRICAT, P_CRASH2, PCRASH5 (XGBoost gain importance, training data; associations within FARS fatal crashes, not causal effects).
