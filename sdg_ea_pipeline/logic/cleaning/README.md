STEP 4: Data Cleaning & Standardization (Pandas Only)

Overview
- Apply transparent, interpretable data cleaning to interim data produced by STEP 3.
- No ML here. Focus on governance-friendly standardization for policymakers.

What this does
- Country harmonization: unify country codes (supporting 3-letter codes and common full names).
- Indicator normalization: ensure codes are uppercase and consistently referenced.
- Year alignment: fill in missing year-entity-indicator combinations to support trend analysis.
- Missing value handling: expose missingness and impute with simple, explainable rules (per-indicator medians).
- Output: a cleaned dataset ready for modeling or reporting; also a long-format version for dashboards.

Run independently
- Command: `python sdg_ea_pipeline/logic/cleaning/clean.py`
- Reads interim data from `sdg_ea_pipeline/data/interim/` and writes cleaned data to `sdg_ea_pipeline/data/processed/`.

Notes for policymakers
- Transformations are documented inline in the script so stakeholders can audit every step.
- Data quality flags (missing/estimated/outdated) are preserved where possible.
