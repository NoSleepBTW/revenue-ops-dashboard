-- Run: duckdb dev.duckdb -s ".read models/staging/stg_transactions_data.sql"
-- Transform Data
ALTER TABLE raw_transactions_data
ALTER id TYPE INTEGER;

-- Primary Key
ALTER TABLE raw_transactions_data
ADD PRIMARY KEY (id);

ALTER TABLE raw_transactions_data
ALTER client_id TYPE SMALLINT;

ALTER TABLE raw_transactions_data
ALTER card_id TYPE SMALLINT;

ALTER TABLE raw_transactions_data
ALTER merchant_id TYPE INTEGER;

ALTER TABLE raw_transactions_data
ALTER mcc TYPE SMALLINT;

ALTER TABLE raw_transactions_data
ALTER zip TYPE BIGINT;

-- Convert date and create seperate timestamp
ALTER TABLE raw_transactions_data
ADD COLUMN IF NOT EXISTS transaction_time VARCHAR;

UPDATE raw_transactions_data
SET
    transaction_time = strftime ("date"::TIMESTAMP, '%H:%M:%S');

ALTER TABLE raw_transactions_data
ALTER date TYPE DATE;

-- Clean amount: remove $ and commas → DECIMAL
UPDATE raw_transactions_data
SET
    amount = REPLACE(REPLACE(amount, '$', ''), ',', '');

ALTER TABLE raw_transactions_data
ALTER amount TYPE DECIMAL(14, 2) USING amount::DECIMAL(14, 2);