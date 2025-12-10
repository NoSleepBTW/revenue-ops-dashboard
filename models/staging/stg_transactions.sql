-- sql/clean_transactions.sql
-- Run: duckdb dev.duckdb -s ".read models/staging/stg_transactions.sql"
-- Preview:
SELECT
    *
FROM
    raw_transactions_data
ORDER BY
    id ASC
LIMIT
    10;

-- 1. Cast IDs and numeric columns
ALTER TABLE raw_transactions_data
ALTER id TYPE BIGINT;

ALTER TABLE raw_transactions_data
ALTER client_id TYPE BIGINT;

ALTER TABLE raw_transactions_data
ALTER card_id TYPE BIGINT;

ALTER TABLE raw_transactions_data
ALTER merchant_id TYPE BIGINT;

ALTER TABLE raw_transactions_data
ALTER mcc TYPE BIGINT;

-- 2. Convert date and create seperate timestamp
ALTER TABLE raw_transactions_data
ADD COLUMN IF NOT EXISTS transaction_time VARCHAR;

UPDATE raw_transactions_data
SET
    transaction_time = strftime ("date"::TIMESTAMP, '%H:%M:%S');

ALTER TABLE raw_transactions_data
ALTER date TYPE DATE;

-- 3. Clean amount: remove $ and commas → DECIMAL
UPDATE raw_transactions_data
SET
    amount = REPLACE(REPLACE(amount, '$', ''), ',', '');

ALTER TABLE raw_transactions_data
ALTER amount TYPE DECIMAL(14, 2) USING amount::DECIMAL(14, 2);

-- 4. Clean categorical columns
ALTER TABLE raw_transactions_data
ALTER use_chip TYPE VARCHAR;

ALTER TABLE raw_transactions_data
ALTER merchant_city TYPE VARCHAR;

ALTER TABLE raw_transactions_data
ALTER merchant_state TYPE VARCHAR;

ALTER TABLE raw_transactions_data
ALTER errors TYPE VARCHAR;

-- 5. ZIP is often incomplete → keep as VARCHAR
ALTER TABLE raw_transactions_data
ALTER zip TYPE BIGINT;

-- 6. Add primary key
ALTER TABLE raw_transactions_data
ADD PRIMARY KEY (id);

-- Final preview
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE
FROM
    INFORMATION_SCHEMA.COLUMNS
WHERE
    TABLE_NAME = 'raw_transactions_data';

SELECT
    *
FROM
    raw_transactions_data
ORDER BY
    id ASC
LIMIT
    10;