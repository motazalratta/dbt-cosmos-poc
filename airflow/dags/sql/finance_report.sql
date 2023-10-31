SELECT
  FORMAT_DATE('%Y-%m-%d', DATE_TRUNC(created_at, DAY)) date,
  platform,
  ROUND(SUM(grading_fee + platform_fee + buybay_fee),2) AS total_fee,
  ROUND(SUM(transport_cost),2) AS total_transport_cost,
  ROUND(SUM(partner_payout),2) AS total_partner_payout
FROM
  `{{ params.source_table_name }}`
GROUP BY
  1,
  2
ORDER BY
  1