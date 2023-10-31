{% set BUYBAY_FEE_SOLD_PERCENT = 10 %}

WITH transport_cost_other AS (
    SELECT MIN(transport_cost) AS transport_cost
    FROM {{ ref('stg_transport_cost') }}
    WHERE UPPER(country) = 'OTHER'
),
platform_fees_other AS (
    SELECT MIN(sold_percent) AS sold_percent
    FROM {{ ref('stg_platform_fees') }}
    WHERE UPPER(platform) = 'OTHER'
),
fact_products AS (
    SELECT
        sold_products.license_plate,
        sold_products.status,
        sold_products.platform,
        sold_products.created_at,
        sold_products.shipped_at,
        sold_products.sold_price,
        sold_products.country,
        sold_products.channel_ref,
        COALESCE(
            sold_products.platform_fee,
            sold_products.sold_price * platform_fees.sold_percent / 100,
            sold_products.sold_price * platform_fees_other.sold_percent / 100
        ) AS platform_fee,
        graded_products.grading_cat,
        graded_products.grading_time,
        grading_fees.cost AS grading_fee,
        COALESCE(transport_cost.transport_cost, transport_cost_other.transport_cost) AS transport_cost,
        sold_products.sold_price * {{ BUYBAY_FEE_SOLD_PERCENT }} / 100 AS buybay_fee
    FROM {{ ref('stg_sold_products') }} AS sold_products
    LEFT JOIN {{ ref('stg_graded_products') }} AS graded_products
    ON UPPER(sold_products.license_plate) = UPPER(graded_products.license_plate)
    LEFT JOIN {{ ref('stg_grading_fees') }} AS grading_fees
    ON UPPER(graded_products.grading_cat) = UPPER(grading_fees.grading_cat)
    LEFT JOIN {{ ref('stg_transport_cost') }} AS transport_cost
    ON UPPER(sold_products.country) = UPPER(transport_cost.country)
    LEFT JOIN {{ ref('stg_platform_fees') }} AS platform_fees
    ON UPPER(sold_products.platform) = UPPER(platform_fees.platform)
    CROSS JOIN transport_cost_other
    CROSS JOIN platform_fees_other
)

SELECT
    license_plate,
    status,
    platform,
    created_at,
    shipped_at,
    country,
    channel_ref,
    grading_cat,
    grading_time,
    sold_price,
    grading_fee,
    round(platform_fee,2) AS platform_fee,
    round(buybay_fee,2) AS buybay_fee,
    transport_cost,
    round(sold_price - buybay_fee - transport_cost - platform_fee - grading_fee, 2) AS partner_payout
FROM fact_products