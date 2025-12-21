SELECT
    DISTINCT EXTRACT(
        YEAR
        FROM
            transaction_date
    ) :: INT AS report_year
FROM
    enriched_transactions
ORDER BY
    1 DESC;