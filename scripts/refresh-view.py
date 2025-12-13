import os
import time
import pathlib
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class RefreshViews:

    def __init__(self, db_connection_string):
        self.db_url = db_connection_string
        self.engine = None
        self.paths = {"refresh": pathlib.Path("models/refresh")}

    def connect(self):
        print(f"\nConnecting to Database...")
        self.engine = create_engine(self.db_url)
        print("Connection Established.\n")

    def refreshView(self):
        print("\nStarting Materialized View Refresh...")
        sql_files = sorted(list(self.paths["refresh"].glob("*.sql")))

        with self.engine.connect() as connection:
            for sql_file in sql_files:
                file_name = sql_file.name

                print(f"Refreshing: {file_name}...", end=" ", flush=True)

                try:
                    start_time = time.time()

                    with open(sql_file, "r") as f:
                        query = f.read()

                    # Execute the SQL
                    connection.execute(text(query))
                    connection.commit()  # Commit the successful operation

                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"→ Success [{elapsed:.2f}s]")

                except Exception as e:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Failed → {e} [{elapsed:.2f}s]")
                    connection.rollback()  # Rollback on failure
                    continue

        print("\nAll refresh scripts completed.")


if __name__ == "__main__":
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

    # Guardrail for DB connection
    if not DB_CONNECTION_STRING:
        print("Error: DB_CONNECTION_STRING not found in .env file.")
        exit()

    pipeline = RefreshViews(DB_CONNECTION_STRING)

    try:
        pipeline.connect()
        pipeline.refreshView()
    except Exception as e:
        print(f"\nFatal error during pipeline run: {e}")
    finally:
        if pipeline.engine:
            pipeline.engine.dispose()
        print("Database connection closed.")
