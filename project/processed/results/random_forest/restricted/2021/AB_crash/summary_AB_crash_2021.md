**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 57,774 occupants from 18,452 crashes; holdout 11,637 occupants / 3,691 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.706) on holdout:** accuracy 0.783, balanced accuracy 0.711, precision 0.712, recall 0.517, fatal F1 0.599, macro-F1 0.725, ROC-AUC 0.843, PR-AUC (AP) 0.707 (prevalence 0.313).

**Default settings on holdout:** balanced accuracy 0.704, ROC-AUC 0.839, AP 0.692.

**Tuned decision tree, same holdout:** ROC-AUC 0.798, PR-AUC (AP) 0.638, balanced accuracy 0.685, macro-F1 0.695.

**Top summed importances:** AGE, REST_USE, PERMVIT, P_CRASH2, BODY_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
