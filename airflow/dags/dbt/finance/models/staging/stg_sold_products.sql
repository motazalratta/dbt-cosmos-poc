WITH source AS (
    SELECT *
    FROM {{ ref('sold_products') }}
)

SELECT
    license_plate,
    status,
    platform,
    created_at,
    shipped_at,
    sold_price,
    country,
    channel_ref,
    platform_fee
FROM source