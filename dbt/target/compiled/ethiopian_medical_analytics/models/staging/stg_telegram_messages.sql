

WITH combined_messages AS (
  SELECT id, text, date, views, _channel, _loaded_at
  FROM "telegram_analytics"."raw"."telegram_messages_chemed123"
  
  UNION ALL
  
  SELECT id, text, date, views, _channel, _loaded_at
  FROM "telegram_analytics"."raw"."telegram_messages_lobelia4cosmetics"
  
  UNION ALL
  
  SELECT id, text, date, views, _channel, _loaded_at
  FROM "telegram_analytics"."raw"."telegram_messages_tikvahpharma"
)

SELECT
  id::INTEGER AS message_id,
  text AS message_text,
  date::TIMESTAMP AS message_date,
  _channel AS channel_name,
  views::INTEGER AS view_count,
  _loaded_at::TIMESTAMP AS loaded_at
FROM combined_messages