**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 50,551 occupants from 16,029 crashes; holdout 10,050 occupants / 3,206 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.707) on holdout:** accuracy 0.783, balanced accuracy 0.712, precision 0.709, recall 0.522, fatal F1 0.601, macro-F1 0.726, ROC-AUC 0.843, PR-AUC (AP) 0.717 (prevalence 0.314).

**Default settings on holdout:** balanced accuracy 0.708, ROC-AUC 0.839, AP 0.701.

**Tuned decision tree, same holdout:** ROC-AUC 0.808, PR-AUC (AP) 0.651, balanced accuracy 0.695, macro-F1 0.703.

**Top summed importances:** AGE, REST_USE, PERMVIT, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
