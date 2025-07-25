{{ config(materialized='table') }}

SELECT
  session_id,
  viewer_id,
  stream_id,
  session_duration_sec,
  total_events,
  add_to_cart_count,
  orders_placed,
  dropped_out,
  -- Engagement scoring formula (0–100 scale)
  ROUND(
    0.4 * total_events +
    0.3 * add_to_cart_count +
    0.3 * session_duration_sec / 60, 2
  ) AS engagement_score
FROM {{ ref('fct_sessions') }}

