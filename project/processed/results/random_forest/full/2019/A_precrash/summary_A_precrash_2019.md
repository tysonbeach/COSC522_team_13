**Model:** Random forest. **Feature block:** A_precrash (25 features).

**Data:** 69,304 occupants from 31,587 crashes; holdout 14,049 occupants / 6,318 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 5, 'model__n_estimators': 300}; mean CV AP 0.784) on holdout:** accuracy 0.771, balanced accuracy 0.740, precision 0.771, recall 0.595, fatal F1 0.671, macro-F1 0.748, ROC-AUC 0.837, PR-AUC (AP) 0.779 (prevalence 0.394).

**Default settings on holdout:** balanced accuracy 0.736, ROC-AUC 0.832, AP 0.771.

**Tuned decision tree, same holdout:** ROC-AUC 0.814, PR-AUC (AP) 0.754, balanced accuracy 0.729, macro-F1 0.735.

**Top summed importances:** REST_USE, BODY_TYP, AGE, MOD_YEAR, PER_TYP (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
