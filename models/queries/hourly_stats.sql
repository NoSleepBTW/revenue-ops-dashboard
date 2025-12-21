SELECT
    EXTRACT(
        HOUR
        FROM
            transaction_time :: time
    ) AS hour_of_day,
    COUNT(transaction_id) AS vol,
    SUM(
        CASE
            WHEN is_fraud = TRUE THEN 1
            ELSE 0
        END
    ) AS fraud_cases
FROM
    enriched_transactions
WHERE
    1 = 1 -- FILTERS --
GROUP BY
    hour_of_day
ORDER BY
    hour_of_day;