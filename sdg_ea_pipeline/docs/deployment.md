Deployment & Sustainability Plan

Overview
- A modular, open-source pipeline that can be run locally or in on-premises environments without cloud lock-in.

How to deploy
- Install Python 3.8+ and required packages from `requirements.txt`.
- Run the end-to-end pipeline with:
  - `python sdg_ea_pipeline/run_pipeline.py` or `python sdg_ea_pipeline/run_pipeline.py` and invoke individual steps as needed.

Project maintenance & knowledge transfer
- Governance artifacts (STEP 2) are the single source of truth for data mapping and quality flags.
- All outputs are versioned via simple filenames and a provenance log.
- Documentation (this file, architecture diagram) supports staff turnover and regional scaling.

Capacity-building guidance for East Africa
- Provide hands-on training for data collection, metadata management, and basic modeling.
- Use the pipeline’s modular steps to integrate national datasets and indicators.

Sustainability notes
- The config-driven approach ensures future staff can reproduce results.
- Regularly refresh placeholders with actual data; re-run validation to ensure continued reliability.
