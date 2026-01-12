# Contributing to the UN SDG East Africa Insights Pipeline

Thank you for your interest! We welcome contributions from UN staff, governments, NGOs, and the open data community.

## How to contribute
- Add data: Place new source datasets in \`sdg_ea_pipeline/data/raw/placeholders/\` (CSV/Excel). Update \`config.yaml\` to reflect new sources and indicators.
- Extend ingestion: Enhance \`sdg_ea_pipeline/logic/ingestion/\` to support new sources while maintaining immutable raw storage and provenance.
- Improve cleaning/FE: Extend \`logic/cleaning/\` and \`logic/fe/\` to add new indicators, better harmonization, or new explainable features. Keep every transformation documented and auditable.
- Models: Add explainable baseline or advanced models in \`logic/models/\`. Add reports in the same structure and update documentation.
- Validation/Insights: Extend \`logic/validation/\` and \`outputs/insights/\` to provide better policy summaries and confidence scores.
- Documentation: Extend \`docs/\` with diagrams, onboarding materials, and guides for East African partners.

## Development workflow
1. Fork and clone the repo.
2. Create a virtual environment and install dependencies (see README.md).
3. Make changes.
4. Test locally by running \`python sdg_ea_pipeline/run_pipeline.py\`.
5. Submit a Pull Request with:
   - Clear description
   - Link to any relevant issues
   - One logical commit per major change

## Governance
- All changes must preserve data provenance, use clear field names, and avoid black-box transformations unless justified.
- Add unit tests in \`tests/\` if adding new logic.

## License
By contributing, you agree to license your contributions under the MIT License (see LICENSE).
