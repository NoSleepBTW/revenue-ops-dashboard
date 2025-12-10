import duckdb
import pandas as pd
import pathlib
import json

con = duckdb.connect("../dev.duckdb")
raw_path = pathlib.Path("../data/raw")

print("Starting raw data load...\n")

for file_path in sorted(raw_path.glob("*.*")):
    if file_path.name.startswith("."):
        continue

    table_name = f"raw_{file_path.stem.lower()}"
    print(f"Loading {file_path.name}...", end=" ")

    try:
        if file_path.suffix == ".csv":
            df = pd.read_csv(file_path)

        elif file_path.suffix == ".json":
            with open(file_path) as f:
                data = json.load(f)

            if file_path.name == "mcc_codes.json":
                df = pd.DataFrame.from_dict(data, orient="index").reset_index(names="mcc")
            else:
                df = pd.read_json(file_path)

        else:
            print("skipped")
            continue

        rows = len(df)
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
        print(f"→ {table_name} ({rows:,} rows)")

    except Exception as e:
        print(f"failed → {e}")

print("\nData load complete.")
con.close()