# Automotive Dealership Financial Analytics Pipeline

An end-to-end data engineering portfolio project building an enterprise General Ledger and OEM Rebate analytics layer using **dbt Core**, **DuckDB**, and **Power BI**.

## Business Problem & Context
Multi-location automotive dealership groups struggle with fragmented General Ledger (GL) reporting and delayed OEM rebate reconciliation. Without a unified analytics layer, calculating store-level profit margins and auditing vendor rebate claims requires slow, manual reporting.

This project transforms raw transactional dealership data into a Kimball dimensional star schema optimized for executive financial reporting and Power BI visualization.

## Key Architecture & Design Decisions
* **Synthetic Data Generation (`generate_gl.py`):** Programmatically generated realistic GL transactional data enforcing double-entry accounting rules (balancing debits and credits) to mimic enterprise ERP data.
* **Kimball Star Schema:** Organized staging views (`main_staging`) into clean analytics marts (`main_analytics`), separating core facts (`fct_general_ledger`, `fct_oem_rebate_allocations`) from dimensions (`dim_account`, `dim_dealer`, `dim_employee`, `dim_sku`, `dim_date`).
* **Grain Definition:** Maintained the general ledger fact table at the individual journal line item level to enable both high-level financial summary KPIs and full audit drill-downs.

## Business Questions Answered
1. What is the net financial performance across individual dealership locations over time?
2. Are OEM rebate allocations reconciled accurately against core GL accounts?
3. What are the highest-volume debit/credit activity drivers by account type?

## Tech Stack
* **Transformation:** dbt Core (v1.12)
* **Database Engine:** DuckDB (v1.11)
* **Data Synthesis:** Python (`generate_gl.py`)
* **Visualization:** Power BI Desktop
* **Version Control:** Git & GitHub

## Data Quality & Testing
Includes 18 automated dbt data tests enforcing `unique`, `not_null`, `relationships` (referential integrity), and `accepted_values` across staging and analytics models.

## How to Run
```bash
# 1. Load seed CSVs into DuckDB
dbt seed

# 2. Build staging models and analytics marts
dbt run

# 3. Execute data quality tests
dbt test