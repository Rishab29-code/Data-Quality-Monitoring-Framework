{{ config(
    materialized='incremental'
) }}

WITH source_data AS (

    SELECT
        "id" AS product_id,
        "title" as title,
        "price" as price

    FROM DQ_FRAMEWORK.RAW.RAW_PRODUCTS
),

existing_current AS (

    {% if is_incremental() %}

    SELECT *
    FROM {{ this }}
    WHERE is_current = TRUE

    {% else %}

    SELECT NULL AS product_id,
           NULL AS title,
           NULL AS price
    WHERE FALSE

    {% endif %}
),

changed_records AS (

    SELECT s.*
    FROM source_data s
    LEFT JOIN existing_current e
    ON s.product_id = e.product_id

    WHERE e.product_id IS NULL
       OR s.price != e.price
       OR s.title != e.title
)

SELECT
    product_id,
    title,
    price,
    CURRENT_TIMESTAMP() AS effective_start_date,
    NULL AS effective_end_date,
    TRUE AS is_current

FROM changed_records