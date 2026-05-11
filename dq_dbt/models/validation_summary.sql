{{ config(
    materialized='incremental',
    unique_key='RULE_NAME'
) }}

WITH max_time AS (
    SELECT COALESCE(MAX(EXECUTION_TIME), '1900-01-01'::TIMESTAMP) AS last_run
    FROM DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS
)

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

FROM DQ_FRAMEWORK.VALIDATION.VALIDATION_RESULTS vr

{% if is_incremental() %}
WHERE vr.EXECUTION_TIME > (SELECT last_run FROM max_time)
{% endif %}
GROUP BY RULE_NAME