# Revenue Operations Dashboard

A local-first data pipeline being built to analyze revenue streams and user transaction data.

## 🏗 Architecture

This project uses a production-grade, Python-driven **ELT (Extract, Load, Transform)** pipeline orchestrated against a containerized PostgreSQL database. 

* **Database:** PostgreSQL (Containerized via Docker) 
* **Orchestration:** Python/Pandas/SQLAlchemy (`scripts/load-data.py`)
* **Transformation:** Standard PostgreSQL SQL (Staging & Cleaning)

## ⚡️ Current Status

**Phase 1: Ingestion & Staging (Complete)**
* **Architectural Switch:** Successfully migrated from local DuckDB to containerized PostgreSQL for enhanced stability and compliance.
* **Data Quality:** Raw data ingested, cleaned, and type-cast. Handled complex cleaning of currency strings, date parsing, and PII masking.
* **Pipeline Run:** The full pipeline, including the 13+ million row transactions table, runs successfully from a single Python script.
* Scope focused purely on revenue operations (Fraud data removed).

**Phase 2: Optimization (In Progress)**
* Indexing strategies for high-performance querying on the large `transactions_data` table.

**Phase 3: Visualization (Planned)**
* Streamlit dashboard for revenue reporting.

## 📂 Project Structure

* `data/raw/`: Source CSV/JSON files (Cards, Transactions, Users, MCC Codes).
* `models/`: SQL logic.
    * `staging/`: Current cleaning and standardization scripts.
    * `indexing/`: **(NEW)** Optimization scripts (Indexes, Partitioning).
    * `intermediate/`: Planned joins.
* `scripts/`:
    * `load-data.py`: **(NEW)** Consolidated main pipeline. Ingests raw data, loads into Postgres, and executes staging SQL.
* `.env`: **(NEW)** Stores the PostgreSQL database connection string.

## 🚀 How to Run

### 1. Start the Database (Docker)

Ensure the Docker Desktop application is running. Launch the PostgreSQL container using the following command. **Update the POSTGRES\_PASSWORD to your secret value.**

```bash
docker run -d \
    --name revenue-postgres \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=<YOUR_SECRET_DB_PASSWORD> \
    -e POSTGRES_DB=revenue_ops \
    -p 5432:5432 \
    postgres:latest