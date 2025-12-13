# Revenue Operations & Fraud Detection Pipeline

**A production-grade, local-first ELT pipeline designed to ingest, validate, and model over 22 million financial records.**

---

## 💼 Executive Summary
This project simulates a real-world Data Engineering environment for a Fintech company. The goal was to migrate away from ad-hoc analysis (CSV/local files) to a scalable **Centralized Data Platform**.

It ingests **22 million+** raw records (transactions, fraud labels, and user data), performs rigorous data quality checks, detects fraud patterns, and materializes a "One Big Table" (OBT) for high-performance reporting on the core 13 million transactions.

## 🛠 Skills Demonstrated
* **Data Engineering:** ELT Architecture, Python Scripting, Data Modeling (Star Schema).
* **Database Management:** PostgreSQL, Indexing Strategies, Foreign Key Constraints, Materialized Views.
* **DevOps:** Docker Containerization, Environmental Configuration.
* **Data Quality:** PII Masking, Type Casting, Referential Integrity.

---

## 🏗 Architecture
The pipeline follows a modern **ELT (Extract, Load, Transform)** pattern, leveraging the power of the database engine for heavy lifting.

1.  **Extract & Load:** Python (`pandas` + `sqlalchemy`) streams raw JSON/CSV data into the database.
2.  **Staging:** SQL transformations clean currency formats, parse dates, and mask sensitive PII (Personal Identifiable Information).
3.  **Modeling:** Data is normalized into a Star Schema (Fact + Dimensions) with strict Primary/Foreign keys.
4.  **Serving:** A denormalized Materialized View (`enriched_transactions`) provides a low-latency layer for BI tools.

## 📊 Data Source
* **Dataset:** [Transactions Fraud Datasets (Kaggle)](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets/data?select=transactions_data.csv)
* **Volume:** **~22 Million Total Rows** (~13M Transactions + ~9M Fraud History Labels).

---

## 🚀 Project Roadmap & Achievements

### ✅ Phase 1: Robust Ingestion (Completed)
* **Challenge:** Moving from fragile local files to a structured database.
* **Solution:** Built a Dockerized PostgreSQL instance. Created a Python orchestration script (`load-data.py`) to handle ingestion errors and raw data cleaning.
* **Scale:** Successfully pipelines the full **22 million row** dataset, including parsing complex nested JSON structures for fraud history.

### ✅ Phase 2: Optimization & Integrity (Completed)
* **Challenge:** Queries on the 13M transaction table were slow; data inconsistencies were common.
* **Solution:**
    * **Indexing:** Added targeted B-Tree indexes on high-cardinality columns (`client_id`, `mcc`, `date`), achieving sub-second query performance.
    * **Integrity:** Enforced strict Foreign Key constraints between Transactions and Dimensions (Users, Cards, MCCs) to reject orphaned records.

### 🔄 Phase 3: Reporting Layer (Active)
* **Challenge:** Analysts needed a simple way to view "enriched" data without writing complex joins.
* **Solution:**
    * **Data Mart:** Implemented `enriched_transactions`, a wide Materialized View that pre-joins all dimensions to the 13M transactions.
    * **Concurrency:** Developed `refresh-view.py` to refresh analytics data concurrently, ensuring zero downtime for end-users during updates.

---

## 📂 Repository Structure
* `data/raw/`: Raw source files (excluded from repo).
* `models/`:
    * `staging/`: Cleaning logic and PII masking.
    * `indexing/`: Performance tuning and constraints.
    * `intermediate/`: The serving layer (Materialized Views).
    * `refresh/`: Maintenance scripts.
* `scripts/`:
    * `load-data.py`: Main orchestration (CLI menu driven).
    * `refresh-view.py`: Zero-downtime refresh utility.

---

## 💻 How to Run

### 1. Prerequisites
Ensure **Docker Desktop** and **Python 3.9+** are installed.

### 2. Start the Database
Spin up the isolated database container:
```bash
docker run -d \
    --name revenue-postgres \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=<YOUR_SECRET_PASSWORD> \
    -e POSTGRES_DB=revenue_ops \
    -p 5432:5432 \
    postgres:latest
```

### 3. Configure Environment
Create a `.env` file in the root directory:
```text
DB_CONNECTION_STRING=postgresql://admin:<YOUR_SECRET_PASSWORD>@localhost:5432/revenue_ops
```

### 4. Execute Pipeline
Run the interactive orchestration script:
```bash
python scripts/load-data.py
```
*Select **Option 6** for the full End-to-End run (Load -> Stage -> Mart -> Index).*