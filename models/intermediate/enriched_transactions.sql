/* int_enriched_transactions will be the datamart for our reporting and analysis.
This is applicable because in real life, you may want to control what data your
Analyst have access to, without providing unrestricted access to dimensions.    */

-- Drop view if exists
DROP MATERIALIZED VIEW IF EXISTS enriched_transactions;

CREATE MATERIALIZED VIEW enriched_transactions AS
SELECT
    -- Primary Keys & Other Ids
    t.id AS transaction_id, t.client_id, t.card_id, t.mcc,

-- Transaction Details & Operations Data
    t.date AS transaction_date,
    t.transaction_time,
    t.amount AS transaction_amount,
    t.use_chip AS transaction_type,
    t.errors AS transaction_error,

    -- Merchant Details
    t.merchant_id, t.merchant_city, t.merchant_state, t.zip,

    -- Fraud Flagging & Calculating Loss
    COALESCE(f.is_fraud, FALSE) AS is_fraud,
    CASE
        WHEN t.errors IS NOT NULL THEN 'Rejected'
        WHEN COALESCE(f.is_fraud, FALSE) IS TRUE THEN 'Confirmed Fraud'
        ELSE 'Successful'
    END AS transaction_status,
    CASE
        WHEN COALESCE(f.is_fraud, FALSE) IS TRUE
        AND t.errors IS NULL THEN t.amount
        ELSE 0.00
    END AS fraud_loss_amount,

    -- Card Information (Dimension)
    c.card_brand,
    c.card_type,
    c.credit_limit,
    c.has_chip AS card_has_chip,
    c.card_on_dark_web,
    c.card_issued_date,
    c.num_cards_issued AS total_cards_issued_to_client,

    -- User Demographics (Dimension)
    u.gender,
    u.current_age AS age,
    u.num_credit_cards,
    u.yearly_income AS income,
    u.per_capita_income,
    u.credit_score,
    u.total_debt,
    u.latitude,
    u.longitude,

    -- Merchant Categories (Dimension)
    m.category AS merchant_category
FROM
    transactions_data AS t
    LEFT JOIN train_fraud_labels AS f ON t.id = f.id
    LEFT JOIN cards_data AS c ON t.card_id = c.id
    LEFT JOIN users_data AS u ON t.client_id = u.id
    LEFT JOIN mcc_codes AS m ON t.mcc = m.mcc
;

CREATE UNIQUE INDEX IF NOT EXISTS idx_int_transaction_id ON enriched_transactions (transaction_id);

CREATE INDEX IF NOT EXISTS idx_int_date_status ON enriched_transactions (
    transaction_date,
    transaction_status
);

CREATE INDEX IF NOT EXISTS idx_int_client_card ON enriched_transactions (client_id, card_id);

CREATE INDEX IF NOT EXISTS idx_int_mcc ON enriched_transactions (mcc);