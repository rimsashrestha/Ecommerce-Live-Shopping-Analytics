{{ config(materialized='view') }}

SELECT
  stream_id,
  streamer_name,
  stream_start_time,
  viewer_id,
  viewer_email,
  viewer_state,
  device_type,
  event_time,
  event_type,
  product_id,
  product_name,
  chat_message
FROM
  {{ source('live_shopping_raw', 'live_events') }}

