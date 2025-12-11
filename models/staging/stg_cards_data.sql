-- Run with: duckdb dev.duckdb -s ".read models/staging/stg_cards_data.sql"
-- Transform Data
ALTER TABLE raw_cards_data
ALTER id TYPE SMALLINT;

-- Primary Key
ALTER TABLE raw_cards_data
ADD PRIMARY KEY (id);

ALTER TABLE raw_cards_data
ALTER client_id TYPE SMALLINT;

ALTER TABLE raw_cards_data
ALTER num_cards_issued TYPE TINYINT;

ALTER TABLE raw_cards_data
ALTER year_pin_last_changed TYPE SMALLINT;

ALTER TABLE raw_cards_data
ALTER has_chip TYPE BOOLEAN USING (has_chip = 'YES');

ALTER TABLE raw_cards_data
ALTER card_on_dark_web TYPE BOOLEAN USING (card_on_dark_web = 'YES');

-- Clean credit_limit (remove $, commas, spaces)
UPDATE raw_cards_data
SET
  credit_limit = REPLACE(
    REPLACE(REPLACE(credit_limit, '$', ''), ',', ''),
    ' ',
    ''
  );

ALTER TABLE raw_cards_data
ALTER credit_limit TYPE DECIMAL(14, 2) USING credit_limit::DECIMAL(14, 2);

-- Date/Timestamps
ALTER TABLE raw_cards_data
ADD COLUMN IF NOT EXISTS card_issued_date DATE;

ALTER TABLE raw_cards_data
ADD COLUMN IF NOT EXISTS card_expiration_date DATE;

UPDATE raw_cards_data
SET
  card_issued_date = CONCAT(
    RIGHT(acct_open_date, 4),
    '-',
    LEFT(acct_open_date, 2),
    '-01'
  )::DATE,
  card_expiration_date = CONCAT(RIGHT(expires, 4), '-', LEFT(expires, 2), '-01')::DATE;

-- Masked Card Number
ALTER TABLE raw_cards_data
ADD COLUMN IF NOT EXISTS card_number_masked VARCHAR;

UPDATE raw_cards_data
SET
  card_number_masked = CONCAT(
    LEFT(card_number::VARCHAR, 4),
    '-****-****-',
    RIGHT(card_number::VARCHAR, 4)
  );