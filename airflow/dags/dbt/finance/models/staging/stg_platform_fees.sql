WITH source AS (
    SELECT *
    FROM {{ ref('platform_fees') }}
)

SELECT platform, sold_percent
FROM source