import duckdb
import pandas as pd
import pathlib
import json

# Setup & Connection
con = duckdb.connect("../dev.duckdb")
raw_path = pathlib.Path("../data/raw")
staging_dir = pathlib.Path('../models/staging')

# Load Raw Data
print("Starting raw data load...\n")

for file_path in sorted(raw_path.glob("*.*")):
    if file_path.name.startswith("."):
        continue

    table_name = f"raw_{file_path.stem.lower()}"
    print(f"Loading {file_path.name}", end=" ")

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

# Clean Data Using our Staging Files 
for sql_file in sorted(staging_dir.glob("*.sql")):
    file_name = sql_file.stem
    core_name = file_name.replace("stg_","")
    table_name = f"raw_{core_name}"
    
    print(f"Cleaning Table: {table_name}...")
    
    try:
        pre_change = con.execute(f"""
                                 SELECT column_name, data_type
                                 FROM information_schema.columns
                                 WHERE table_name = '{table_name}'
                                 """).fetchall()
        
        if pre_change:
            print(f"Existing Schema: {pre_change}")
        else:
            print(f"{table_name} not found.")
            
        with open(sql_file, "r") as f:
            query = f.read()
        
        con.execute(query)
        print(" → Success")
        
        post_change = con.execute(f"""
                                 SELECT column_name, data_type
                                 FROM information_schema.columns
                                 WHERE table_name = '{table_name}'
                                 """).fetchall()
        print(f"New Schema: {post_change}\n")
    
    except Exception as e:
        print(f"failed → {e}\n")
            
print("\nData load and stage complete.")
con.close()