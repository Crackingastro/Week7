

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
FROM "telegram_analytics"."star_staging"."stg_telegram_channels"