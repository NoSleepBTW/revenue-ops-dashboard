SELECT
    CASE
        WHEN age < 25 THEN 'Gen Z (<25)'
        WHEN age BETWEEN 25
        AND 40 THEN 'Millennial (25-40)'
        WHEN age BETWEEN 41
        AND 60 THEN 'Gen X (41-60)'
        ELSE 'Senior (60+)'
    END AS age_group,
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
    age_group;