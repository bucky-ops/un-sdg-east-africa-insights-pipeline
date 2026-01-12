STEP 5: Feature Engineering (Human-Understandable)

Overview
- Build transparent features on top of the cleaned data from STEP 4.
- Features are designed to be interpretable and policy-friendly.

What’s produced
- YOY change: year-over-year percentage change for each country/indicator.
- Rolling mean (3-year): simple moving average over the last 3 years for each country/indicator.
- Rolling std (3-year): standard deviation over the last 3 years for each country/indicator.
- Risk level: categorized per-indicator within the indicator’s value distribution (low/medium/high).
- Outputs: wide feature set and a long-form version suitable for dashboards and exports.

Run independently
- Command: `python sdg_ea_pipeline/logic/fe/feature_engineering.py`
- Reads cleaned data from `sdg_ea_pipeline/data/processed/cleaned.csv`.
- Writes outputs to `sdg_ea_pipeline/data/processed/fe/` as `features.csv` and `features_long.csv`.

Notes for policymakers
- Each feature is explicitly documented in code comments and in this README.
- If data gaps exist, YOY and rolling features will reflect NaNs or will be imputed consistently with STEP 4 rules.
