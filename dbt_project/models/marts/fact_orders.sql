{{ config(
    materialized = 'incremental',
    unique_key   = 'order_id',
    on_schema_change = 'sync_all_columns'
) }}

SELECT
    order_id,
    customer_id,
    order_date,
    status,
    total_amount,
    region,
    updated_at,
    CURRENT_TIMESTAMP() AS dbt_loaded_at
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}