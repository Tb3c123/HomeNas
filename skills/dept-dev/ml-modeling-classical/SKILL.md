---
name: ml-modeling-classical
description: Build leakage-free classical ML pipelines (tabular, GBDT, linear, clustering) with proper CV, feature engineering, and probability calibration.
metadata:
  model: inherit
  source: K-Dense-AI/scientific-agent-skills (MIT)
---

# Classical Machine Learning & Tabular Modeling

## Use This Skill When
- Training classification, regression, ranking, or clustering models on tabular/structured datasets.
- Engineering features, tuning GBDTs (LightGBM/XGBoost/CatBoost) or `scikit-learn` pipelines.
- Auditing model generalization, class imbalance, or miscalibrated predicted probabilities.

## Core Principles
1. **Pipeline-First Zero Leakage:** Encapsulate all imputation, scaling, encoding, and feature selection inside a `scikit-learn` `Pipeline` / `ColumnTransformer` fit strictly on training folds—never fit preprocessors on the full dataset.
2. **Match CV Split to Data Structure:**
   - Imbalanced classes → `StratifiedKFold`.
   - Repeated users/sessions/entities → `GroupKFold` / `StratifiedGroupKFold` (prevent entity leakage).
   - Keep a **final untouched holdout test set** evaluated once at the end.
3. **Baseline Ladder:** Start with `DummyClassifier`/`Ridge`/`LogisticRegression` → Random Forest → Tuned GBDT (LightGBM/CatBoost). Add complexity only when CV improves meaningfully.
4. **Metric & Calibration Alignment:**
   - For imbalanced binary classification, evaluate **PR-AUC**, **LogLoss/Brier**, and business-cost thresholded F1/recall—not raw Accuracy.
   - Calibrate probabilities (`CalibratedClassifierCV` isotonic/Platt) when outputs drive risk scores or expected-value decisions.
5. **Interpretability & Error Analysis:** Inspect feature importances/SHAP, slice errors by subgroup/regime, and verify features are available and non-drifting at inference time.

## Delivery Checklist
- Confirm deterministic seeds, saved preprocessing + model artifact, and schema contract.
- Report CV mean ± std across folds plus error breakdown on worst-performing slices.
