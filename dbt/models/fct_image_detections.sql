-- dbt/models/marts/fct_image_detections.sql
-- Fact table linking each message to its detected image objects

{{ config(materialized='table') }}

with raw_detections as (
    select
        message_id,
        detected_object_class,
        confidence_score
    from raw.raw_image_detections
),

valid_messages as (
    select distinct message_id
    from {{ ref('fct_messages') }}
)

select
    rd.message_id,
    rd.detected_object_class,
    rd.confidence_score
from raw_detections rd
join valid_messages vm
  on rd.message_id = vm.message_id
