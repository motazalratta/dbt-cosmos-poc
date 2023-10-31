WITH source AS (
    SELECT *
    FROM {{ ref('transport_cost') }}
)

SELECT
    country,
    transport_cost
FROM source