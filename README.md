# Revenue Operations & Fraud Detection Platform

**A production-grade ELT pipeline and Analytics Dashboard designed to ingest, validate, and visualize over 22 million financial records.**

---

## 💼 Executive Summary
This project simulates a complete Data Engineering lifecycle for a Fintech company. It migrates ad-hoc data processes into a scalable **Centralized Data Platform**.

The system ingests **22 million+** raw records, detects fraud patterns using SQL logic, and surfaces insights via a live **Streamlit Dashboard**.

## 🚀 Key Features

### 1. Robust ELT Pipeline
* **Ingestion:** Python scripts stream raw JSON/CSV data into PostgreSQL.
* **Data Quality:** Automated cleaning of currency formats, date parsing, and PII masking.
* **Integrity:** Enforced Foreign Key constraints to reject orphaned records.

### 2. High-Performance Data Modeling
* **Star Schema:** Normalized data into Fact and Dimension tables.
* **Indexing:** Optimized B-Tree indexes on `client_id` and `transaction_date` for sub-second queries.
* **Materialized Views:** Pre-computed "One Big Table" (`enriched_transactions`) for fast analytics.

### 3. Interactive Dashboard
* **Tech Stack:** Streamlit + Altair.
* **Capabilities:** Tracks the "Vampire Index" (fraud by hour), identifies high-risk merchant categories, and monitors real-time financial loss.

---

## ⚙️ Technical Requirements & Dependencies

To ensure reproducibility across different environments, this project relies on containerization and a specific Python toolset.

### 1. System Infrastructure

* **Docker Desktop:**
    * **Why:** We use Docker to spin up a consistent, isolated PostgreSQL database version (`postgres:latest`) regardless of the host OS (Windows/Mac/Linux). This mimics a production cloud environment.
* **Python 3.9+:**
    * **Why:** The orchestration scripts leverage modern Python features for file handling and type safety.

### 2. Python Libraries

The following libraries are required for the ELT pipeline and Dashboard. You can install them via `pip install -r requirements.txt`.

| Package | Role | Justification |
| :--- | :--- | :--- |
| **`pandas`** | Extract & Transform | Efficient handling of CSV/JSON parsing before data hits the database. |
| **`sqlalchemy`** | ORM / Connection | Secure, abstract layer for SQL interaction to prevent injection attacks. |
| **`psycopg2-binary`** | DB Driver | The standard, high-performance PostgreSQL adapter for Python. |
| **`python-dotenv`** | Security | Loads configuration from `.env` files, ensuring secrets (passwords) are never hardcoded in Git. |
| **`streamlit`** | Visualization | Framework used to build the interactive Risk Profile dashboard. |
| **`altair`** | Analytics | Declarative statistical visualization library for the dashboard charts. |

### 3. Configuration

* **Environmental Variables:** The application expects a `.env` file at the root to store the `DB_CONNECTION_STRING` securely.
* **Directory Structure:** The scripts are path-aware and expect `data/raw/` and `models/` to exist relative to the execution directory.

---

## 📂 Repository Structure
* `data/raw/`: Raw source files (excluded from repo).
* `models/`:
    * `staging/`: Cleaning logic and PII masking.
    * `indexing/`: Performance tuning and constraints.
    * `intermediate/`: The serving layer (Materialized Views).
    * `queries/`: SQL backing the Streamlit dashboard.
* `scripts/`:
    * `load-data.py`: Main orchestration (CLI menu driven).
    * `refresh-view.py`: Zero-downtime refresh utility.
* `dashboard/`:
    * `app.py`: The entry point for the Streamlit visualization.
* `docker/`:
    * `pg_hba.conf`: PostgreSQL client authentication configuration.

---

## 💻 How to Run

### 1. Prerequisites
* **Docker & Docker Compose** (for the database)
* **Python 3.9+**

### 2. Configure Environment

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` with your preferred credentials:
```text
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=revenue_ops
DB_CONNECTION_STRING=postgresql://admin:your_secure_password_here@localhost:5432/revenue_ops
```

### 3. Start the Database

Using Docker Compose:
```bash
docker compose up -d postgres
```

This spins up a PostgreSQL 16 container with:
- Persistent data storage
- Network access configured for Power BI/external tools
- Health checks enabled

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Pipeline

Initialize the database, load raw data, and build models:

```bash
python scripts/load-data.py
```

*Select **Option 6** in the menu to run the full End-to-End pipeline.*

### 6. Launch Dashboard

**Option A:** Run locally:
```bash
streamlit run dashboard/app.py
```

**Option B:** Run via Docker (includes database):
```bash
docker compose --profile dashboard up -d
```
Access the dashboard at `http://localhost:8501`