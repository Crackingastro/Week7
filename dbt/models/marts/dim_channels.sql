{{
  config(
    materialized = 'table',
    unique_key = 'channel_key'
  )
}}

SELECT
  channel_key,
  channel_name,
  first_scraped_at,
  last_scraped_at,
  CASE
    WHEN channel_name ILIKE '%pharma%' THEN 'Pharmaceutical'
    WHEN channel_name ILIKE '%cosmetic%' THEN 'Cosmetic'
    ELSE 'Other'
  END AS channel_category
FROM {{ ref('stg_telegram_channels') }}