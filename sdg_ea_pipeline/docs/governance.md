Governance and Configuration Layer

Rationale
- Establish a single source of truth for the SDG monitoring system to ensure transparent, auditable data handling across UN agencies, governments, and NGOs.
- Provide explicit mappings for countries, SDGs, indicators, and years to prevent misinterpretation and enable reproducibility.
- Flag data quality (missing, outdated, estimated) to surface uncertainty and guide policy decisions prudently.

What is governed
- Countries: list of East African country codes covered by the system.
- SDGs: the SDGs and their mappings used in the analytics pipeline.
- Indicators: the concrete metrics with codes and human-friendly names.
- Years: the temporal scope for historical data, enabling trend analysis.
- Metadata schema: the schema describing dataset columns for traceability.
- Data quality flags: indicators of data quality and reliability.

How governance helps UN systems
- Traceability: Every dataset is described by provenance, year, country, and indicator, enabling audit trails.
- Interoperability: Standardized codes and schemas reduce miscommunication across agencies and partners.
- Risk awareness: Quality flags surface uncertainty, reducing over-claiming in policy outputs.
- Reproducibility: All configurations can be loaded deterministically, ensuring same results across environments.

What to do next
- STEP 3 will implement immutable raw data ingestion with provenance logging, guided by the governance config.
