# 🛍️ Live Shopping Analytics Dashboard

A real-time analytics pipeline to track and segment customer behavior during live shopping streams. Built with **BigQuery**, **dbt**, **BigQuery ML**, and visualized through **Streamlit**.

---

## 🔧 Architecture Overview

- **Data Ingestion**:  
  Simulated live events (views, clicks, purchases) are generated via Python and streamed through **Google Pub/Sub** into **BigQuery**.

- **Data Modeling (dbt)**:  
  Models are built to structure and transform the data:
  - `fct_sessions`: raw session data
  - `rfm_analysis`: computes Recency, Frequency, Monetary scores
  - `train_customer_segments`: k-means clustering with BigQuery ML
  - `customer_segments_scored`: cluster assignment
  - `customer_segments_named`: human-readable labels (e.g., *High-Value Loyal*)

- **Analytics & Prediction**:
  - BigQuery ML models predict conversion probability
  - Outputs include session-level predictions and customer segments

- **Visualization (Streamlit)**:  
  - Interactive dashboard displaying session metrics, engagement, conversion stats, and segments
  - Filters by `device`, `location`, and `viewer_id`

---

## 📊 Key Metrics Displayed

- Total Sessions / Unique Viewers  
- Drop-off Rate  
- Average Session Duration  
- Conversion Rate / Probability  
- Click-to-Purchase Lag  
- Engagement Score  
- High-Intent Session Count  
- Customer Segments (RFM-based)

---

## 🚀 Deployment (Streamlit Cloud)

- File: `streamlit_app.py`
- Uses `google.cloud.bigquery` to query BigQuery
- Deploy by pushing to GitHub — Streamlit Cloud auto-redeploys

---

## 📦 Tech Stack

- Google Pub/Sub  
- BigQuery  
- dbt  
- BigQuery ML  
- Streamlit Cloud  
