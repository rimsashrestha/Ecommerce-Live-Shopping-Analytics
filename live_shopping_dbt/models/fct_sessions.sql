{{ config(materialized='table') }}

WITH base AS (
  SELECT
    *,
    TIMESTAMP_DIFF(
      event_time,
      LAG(event_time) OVER (PARTITION BY viewer_id ORDER BY event_time),
      MINUTE
    ) AS minutes_since_last_event
  FROM {{ ref('stg_live_events') }}
),

sessionized AS (
  SELECT
    *,
    -- New session if more than 30 minutes since last event
    SUM(CASE WHEN minutes_since_last_event > 30 OR minutes_since_last_event IS NULL THEN 1 ELSE 0 END)
      OVER (PARTITION BY viewer_id ORDER BY event_time) AS session_num
  FROM base
)

SELECT
  CONCAT(viewer_id, '-', session_num) AS session_id,
  viewer_id,
  stream_id,
  MIN(event_time) AS session_start,
  MAX(event_time) AS session_end,
  TIMESTAMP_DIFF(MAX(event_time), MIN(event_time), SECOND) AS session_duration_sec,
  COUNT(*) AS total_events,
  COUNTIF(event_type = 'add_to_cart') AS add_to_cart_count,
  COUNTIF(event_type = 'order_completed') AS orders_placed,
  COUNTIF(event_type = 'stream_exit') > 0 AS dropped_out
FROM sessionized
GROUP BY viewer_id, stream_id, session_num

