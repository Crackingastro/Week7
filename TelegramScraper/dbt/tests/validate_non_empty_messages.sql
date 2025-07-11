SELECT message_id
FROM {{ ref('stg_telegram_messages') }}
WHERE 
  message_text IS NULL 
  OR TRIM(message_text) = ''