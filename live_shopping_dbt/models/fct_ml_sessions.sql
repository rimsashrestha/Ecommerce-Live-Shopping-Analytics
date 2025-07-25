{{ config(materialized='table') }}

WITH first_event AS (
  SELECT
    viewer_id,
    event_time,
    device_type,
    viewer_state,
    ROW_NUMBER() OVER (
      PARTITION BY viewer_id, DATE(event_time)
      ORDER BY event_time
    ) AS rn
  FROM {{ ref('stg_live_events') }}
),

joined AS (
  SELECT
    fct.*,
    evt.device_type,
    evt.viewer_state,
    CASE WHEN fct.dropped_out THEN 1 ELSE 0 END AS dropped_flag,
    CASE WHEN fct.orders_placed > 0 THEN 1 ELSE 0 END AS converted
  FROM {{ ref('fct_sessions') }} fct
  LEFT JOIN first_event evt
    ON fct.viewer_id = evt.viewer_id
    AND evt.rn = 1
    AND evt.event_time BETWEEN fct.session_start AND fct.session_end
)

SELECT * FROM joined

