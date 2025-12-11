# Revenue Operations Dashboard

A local-first data pipeline being built to analyze revenue streams and user transaction data.

## 🏗 Architecture
This project uses a lightweight, Python-driven ETL pipeline to orchestrate a DuckDB database.

* **Database:** DuckDB (Local file `dev.duckdb`)
* **Orchestration:** Python (`scripts/load-raw-data.py`)
* **Transformation:** Standard SQL (Staging & Cleaning)

## ⚡️ Current Status
**Phase 1: Ingestion & Staging (Complete)**
* Raw data ingestion pipeline is active.
* Staging models are implemented for cleaning, type casting, and PII masking.
* Scope focused purely on revenue operations (Fraud data removed).

**Phase 2: Optimization (In Progress)**
* Indexing strategies for high-performance querying.

**Phase 3: Visualization (Planned)**
* Streamlit dashboard for revenue reporting.

## 📂 Project Structure

* `data/raw/`: Source CSV/JSON files (Cards, Transactions, Users, MCC Codes).
* `models/`: SQL logic.
    * `staging/`: Current cleaning and standardization scripts.
    * `intermediate/`: Planned joins.
* `scripts/`:
    * `load-raw-data.py`: Main pipeline. Ingests raw data and executes staging SQL.

## 🚀 How to Run

1.  **Install Dependencies:**
    ```bash
    pip install duckdb pandas
    ```

2.  **Run the Pipeline:**
    This script loads raw data and applies staging transformations.
    ```bash
    python scripts/load-raw-data.py
    ```