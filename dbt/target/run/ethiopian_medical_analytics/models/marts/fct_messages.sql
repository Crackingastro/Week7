
  
    

  create  table "telegram_analytics"."star_analytics"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    

SELECT
  m.message_id,
  c.channel_key,
  d.date_key,
  m.message_text,
  LENGTH(m.message_text) AS message_length,
  m.view_count,
  
  -- Engagement metrics
  CASE 
    WHEN m.view_count > 0 THEN m.view_count::FLOAT / NULLIF(m.view_count, 0)
    ELSE NULL 
  END AS engagement_rate,
  
  -- Ethiopia mentions
  CASE 
    WHEN m.message_text ILIKE '%ethiopia%' THEN TRUE
    ELSE FALSE
  END AS mentions_ethiopia,
  
  m.loaded_at
FROM "telegram_analytics"."star_staging"."stg_telegram_messages" m
LEFT JOIN "telegram_analytics"."star_analytics"."dim_channels" c ON m.channel_name = c.channel_name
LEFT JOIN "telegram_analytics"."star_analytics"."dim_dates" d ON DATE_TRUNC('day', m.message_date) = d.date_key
  );
  