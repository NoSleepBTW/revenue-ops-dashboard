import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Module-level engine singleton (reused across all queries)
_engine = None


def get_engine():
    """Returns a shared SQLAlchemy engine instance."""
    global _engine
    if _engine is None:
        db_url = os.getenv("DB_CONNECTION_STRING")
        if db_url:
            _engine = create_engine(db_url, pool_pre_ping=True)
    return _engine


class DataLoader:
    def __init__(self, query_path):
        self.query_path = Path(query_path)

    def get_data(self, year=None):
        """
        Loads data from SQL file.
        If 'year' is provided, injects SQL into '-- FILTERS --' placeholder.
        """
        engine = get_engine()
        if engine is None:
            print("ERROR: DB_CONNECTION_STRING not found")
            return pd.DataFrame()

        if not self.query_path.exists():
            print(f"ERROR: Query file not found at: {self.query_path}")
            return pd.DataFrame()

        try:
            with open(self.query_path, "r") as f:
                query = f.read().strip()

            # --- Dynamic Year Injection ---
            if year:
                try:
                    # Validate year is an integer to prevent injection
                    safe_year = int(year)
                    # We use 1=1 in the base queries, so we just append AND ...
                    injection = (
                        f" AND EXTRACT(YEAR FROM transaction_date) = {safe_year}"
                    )
                    query = query.replace("-- FILTERS --", injection)
                except ValueError:
                    print(f"Invalid year format: {year}")

            df = pd.read_sql(query, engine)
            return df

        except Exception as e:
            print(f"ERROR: Failed to load data: {e}")
            return pd.DataFrame()
