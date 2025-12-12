-- Transform Data
-- Clean Credit Limit (remove $, commas, spaces)
UPDATE cards_data
SET credit_limit = CAST(
  REPLACE(
    REPLACE(
      REPLACE(CAST(credit_limit AS TEXT), '$', ''),
      ',',
      ''
    ),
    ' ',
    ''
  ) AS DECIMAL(14, 2)
);

-- Type Casting & PK
ALTER TABLE cards_data
ALTER COLUMN id TYPE SMALLINT USING CAST(id AS SMALLINT),
ALTER COLUMN client_id TYPE SMALLINT USING CAST(client_id AS SMALLINT),
ALTER COLUMN num_cards_issued TYPE SMALLINT USING CAST(
  num_cards_issued AS SMALLINT
),
ALTER COLUMN year_pin_last_changed TYPE SMALLINT USING CAST(
  year_pin_last_changed AS SMALLINT
),
ALTER COLUMN has_chip TYPE BOOLEAN USING (has_chip = 'YES'),
ALTER COLUMN card_on_dark_web TYPE BOOLEAN USING (card_on_dark_web = 'YES'),
ALTER COLUMN credit_limit TYPE DECIMAL(14, 2) USING CAST(
  credit_limit AS DECIMAL(14, 2)
),
ADD PRIMARY KEY (id);

-- Date Parsing & Masking PII
ALTER TABLE cards_data
ADD COLUMN IF NOT EXISTS card_issued_date DATE,
ADD COLUMN IF NOT EXISTS card_expiration_date DATE,
ADD COLUMN IF NOT EXISTS card_number_masked VARCHAR(19);

UPDATE cards_data
SET card_issued_date = TO_DATE(
  CONCAT(
    RIGHT(acct_open_date, 4),
    '-',
    LEFT(acct_open_date, 2),
    '-01'
  ),
  'YYYY-MM-DD'
),
card_expiration_date = TO_DATE(
  CONCAT(RIGHT(expires, 4), '-', LEFT(expires, 2), '-01'),
  'YYYY-MM-DD'
),
card_number_masked = CONCAT(
  LEFT(CAST(card_number AS VARCHAR), 4),
  '-****-****-',
  RIGHT(CAST(card_number AS VARCHAR), 4)
);

-- Cleanup and Drop Old Dirty Columns
ALTER TABLE cards_data DROP COLUMN acct_open_date,
DROP COLUMN expires,
DROP COLUMN card_number;
