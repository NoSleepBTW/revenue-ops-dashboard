DROP VIEW IF EXISTS rpt_customer_segmentation;

CREATE VIEW rpt_customer_segmentation AS
SELECT
    -- 1. SEGMENTATION
    CASE
        WHEN age < 25 THEN '(Under 25)'
        WHEN age BETWEEN 25
        AND 40 THEN '(25-40)'
        WHEN age BETWEEN 41
        AND 56 THEN '(41-56)'
        WHEN age >= 57 THEN '(57+)'
        ELSE 'Unknown'
    END AS age_generation,
    -- 2. PURCHASING POWER
    COUNT(DISTINCT client_id) AS active_customers,
    SUM(transaction_amount) AS total_spend,
    ROUND(AVG(transaction_amount), 2) AS avg_ticket_size,
    -- 3. RISK PROFILE
    SUM(fraud_loss_amount) AS total_fraud_loss,
    ROUND(
        (
            SUM(fraud_loss_amount) / NULLIF(SUM(transaction_amount), 0)
        ) * 100,
        3
    ) AS segment_risk_rate_percent,
    -- 4. FINANCIAL CONTEXT
    ROUND(AVG(credit_score), 0) AS avg_credit_score
FROM
    enriched_transactions
GROUP BY
    1
ORDER BY
    total_spend DESC;