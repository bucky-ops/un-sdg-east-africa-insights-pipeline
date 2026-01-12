# AGENTS.md - Repo Guidance for Contributors

This file provides guidance for AI agents or automated tools contributing to the repository.

## Repository Structure
- Use `sdg_ea_pipeline/` as the root for code changes.
- Maintain governance in `config/` and documentation in `docs/`.
- Outputs go to `outputs/` for policy-ready artifacts.

## Coding Standards
- Python 3.8+ compatible.
- Use pandas, numpy, scikit-learn for data/ML.
- Avoid black-box models; prioritize explainability.
- Comment code clearly for policymakers.

## Commit Messages
- Use descriptive, policy-focused messages (e.g., "feat: add YoY change feature for SDG3").
- Separate commits by logical changes (governance, ingestion, FE, etc.).

## Testing
- Run `python sdg_ea_pipeline/run_pipeline.py` to test end-to-end.
- Add smoke tests in `tests/` for new modules.
