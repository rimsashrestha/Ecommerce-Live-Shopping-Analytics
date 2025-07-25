{{ config(materialized='table') }}

WITH add_cart AS (
  SELECT
    viewer_id,
    stream_id,
    MIN(event_time) AS cart_time
  FROM {{ ref('stg_live_events') }}
  WHERE event_type = 'add_to_cart'
  GROUP BY viewer_id, stream_id
),

order_complete AS (
  SELECT
    viewer_id,
    stream_id,
    MIN(event_time) AS order_time
  FROM {{ ref('stg_live_events') }}
  WHERE event_type = 'order_completed'
  GROUP BY viewer_id, stream_id
)

SELECT
  a.viewer_id,
  a.stream_id,
  CONCAT(a.viewer_id, '-', a.stream_id) AS session_id,
  TIMESTAMP_DIFF(o.order_time, a.cart_time, MINUTE) AS click_to_purchase_lag_min
FROM add_cart a
JOIN order_complete o
  ON a.viewer_id = o.viewer_id AND a.stream_id = o.stream_id
WHERE o.order_time > a.cart_time

