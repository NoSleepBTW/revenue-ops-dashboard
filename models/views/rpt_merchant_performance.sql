DROP VIEW IF EXISTS rpt_merchant_performance;

CREATE VIEW rpt_merchant_performance AS
SELECT
    -- Category
    merchant_category,
    -- Revenue Generation
    COUNT(transaction_id) AS transaction_volume,
    SUM(transaction_amount) AS total_revenue,
    -- Risk Metrics
    SUM(fraud_loss_amount) AS total_fraud_loss,
    ROUND(
        (
            SUM(fraud_loss_amount) / NULLIF(SUM(transaction_amount), 0)
        ) * 100,
        2
    ) AS fraud_loss_rate_percent,
    -- Profitability (Revenue - Loss)
    (SUM(transaction_amount) - SUM(fraud_loss_amount)) AS net_revenue,
    -- Context
    ROUND(AVG(transaction_amount), 2) AS avg_ticket_size
FROM
    enriched_transactions
GROUP BY
    1
ORDER BY
    net_revenue DESC;