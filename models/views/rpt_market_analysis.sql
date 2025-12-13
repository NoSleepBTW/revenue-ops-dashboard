DROP VIEW IF EXISTS rpt_market_analysis;

CREATE VIEW rpt_market_analysis AS
SELECT
    -- 1. MARKET JURISDICTION
    merchant_state AS jurisdiction,
    CASE
        WHEN LENGTH(merchant_state) = 2 THEN 'Domestic'
        ELSE 'International'
    END AS jurisdiction_type,
    -- 2. REVENUE PERFORMANCE
    SUM(transaction_amount) AS total_market_revenue,
    RANK() OVER (
        ORDER BY
            SUM(transaction_amount) DESC
    ) AS market_rank,
    -- 3. RISK PROFILE
    SUM(fraud_loss_amount) AS total_market_loss,
    ROUND(
        (
            SUM(fraud_loss_amount) / NULLIF(SUM(transaction_amount), 0)
        ) * 100,
        2
    ) AS risk_rate_percent,
    -- 4. OPERATIONAL METRICS
    COUNT(transaction_id) AS transaction_volume,
    ROUND(AVG(transaction_amount), 2) AS avg_ticket_size
FROM
    enriched_transactions
WHERE
    merchant_state IS NOT NULL
GROUP BY
    1,
    2
ORDER BY
    total_market_revenue DESC;