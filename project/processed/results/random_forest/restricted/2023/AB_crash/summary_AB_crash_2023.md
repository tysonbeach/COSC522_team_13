**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 54,522 occupants from 17,388 crashes; holdout 10,915 occupants / 3,478 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.706) on holdout:** accuracy 0.780, balanced accuracy 0.707, precision 0.706, recall 0.510, fatal F1 0.592, macro-F1 0.721, ROC-AUC 0.841, PR-AUC (AP) 0.703 (prevalence 0.312).

**Default settings on holdout:** balanced accuracy 0.697, ROC-AUC 0.838, AP 0.690.

**Tuned decision tree, same holdout:** ROC-AUC 0.797, PR-AUC (AP) 0.633, balanced accuracy 0.681, macro-F1 0.691.

**Top summed importances:** AGE, REST_USE, PERMVIT, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
