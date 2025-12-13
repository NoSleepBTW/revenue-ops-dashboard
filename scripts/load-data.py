import os
import json
import time
import pathlib
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class RevenueOpsPipeline:
    def __init__(self, db_connection_string):
        self.db_url = db_connection_string
        self.engine = None
        self.paths = {
            "raw": pathlib.Path("data/raw"),
            "staging": pathlib.Path("models/staging"),
            "indexing": pathlib.Path("models/indexing"),
            "intermediate": pathlib.Path("models/intermediate"),
        }

    def connect(self):
        print(f"\nConnecting to Database...")
        self.engine = create_engine(self.db_url)
        print("Connection Established.\n")

    def _read_file_to_df(self, file_path):
        # Helper to read CSV or JSON
        if file_path.suffix == ".csv":
            return pd.read_csv(file_path)
        elif file_path.suffix == ".json":
            with open(file_path) as f:
                data = json.load(f)

            if file_path.name == "mcc_codes.json":
                return pd.DataFrame.from_dict(data, orient="index").reset_index(
                    names="mcc"
                )
            elif file_path.name.lower() == "train_fraud_labels.json":
                data = data["target"]
                df = pd.DataFrame.from_dict(data, orient="index").reset_index()
                df.columns = ["id", "is_fraud"]
                return df
            else:
                return pd.read_json(file_path)
        return None

    def load_raw_data(self):
        # Ingest raw files from data/raw into Postgres
        print("\nStarting Raw Data Load...")

        total_rows = 0  # Row counter

        for file_path in sorted(self.paths["raw"].glob("*.*")):
            if file_path.name.startswith("."):
                continue

            table_name = file_path.stem.lower()
            print(f"Loading {file_path.name}", end=" ", flush=True)

            try:
                start_time = time.time()

                df = self._read_file_to_df(file_path)

                if df is None:
                    print("Skipped (Unsupported Format)")
                    continue

                df.to_sql(
                    table_name,
                    self.engine,
                    if_exists="replace",
                    index=False,
                    method="multi",
                    chunksize=5000,
                )

                end_time = time.time()
                elapsed = end_time - start_time
                rows = len(df)
                total_rows += rows

                print(f"→ {table_name} ({rows:,} Rows) [{elapsed:.2f}s]")

            except Exception as e:
                print(f"Failed → {e}")
        print(f"Done. Total Rows Loaded: {total_rows:,}\n")

    def run_staging_models(self):
        # Executes SQL files stored in models/staging
        print("\nRunning SQL models (Staging)...")

        sql_files = sorted(list(pathlib.Path("models/staging").glob("*.sql")))

        with self.engine.connect() as connection:
            for sql_file in sql_files:
                file_name = sql_file.name

                print(f"Applying model: {file_name}...", end=" ", flush=True)

                try:
                    start_time = time.time()

                    with open(sql_file, "r") as f:
                        query = f.read()

                    connection.execute(text(query))
                    connection.commit()
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"→ Success [{elapsed:.2f}s]")

                except Exception as e:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Failed → {e} [{elapsed:.2f}s]")
                    connection.rollback()
                    return

        print("\nStaging complete.")

    def run_index_models(self):
        # Executes SQL files stored in models/indexing
        print("\nRunning SQL models (Indexing)...")

        sql_files = sorted(list(pathlib.Path("models/indexing").glob("*.sql")))

        with self.engine.connect() as connection:
            for sql_file in sql_files:
                file_name = sql_file.name

                print(f"Applying model: {file_name}...", end=" ", flush=True)

                try:
                    start_time = time.time()

                    with open(sql_file, "r") as f:
                        query = f.read()

                    connection.execute(text(query))
                    connection.commit()
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"→ Success [{elapsed:.2f}s]")

                except Exception as e:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Failed → {e} [{elapsed:.2f}s]")
                    connection.rollback()
                    return

        print("\nIndexing complete.")

    def drop_foreign_keys(self):
        print("\nDropping Foreign Key Constraints...")

        # List of all Foreign Key names to drop
        constraints_to_drop = ["fk_client", "fk_card", "fk_mcc", "fk_transaction_fraud"]

        with self.engine.connect() as connection:
            for constraint in constraints_to_drop:
                try:
                    # Determine the correct table to drop the constraint from
                    if constraint in ["fk_client", "fk_card", "fk_mcc"]:
                        table_name = "transactions_data"
                    elif constraint == "fk_transaction_fraud":
                        table_name = "train_fraud_labels"
                    else:
                        continue

                    # SQL to drop the constraint IF it exists, using the determined table name
                    query = text(
                        f"""
                        ALTER TABLE {table_name}
                        DROP CONSTRAINT IF EXISTS {constraint};
                    """
                    )
                    connection.execute(query)
                    connection.commit()
                    print(f"  - Dropped {constraint}.")
                except Exception as e:
                    print(f"  - Failed to drop {constraint}: {e}")
                    connection.rollback()
        print("\nForeign Key cleanup complete.")

    def run_data_mart(self):
        print("\nCreating Data Mart for Querying...")

        sql_files = sorted(list(pathlib.Path("models/intermediate").glob("*.sql")))

        with self.engine.connect() as connection:
            for sql_file in sql_files:
                file_name = sql_file.name

                print(f"Creating Mart: {file_name}...", end=" ", flush=True)

                try:
                    start_time = time.time()

                    with open(sql_file, "r") as f:
                        query = f.read()

                    connection.execute(text(query))
                    connection.commit()
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"→ Success [{elapsed:.2f}s]")

                except Exception as e:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Failed → {e} [{elapsed:.2f}s]")
                    connection.rollback()
                    return

        print("\nData Mart creation complete.")


if __name__ == "__main__":
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
    run = "Y"

    if not DB_CONNECTION_STRING:
        raise ValueError("Error: DB_CONNECTION_STRING Not Found in .env File")

    pipeline = RevenueOpsPipeline(DB_CONNECTION_STRING)

    # Establish Connection:
    pipeline.connect()

    try:
        while run.upper() == "Y":

            answer = input(
                "Please Select Action:\n1. Drop Foreign Keys\n2. Load Raw Data\n3. Run Staging Models\n4. Run Index Models\n5. Create Data Mart\n6. Run All Scripts\n"
            )

            VALID_CHOICE = ["1", "2", "3", "4", "5", "6"]

            if answer not in VALID_CHOICE:
                print("\nInvalid Selection. Please enter a number between 1 and 6.")
                continue
            elif answer == "1":
                pipeline.drop_foreign_keys()
            elif answer == "2":
                pipeline.load_raw_data()
            elif answer == "3":
                pipeline.run_staging_models()
            elif answer == "4":
                pipeline.run_index_models()
            elif answer == "5":
                pipeline.run_data_mart()
            elif answer == "6":
                pipeline.drop_foreign_keys()
                pipeline.load_raw_data()
                pipeline.run_staging_models()
                pipeline.run_data_mart()
                pipeline.run_index_models()

            run = input("Would you like to run another script?(Y/N): ")

    finally:
        if pipeline.engine:
            print("\nClosing connection...")
            pipeline.engine.dispose()
        print("Database connection closed.")
