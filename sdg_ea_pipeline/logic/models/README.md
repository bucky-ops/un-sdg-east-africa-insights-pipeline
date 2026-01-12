STEP 6: Baseline Models (Explainable)

Goal
- Provide transparent, baseline ML models using features from STEP 5 to illustrate policy-relevant insights without black-box techniques.

What’s included
- Regression: Linear Regression (baseline) to predict numeric indicator values.
- Classification: Logistic Regression to predict a simple proxy (increase vs not).
- Tree-based baseline: Decision Tree Regressor and Classifier for interpretable splits.
- Simple evaluation metrics and a JSON report describing model benefits/limits.

How to run
- Ensure STEP 5 outputs exist at `sdg_ea_pipeline/data/processed/fe/features.csv`.
- Run: `python sdg_ea_pipeline/logic/models/train_baseline.py`
- Outputs:
  - Models: `sdg_ea_pipeline/models/` (pickled)
  - Reports: `sdg_ea_pipeline/data/processed/fe/model_reports/*.json`

Interpretability notes for policy
- Linear models: coefficients indicate marginal impact per feature.
- Decision trees: easy to visualize decision paths; show where country and indicator interactions drive changes.
- Cautions: models are benchmarks with limited data; use them as starting points, not definitive truth.
