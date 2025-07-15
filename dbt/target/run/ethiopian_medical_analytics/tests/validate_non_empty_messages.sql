
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT message_id
FROM "telegram_analytics"."star_staging"."stg_telegram_messages"
WHERE 
  message_text IS NULL 
  OR TRIM(message_text) = ''
  
  
      
    ) dbt_internal_test