**Model:** Random forest. **Feature block:** AB_crash (38 features).

**Data:** 72,373 occupants from 32,667 crashes; holdout 14,582 occupants / 6,534 crashes, no crash overlap; split identical to the decision-tree manifest.

**Tuned model ({'model__max_features': 0.1, 'model__min_samples_leaf': 1, 'model__n_estimators': 300}; mean CV AP 0.880) on holdout:** accuracy 0.823, balanced accuracy 0.805, precision 0.816, recall 0.717, fatal F1 0.763, macro-F1 0.811, ROC-AUC 0.905, PR-AUC (AP) 0.880 (prevalence 0.398).

**Default settings on holdout:** balanced accuracy 0.797, ROC-AUC 0.899, AP 0.869.

**Tuned decision tree, same holdout:** ROC-AUC 0.881, PR-AUC (AP) 0.853, balanced accuracy 0.783, macro-F1 0.789.

**Top summed importances:** REST_USE, AGE, PERMVIT, BODY_TYP, P_CRASH2 (mean impurity decrease over the trees, training data; associations within FARS fatal crashes, not causal effects).
