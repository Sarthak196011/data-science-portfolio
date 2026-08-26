# ETL + BI Pipeline 🏗️

> **Full data engineering stack** | DuckDB + Streamlit BI Dashboard

## Overview
End-to-end data pipeline: raw CSVs → DuckDB star schema → 5-tab BI dashboard with 15+ charts. Demonstrates extract, transform, load, and visualize in a single deployable project.

## Quick Start
```bash
pip install -r requirements.txt
python run_pipeline.py      # Runs ETL pipeline
streamlit run dashboard/app.py  # Launches BI dashboard
```

## Pipeline Architecture
```
Raw CSVs (orders, customers, products)
    → extract.py  → Generate & load source data
    → transform.py → DuckDB SQL transformations (star schema)
    → load.py      → Persist to warehouse.duckdb
    → dashboard/app.py → 5-tab Streamlit BI dashboard
```

## Dashboard Tabs
1. Revenue Trends — monthly area chart, unique customers, AOV
2. Product Analytics — category breakdown, top 10 products
3. Customer Cohorts — segment analysis, LTV distribution
4. Regional — revenue by region, country, channel
5. Data Explorer — raw table viewer with CSV download

## Deploy
Streamlit Cloud: `dashboard/app.py` as main file (pipeline auto-runs on first load)
