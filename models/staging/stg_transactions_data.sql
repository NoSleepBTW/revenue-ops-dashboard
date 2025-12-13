-- Transform Data
-- Create Timestamp
ALTER TABLE
    transactions_data
ADD
    COLUMN IF NOT EXISTS transaction_time VARCHAR(20);

-- Populate Time & Clean Amount (remove $, commas)
UPDATE
    transactions_data
SET
    transaction_time = TO_CHAR(
        CAST(date AS TIMESTAMP),
        'HH24:MI:SS'
    ),
    amount = CAST(
        REPLACE(
            REPLACE(CAST(amount AS TEXT), '$', ''),
            ',',
            ''
        ) AS DECIMAL(14, 2)
    );

-- Type Casting & PK
ALTER TABLE
    transactions_data
ALTER COLUMN
    id TYPE INTEGER USING CAST(id AS INTEGER),
ALTER COLUMN
    client_id TYPE SMALLINT USING CAST(client_id AS SMALLINT),
ALTER COLUMN
    card_id TYPE SMALLINT USING CAST(card_id AS SMALLINT),
ALTER COLUMN
    merchant_id TYPE INTEGER USING CAST(merchant_id AS INTEGER),
ALTER COLUMN
    mcc TYPE SMALLINT USING CAST(mcc AS SMALLINT),
ALTER COLUMN
    zip TYPE BIGINT USING CAST(zip AS BIGINT),
ALTER COLUMN
    date TYPE DATE USING CAST(date AS DATE),
ALTER COLUMN
    amount TYPE DECIMAL(14, 2) USING CAST(amount AS DECIMAL(14, 2)),
ADD
    PRIMARY KEY (id);