-- Run with: duckdb dev.duckdb -s ".read models/staging/stg_mcc_codes.sql"
-- Transform data
ALTER TABLE raw_mcc_codes RENAME "0" TO category;

ALTER TABLE raw_mcc_codes
ALTER mcc TYPE SMALLINT;

ALTER TABLE raw_mcc_codes
ALTER mcc
SET
    NOT NULL;

ALTER TABLE raw_mcc_codes ADD PRIMARY KEY (mcc);