WITH source AS (
    SELECT *
    FROM {{ ref('grading_fees') }}
)

SELECT grading_cat, cost
FROM source