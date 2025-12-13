-- Transform Data
-- Standardize 'is_fraud' column from 'Yes'/'No' string to BOOLEAN
UPDATE
    train_fraud_labels
SET
    is_fraud = (is_fraud = 'Yes');

-- Apply Type Casting & PK
ALTER TABLE
    train_fraud_labels
ALTER COLUMN
    id TYPE BIGINT USING CAST(id AS BIGINT),
ALTER COLUMN
    is_fraud TYPE BOOLEAN USING CAST(is_fraud AS BOOLEAN),
ADD
    PRIMARY KEY (id);