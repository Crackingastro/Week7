SELECT message_id
FROM "telegram_analytics"."star_staging"."stg_telegram_messages"
WHERE 
  message_text IS NULL 
  OR TRIM(message_text) = ''