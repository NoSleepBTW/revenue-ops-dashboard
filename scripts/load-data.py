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
        }

    def connect(self):
        print(f"Connecting to Database...")
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
            else:
                return pd.read_json(file_path)
        return None

    def load_raw_data(self):
        # Ingest raw files from data/raw into Postgres
        print("Starting Raw Data Load...")

        if not self.engine:
            self.connect()

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
        print("Running staging models...")

        if not self.engine:
            self.connect()

        with self.engine.connect() as connection:
            for sql_file in sorted(self.paths["staging"].glob("*.sql")):
                file_name = sql_file.stem

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

        print("\nPipeline complete.")


if __name__ == "__main__":
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

    if not DB_CONNECTION_STRING:
        raise ValueError("Error: DB_CONNECTION_STRING Not Found in .env File")

    pipeline = RevenueOpsPipeline(DB_CONNECTION_STRING)
    pipeline.load_raw_data()
    pipeline.run_staging_models()
