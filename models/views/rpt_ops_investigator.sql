DROP VIEW IF EXISTS rpt_ops_investigator;

CREATE VIEW rpt_ops_investigator AS
SELECT
    -- Identifiers
    transaction_id,
    client_id,
    -- Time Context
    transaction_date,
    EXTRACT(
        HOUR
        FROM
            transaction_time :: TIME
    ) AS transaction_hour,
    -- Value
    transaction_amount,
    -- Risk Factors
    merchant_category,
    merchant_state AS jurisdiction,
    -- Fraud Flags
    is_fraud,
    transaction_status,
    transaction_error
FROM
    enriched_transactions
WHERE
    -- Filter: Fraud, Rejections, or Errors
    is_fraud = TRUE
    OR transaction_status = 'Rejected'
    OR transaction_error IS NOT NULL
ORDER BY
    transaction_amount DESC;