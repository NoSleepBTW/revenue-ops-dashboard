# ⚙️ Technical Requirements & Dependencies

To ensure reproducibility across different environments, this project relies on containerization and a specific Python toolset.

## 1. System Infrastructure

* **Docker Desktop:**
    * **Why:** We use Docker to spin up a consistent, isolated PostgreSQL database version (`postgres:latest`) regardless of the host OS (Windows/Mac/Linux). This mimics a production cloud environment.
* **Python 3.9+:**
    * **Why:** The orchestration scripts leverage modern Python features for file handling and type safety.

## 2. Python Libraries

The following libraries are required for the ELT pipeline and Dashboard.

| Package | Role | Justification |
| :--- | :--- | :--- |
| **`pandas`** | Extract & Transform | Chosen for its efficient handling of CSV/JSON parsing before data hits the database. |
| **`sqlalchemy`** | ORM / Connection | Provides a secure, abstract layer to interact with SQL, preventing injection attacks. |
| **`psycopg2-binary`** | DB Driver | The standard, high-performance PostgreSQL adapter for Python. |
| **`python-dotenv`** | Security | Loads configuration from `.env` files, ensuring secrets (passwords) are never hardcoded in Git. |
| **`streamlit`** | Visualization | Framework used to build the interactive Risk Profile dashboard. |
| **`altair`** | Analytics | Declarative statistical visualization library for the dashboard charts. |

## 3. Configuration

* **Environmental Variables:** The application expects a `.env` file at the root to store the `DB_CONNECTION_STRING` securely.
* **Directory Structure:** The scripts are path-aware and expect `data/raw/` and `models/` to exist relative to the execution directory.

## 4. Installation Instructions

To set up the environment and install all dependencies:

1.  **Create Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Verify Installation:**
    ```bash
    streamlit --version
    python -c "import pandas; print(pandas.__version__)"
    ```