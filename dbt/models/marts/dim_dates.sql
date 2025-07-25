{{
  config(
    materialized = 'table',
    unique_key = 'date_key'
  )
}}

WITH date_spine AS (
  SELECT DISTINCT
    DATE_TRUNC('day', message_date) AS date_key
  FROM {{ ref('stg_telegram_messages') }}
)

SELECT
  date_key,
  EXTRACT(YEAR FROM date_key) AS year,
  EXTRACT(QUARTER FROM date_key) AS quarter,
  EXTRACT(MONTH FROM date_key) AS month,
  EXTRACT(DAY FROM date_key) AS day,
  EXTRACT(DOW FROM date_key) AS day_of_week,
  TO_CHAR(date_key, 'Day') AS day_name
FROM date_spine