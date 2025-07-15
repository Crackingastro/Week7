{{
  config(
    materialized = 'table',
    unique_key = 'channel_key'
  )
}}

WITH channel_data AS (
  SELECT DISTINCT
    channel_name,  -- Changed from _channel to channel_name
    MIN(loaded_at) AS first_scraped_at,
    MAX(loaded_at) AS last_scraped_at
  FROM {{ ref('stg_telegram_messages') }}
  GROUP BY 1
)

SELECT
  MD5(channel_name) AS channel_key,  -- Changed from _channel to channel_name
  channel_name,
  first_scraped_at,
  last_scraped_at,
  CURRENT_TIMESTAMP AS dbt_loaded_at
FROM channel_data