{{ config(
    materialized = 'incremental',
    unique_key   = 'shipment_id',
    on_schema_change = 'sync_all_columns'
) }}

SELECT
    shipment_id,
    order_id,
    supplier_id,
    shipment_date,
    delivery_date,
    status,
    delay_days,
    updated_at,
    CURRENT_TIMESTAMP() AS dbt_loaded_at
FROM {{ source('raw', 'shipments') }}

{% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}