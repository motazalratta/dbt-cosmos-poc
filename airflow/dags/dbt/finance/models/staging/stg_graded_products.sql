WITH source AS (
    SELECT *
    FROM {{ ref('graded_products') }}
)

SELECT
    License_plate AS license_plate,
    grading_cat,
    grading_time
FROM source