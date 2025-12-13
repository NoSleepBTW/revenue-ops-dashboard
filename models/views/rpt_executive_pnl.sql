DROP VIEW IF EXISTS rpt_executive_pnl;

CREATE VIEW rpt_executive_pnl AS WITH monthly_stats AS (
    SELECT
        DATE_TRUNC('month', transaction_date) :: DATE AS report_month,
        SUM(transaction_amount) AS revenue,
        COUNT(transaction_id) AS units,
        SUM(fraud_loss_amount) AS fraud_loss,
        COUNT(
            CASE
                WHEN transaction_error IS NOT NULL THEN 1
            END
        ) AS technical_errors
    FROM
        enriched_transactions
    GROUP BY
        1
)
SELECT
    TO_CHAR(report_month, 'YYYY-MM') AS report_month,
    -- Financial Metrics (Revenue, Volume, Efficiency)
    revenue AS total_revenue,
    ROUND(
        (
            (
                revenue - LAG(revenue, 12) OVER (
                    ORDER BY
                        report_month
                )
            ) / NULLIF(
                LAG(revenue, 12) OVER (
                    ORDER BY
                        report_month
                ),
                0
            )
        ) * 100,
        2
    ) AS revenue_growth_yoy_percent,
    units AS total_transactions,
    ROUND(
        (
            (
                units - LAG(units, 12) OVER (
                    ORDER BY
                        report_month
                ) :: DECIMAL
            ) / NULLIF(
                LAG(units, 12) OVER (
                    ORDER BY
                        report_month
                ),
                0
            )
        ) * 100,
        2
    ) AS transaction_growth_yoy_percent,
    ROUND(revenue / NULLIF(units, 0), 2) AS avg_ticket_size,
    ROUND(
        (
            (revenue / NULLIF(units, 0)) - (
                LAG(revenue, 12) OVER (
                    ORDER BY
                        report_month
                ) / NULLIF(
                    LAG(units, 12) OVER (
                        ORDER BY
                            report_month
                    ),
                    0
                )
            )
        ) / NULLIF(
            (
                LAG(revenue, 12) OVER (
                    ORDER BY
                        report_month
                ) / NULLIF(
                    LAG(units, 12) OVER (
                        ORDER BY
                            report_month
                    ),
                    0
                )
            ),
            0
        ) * 100,
        2
    ) AS avg_ticket_growth_yoy_percent,
    -- Risk & Operations Metrics (Fraud, Reliability)
    fraud_loss AS total_fraud_loss,
    ROUND((fraud_loss / NULLIF(revenue, 0)) * 100, 2) AS fraud_loss_rate_percent,
    ROUND(
        (technical_errors :: DECIMAL / NULLIF(units, 0)) * 100,
        2
    ) AS technical_failure_rate_percent
FROM
    monthly_stats
WHERE
    revenue > 0
ORDER BY
    report_month DESC;