import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st

## COMMENT OUT or REMOVE GCP auth during local testing
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_info(
     st.secrets["gcp_service_account"]
 )
 client = bigquery.Client(credentials=credentials, project=st.secrets["gcp_service_account"]["project_id"])

#  MOCK MODE: Use preloaded CSVs or skip querying for demo
##client = None


st.set_page_config(page_title="Live Shopping Predictions", layout="wide")
st.title("🛍️ Session Conversion Predictions")

# Click-to-Purchase Lag Query
lag_query = """
SELECT AVG(click_to_purchase_lag_min) AS avg_lag
FROM `live_shopping_analytics.fct_click_to_purchase_lag`
"""

# Engagement Score Query
engagement_query = """
SELECT AVG(engagement_score) AS avg_score
FROM `live_shopping_analytics.fct_engagement_score`
"""

# Viewer Count Per Minute
viewer_count_query = """
SELECT
  DATETIME_TRUNC(event_time, MINUTE) AS minute,
  COUNT(DISTINCT viewer_id) AS active_viewers
FROM `live_shopping_analytics.stg_live_events`
GROUP BY minute
ORDER BY minute
"""

# Avg Session Duration
avg_session_query = """
SELECT
  ROUND(AVG(session_duration_sec)/60, 1) AS avg_minutes
FROM `live_shopping_analytics.fct_sessions`
"""

# Drop-off Rate
dropoff_rate_query = """
SELECT
  ROUND(100 * (1 - AVG(conversion_probability)), 1) AS dropoff_pct
FROM `live_shopping_analytics.predicted_conversions`
"""


@st.cache_data(ttl=600)
def load_predictions():
    query = """
    SELECT
      session_id, viewer_id, stream_id,
      device_type, viewer_state,
      conversion_probability
    FROM `live_shopping_analytics.predicted_conversions`
    ORDER BY conversion_probability DESC
    LIMIT 500
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=600)
def load_customer_segments():
    query = """
    SELECT 
        viewer_id,
        recency,
        frequency,
        monetary,
        segment_name
    FROM `live-shopping-analytics-466418.live_shopping_analytics.customer_segments_named`
    """
    return client.query(query).to_dataframe()

segments_df = load_customer_segments()

df = load_predictions()
viewer_counts = client.query(viewer_count_query).to_dataframe()
avg_session = client.query(avg_session_query).to_dataframe()
dropoff = client.query(dropoff_rate_query).to_dataframe()
lag_df = client.query(lag_query).to_dataframe()
engage_df = client.query(engagement_query).to_dataframe()


# Filters
col1, col2 = st.columns(2)

# --- KPI Calculations ---
total_sessions = len(df)
unique_viewers = df["viewer_id"].nunique()
avg_conversion = df["conversion_probability"].mean()
high_intent = (df["conversion_probability"] > 0.8).sum()

# --- KPI Display ---

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Sessions", total_sessions)
kpi2.metric("Unique Viewers", unique_viewers)
kpi3.metric("Avg. Conversion", f"{avg_conversion:.2%}")
kpi4.metric("High-Intent Sessions", high_intent)

kpi5, kpi6, kpi7, kpi8 = st.columns(4)
kpi5.metric("Drop-off Rate", f"{dropoff['dropoff_pct'][0]}%")
kpi6.metric("Avg. Session Duration", f"{avg_session['avg_minutes'][0]} min")
kpi7.metric("Click-to-Purchase Lag", f"{lag_df['avg_lag'][0]:.1f} min")
kpi8.metric("Engagement Score", f"{engage_df['avg_score'][0]:.1f}")

with col1:
    selected_device = st.selectbox("Device Type", ["All"] + sorted(df.device_type.dropna().unique()))
with col2:
    selected_state = st.selectbox("Viewer State", ["All"] + sorted(df.viewer_state.dropna().unique()))

if selected_device != "All":
    df = df[df.device_type == selected_device]
if selected_state != "All":
    df = df[df.viewer_state == selected_state]

# KPI
avg_conv = df["conversion_probability"].mean()
st.metric("Average Conversion Probability", f"{avg_conv:.2%}")

# Main Table
st.dataframe(df.reset_index(drop=True), use_container_width=True)

# 📈 Enhancement 1: Conversion Probability Histogram
st.subheader("📈 Conversion Probability Distribution")
fig, ax = plt.subplots()
df["conversion_probability"].hist(bins=20, ax=ax)
ax.set_xlabel("Conversion Probability")
ax.set_ylabel("Number of Sessions")
st.pyplot(fig)

# 🎯 Enhancement 2: Top 10 High-Probability Sessions
st.subheader("🎯 Top 10 Sessions to Retarget")
top10 = df.sort_values("conversion_probability", ascending=False).head(10)
st.dataframe(top10.reset_index(drop=True), use_container_width=True)

st.subheader("📊 Viewer Count Per Minute")
viewer_counts = viewer_counts.rename(columns={"minute": "Time", "active_viewers": "Active Viewers"})
viewer_counts = viewer_counts.set_index("Time")
st.line_chart(viewer_counts)

st.subheader("🧠 Customer Segments")
st.dataframe(segments_df)

# 📺 Enhancement 3: Average Probability by Stream
st.subheader("📺 Average Conversion Probability by Stream")
avg_by_stream = df.groupby("stream_id")["conversion_probability"].mean().sort_values(ascending=False)
st.dataframe(avg_by_stream.reset_index())

