# ⚙️ Project Requirements and Dependencies

This project relies on a specific set of system software and Python libraries to ensure the data pipeline executes successfully and the database is accessible.

## 1. System Requirements (External Software)

The following external software must be installed and running on your local machine:

* **Docker Desktop:** Required to run the PostgreSQL database in a containerized, isolated environment.
    * **Purpose:** Provides the core **Docker Daemon** and the management interface for container operations. 
* **PostgreSQL Image:** The official PostgreSQL Docker image (`postgres:latest`) used to spin up the database container.
    * **Requirement:** The container must be running under the name `revenue-postgres` and exposed on port `5432`.
* **Python:** Version 3.9+ is recommended.
    * **Purpose:** Executes the main data orchestration script (`scripts/load-data.py`).

## 2. Python Dependencies (Pip Packages)

The following libraries must be installed in your Python environment via `pip`.

| Package Name | Purpose |
| :--- | :--- |
| `pandas` | Primary tool for raw data loading, reading CSV/JSON, and initial manipulation (DataFrames). |
| `sqlalchemy` | Object Relational Mapper (ORM) and core library for connecting Python to the PostgreSQL database engine. |
| `psycopg2-binary` | The necessary PostgreSQL database adapter (driver) for `sqlalchemy` to communicate with the database. |
| `python-dotenv` | Used to securely load the database connection string from the local, untracked `.env` file. |

## 3. Configuration Requirements

* **`.env` File:** A local `.env` file must be created in the project root to store the `DB_CONNECTION_STRING` securely. This file is ignored by Git.
* **Project Structure:** The directory structure (especially `data/raw/` and `models/staging/`) must be maintained as this is hardcoded in the pipeline script.