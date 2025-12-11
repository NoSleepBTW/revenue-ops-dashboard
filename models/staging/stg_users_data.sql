-- Run with: duckdb dev.duckdb -s ".read models/staging/stg_users_data.sql"
-- Transform data
ALTER TABLE raw_users_data
ALTER id TYPE SMALLINT;

ALTER TABLE raw_users_data
ALTER id
SET
    NOT NULL;

ALTER TABLE raw_users_data ADD PRIMARY KEY (id);

ALTER TABLE raw_users_data
ALTER current_age TYPE TINYINT;

ALTER TABLE raw_users_data
ALTER retirement_age TYPE TINYINT;

ALTER TABLE raw_users_data
ALTER birth_year TYPE SMALLINT;

ALTER TABLE raw_users_data
ALTER birth_month TYPE TINYINT;

-- Currency
UPDATE raw_users_data
SET
    per_capita_income = REPLACE (REPLACE (per_capita_income, '$', ''), ',', ''),
    yearly_income = REPLACE (REPLACE (yearly_income, '$', ''), ',', ''),
    total_debt = REPLACE (REPLACE (total_debt, '$', ''), ',', '');

ALTER TABLE raw_users_data
ALTER per_capita_income TYPE INTEGER;

ALTER TABLE raw_users_data
ALTER yearly_income TYPE INTEGER;

ALTER TABLE raw_users_data
ALTER total_debt TYPE INTEGER;

ALTER TABLE raw_users_data
ALTER credit_score TYPE SMALLINT;

ALTER TABLE raw_users_data
ALTER num_credit_cards TYPE TINYINT;