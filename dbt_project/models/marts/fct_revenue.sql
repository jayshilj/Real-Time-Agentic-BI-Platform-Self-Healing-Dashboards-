{{ config(
    materialized = 'incremental',
    unique_key   = 'revenue_id',
    on_schema_change = 'sync_all_columns'
) }}

SELECT
    revenue_id,
    order_id,
    revenue_date,
    amount,
    region,
    product_category,
    updated_at,
    CURRENT_TIMESTAMP() AS dbt_loaded_at
FROM {{ source('raw', 'revenue') }}

{% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}