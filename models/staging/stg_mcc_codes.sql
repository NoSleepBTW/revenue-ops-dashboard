-- Transform Data
ALTER TABLE
    mcc_codes RENAME COLUMN "0" TO category;

-- Apply Type Casting & PK
ALTER TABLE
    mcc_codes
ALTER COLUMN
    mcc TYPE SMALLINT USING CAST(mcc AS SMALLINT),
ADD
    PRIMARY KEY (mcc);