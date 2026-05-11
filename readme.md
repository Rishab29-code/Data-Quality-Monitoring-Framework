# Data Quality Framework with Snowflake + dbt

## Overview

End-to-end batch data engineering pipeline for automated data ingestion, validation, transformation, orchestration, and monitoring.

Built to simulate production-grade enterprise data quality workflows.

---

## Architecture

API Source
↓
Python Ingestion
↓
Snowflake Raw Layer
↓
Validation Framework
↓
dbt Transformations
↓
SCD Type 2 Modeling
↓
Pipeline Orchestration
↓
Streamlit Dashboard

---

## Tech Stack

- Python
- Snowflake
- Snowpark
- dbt
- Streamlit
- Pandas

---

## Features

### Data Ingestion
- API-based ingestion
- Large-scale synthetic data generation (10K+ records)

### Validation Framework
- Null checks
- Duplicate checks
- Negative value checks
- Referential integrity checks

### Transformation
- Incremental dbt models
- Validation summary generation

### Historical Modeling
- SCD Type 2 implementation

### Orchestration
- Automated pipeline execution

### Monitoring
- Structured logging
- Interactive dashboard

---

## Dashboard

Displays:

- Validation success rate
- Failed record counts
- Historical validation trends

---

## Key Learnings

- Warehouse modeling
- Incremental pipelines
- Data quality engineering
- Historical tracking
- Operational monitoring
