SELECT
    transaction_date,
    COUNT(transaction_id) AS vol,
    SUM(transaction_amount) AS rev,
    SUM(
        CASE
            WHEN is_fraud = TRUE THEN 1
            ELSE 0
        END
    ) AS fraud_cases,
    SUM(fraud_loss_amount) AS fraud_loss
FROM
    enriched_transactions
WHERE
    1 = 1 -- FILTERS --
GROUP BY
    transaction_date
ORDER BY
    transaction_date;