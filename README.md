# Revenue Operations Dashboard

A local-first data pipeline being built to analyze revenue streams and user transaction data.

## 🏗 Architecture

This project uses a production-grade, Python-driven **ELT (Extract, Load, Transform)** pipeline orchestrated against a containerized PostgreSQL database. 

* **Database:** PostgreSQL (Containerized via Docker) 
* **Orchestration:** Python/Pandas/SQLAlchemy (`scripts/load-data.py`)
* **Transformation:** Standard PostgreSQL SQL (Staging, Indexing, Data Marts)

## ⚡️ Current Status

**Phase 1: Ingestion & Staging (Complete)**
* **Architectural Switch:** Successfully migrated from local DuckDB to containerized PostgreSQL for enhanced stability and compliance.
* **Data Quality:** Raw data ingested, cleaned, and type-cast. Handled complex cleaning of currency strings, date parsing, and PII masking.
* **Pipeline Run:** The full pipeline, including the 13+ million row transactions table, runs successfully from a single Python script.
* Scope focused purely on revenue operations (Fraud data removed).

**Phase 2: Optimization (Complete)**
* **High-Performance Indexing:** Implemented targeted indexing strategies on the 13+ million row `transactions_data` table (`date`, `client_id`, `mcc`) to guarantee sub-second query performance for analytics.
* **Data Integrity:** Established **Primary Keys** on all dimension tables and **Foreign Key constraints** between the Fact table (`transactions_data`) and all Dimension tables (`users_data`, `cards_data`, `mcc_codes`) to enforce referential integrity.
* **Pipeline Control:** The main script now features a robust, interactive menu for modular execution and safe resource cleanup.

**Phase 3: Data Marts & Visualization (In Progress)**
* **Intermediate Marts:** Building denormalized, enriched fact tables for reporting performance.
* **Visualization:** Streamlit dashboard for key revenue reporting and drill-down analysis.

## 📂 Project Structure

* `data/raw/`: Source CSV/JSON files (Cards, Transactions, Users, MCC Codes).
* `models/`: SQL logic.
    * `staging/`: Current cleaning and standardization scripts (Adds **Primary Keys**).
    * `indexing/`: Optimization scripts (**Indexes and Foreign Key Constraints**).
    * `intermediate/`: **(NEW)** Denormalized fact tables/Data Marts (Planned joins).
    * `reporting/`: **(FUTURE)** Final aggregated tables for dashboards.
* `scripts/`:
    * `load-data.py`: **(REFINED)** The core orchestration script featuring an **interactive menu** for modular execution (Load, Stage, Index, Full Run).
* `.env`: Stores the PostgreSQL database connection string.

## 🚀 How to Run

### 1. Start the Database (Docker)

Ensure the Docker Desktop application is running. Launch the PostgreSQL container using the following command (or use your `docker-compose.yml` if available). **Update the POSTGRES\_PASSWORD to your secret value.**

```bash
docker run -d \
    --name revenue-postgres \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=<YOUR_SECRET_DB_PASSWORD> \
    -e POSTGRES_DB=revenue_ops \
    -p 5432:5432 \
    postgres:latest