-- Transform Data
-- Clean Currency (remove $, commas)
UPDATE users_data
SET per_capita_income = CAST(
  REPLACE(
    REPLACE(
      CAST(per_capita_income AS TEXT),
      '$',
      ''
    ),
    ',',
    ''
  ) AS INTEGER
),
yearly_income = CAST(
  REPLACE(
    REPLACE(
      CAST(yearly_income AS TEXT),
      '$',
      ''
    ),
    ',',
    ''
  ) AS INTEGER
),
total_debt = CAST(
  REPLACE(
    REPLACE(
      CAST(total_debt AS TEXT),
      '$',
      ''
    ),
    ',',
    ''
  ) AS INTEGER
);

-- Type Casting & PK
ALTER TABLE users_data
ALTER COLUMN id TYPE SMALLINT USING CAST(id AS SMALLINT),
ALTER COLUMN current_age TYPE SMALLINT USING CAST(current_age AS SMALLINT),
ALTER COLUMN retirement_age TYPE SMALLINT USING CAST(
  retirement_age AS SMALLINT
),
ALTER COLUMN birth_year TYPE SMALLINT USING CAST(birth_year AS SMALLINT),
ALTER COLUMN birth_month TYPE SMALLINT USING CAST(birth_month AS SMALLINT),
ALTER COLUMN per_capita_income TYPE INTEGER USING CAST(
  per_capita_income AS INTEGER
),
ALTER COLUMN yearly_income TYPE INTEGER USING CAST(yearly_income AS INTEGER),
ALTER COLUMN total_debt TYPE INTEGER USING CAST(total_debt AS INTEGER),
ALTER COLUMN credit_score TYPE SMALLINT USING CAST(credit_score AS SMALLINT),
ALTER COLUMN num_credit_cards TYPE SMALLINT USING CAST(
  num_credit_cards AS SMALLINT
),
ADD PRIMARY KEY (id);
