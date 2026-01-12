# UN SDG East Africa Insights Pipeline

A modular, governance-first, open-source SDG monitoring analytics pipeline for East Africa, designed for UN agencies, governments, and NGOs. This project emphasizes transparency, interpretability, sustainability, and explainability in data analytics for policy-making.

## Overview
- **Governance & Configuration**: Single source of truth for countries, SDGs, indicators, years, and data quality flags.
- **Data Ingestion**: Immutable raw data storage with provenance logging.
- **Cleaning & Standardization**: Pandas-based harmonization, missing value handling, and time alignment.
- **Feature Engineering**: Human-understandable features like YoY change, rolling averages, and risk flags.
- **Baseline ML Models**: Explainable regression and classification (Linear and Logistic Regression).
- **Validation & Trust**: Simple bias checks, confidence scoring, and ethical cautions.
- **Insights & Reporting**: Policy-ready summaries, charts, and text-based reports.
- **Visualization Hooks**: Exports ready for Power BI, Tableau, GIS, and static PDFs.
- **Deployment & Sustainability**: Documentation, maintenance guides, and capacity-building notes for East African institutions.

## Key Features
- **Open-Source & No Cloud Lock-In**: Runs locally or on-premises.
- **Ethical & Transparent**: All transformations are auditable; models are explainable.
- **Policy-Focused**: Outputs designed for decision-makers (analyst-ready, policymaker-ready, UN-report-ready).
- **Scalable & Maintainable**: Modular architecture survives staff turnover.
- **Data-Driven Governance**: Provenance logs and quality flags prevent misuse.

## Getting Started
1. **Clone the Repository**
   ```bash
   git clone https://github.com/bucky-ops/un-sdg-east-africa-insights-pipeline.git
   cd un-sdg-east-africa-insights-pipeline
   ```

2. **Install Dependencies**
   ```bash
   python -m pip install --upgrade pip
   python -m pip install pandas numpy scikit-learn joblib
   ```

3. **Run the End-to-End Pipeline**
   ```bash
   python sdg_ea_pipeline/run_pipeline.py
   ```

4. **Review Outputs**
   - `sdg_ea_pipeline/data/raw/archive/` - Immutable raw copies
   - `sdg_ea_pipeline/data/interim/` - Ingested interim CSVs
   - `sdg_ea_pipeline/data/provenance/` - Provenance logs
   - `sdg_ea_pipeline/data/processed/cleaned.csv` - Cleaned data
   - `sdg_ea_pipeline/data/processed/fe/features.csv` - Engineered features
   - `sdg_ea_pipeline/models/` - Serialized models
   - `sdg_ea_pipeline/data/processed/fe/model_reports/` - Model reports
   - `sdg_ea_pipeline/outputs/insights/` - Text and CSV insights
   - `sdg_ea_pipeline/outputs/visuals/` - BI-ready exports
   - `sdg_ea_pipeline/docs/` - Architecture and deployment docs

## Folder Structure
- `sdg_ea_pipeline/data/` - Raw, interim, provenance, and metadata storage
- `sdg_ea_pipeline/logic/` - Core processing (ingestion, cleaning, FE, models, validation)
- `sdg_ea_pipeline/models/` - Model artifacts and reports
- `sdg_ea_pipeline/outputs/` - Policy-ready insights and visualizations
- `sdg_ea_pipeline/config/` - Governance and configuration
- `sdg_ea_pipeline/docs/` - Documentation and architecture
- `sdg_ea_pipeline/tests/` - Unit tests and validation scripts
- `sdg_ea_pipeline/run_pipeline.py` - End-to-end orchestrator

## Policy Relevance
This pipeline supports SDG monitoring by providing:
- Transparent data lineage for auditable decisions.
- Human-understandable features to communicate trends.
- Explainable models with clear limitations.
- Outputs that align with UN reporting standards.
- Governance to prevent misinterpretation or misuse.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to the project.

## License
MIT License (see LICENSE).

## Contact
For questions or collaborations, please reach out via GitHub issues.
