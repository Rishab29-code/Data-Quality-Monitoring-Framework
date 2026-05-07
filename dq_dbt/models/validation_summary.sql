{{ config(
    materialized='incremental',
    unique_key='RULE_NAME'
) }}

SELECT
    RULE_NAME,
    COUNT(*) AS TOTAL_RUNS,

    SUM(
        CASE
            WHEN STATUS = 'PASS' THEN 1
            ELSE 0
        END
    ) AS PASSED_RUNS,

    SUM(
        CASE
            WHEN STATUS = 'FAIL' THEN 1
            ELSE 0
        END
    ) AS FAILED_RUNS,

    SUM(FAILED_COUNT) AS TOTAL_FAILED_RECORDS,

    ROUND(
        (
            SUM(
                CASE
                    WHEN STATUS = 'PASS' THEN 1
                    ELSE 0
                END
            ) * 100.0
        ) / COUNT(*),
        2
    ) AS SUCCESS_RATE

FROM DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS

{% if is_incremental() %}
WHERE EXECUTION_TIME >
(
    SELECT COALESCE(MAX(LAST_RUN), '1900-01-01')
    FROM {{ this }}
)
{% endif %}
GROUP BY RULE_NAME