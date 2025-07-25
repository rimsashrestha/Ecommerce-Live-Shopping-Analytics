
# eCommerce: Live Shopping Analytics

This project is an end-to-end analytics pipeline that captures, processes, and visualizes real-time viewer behavior during live shopping streams. Built for brands looking to boost engagement and conversion, the system provides actionable insights using simulated user data, predictive models, and interactive dashboards.

Built with **BigQuery**, **dbt**, **BigQuery ML**, and visualized through **Streamlit**.

---

## What It Does

- Simulates live stream shopping events (views, clicks, purchases, exits)
- Ingests data in real time using Google Cloud Pub/Sub
- Transforms raw events into sessions and KPIs via dbt in BigQuery
- Applies ML models (via BigQuery ML) to predict churn and engagement
- Visualizes live insights in a Streamlit dashboard

---
##  Architecture Overview

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

## Key Metrics Displayed

- Total Sessions / Unique Viewers  
- Drop-off Rate  
- Average Session Duration  
- Conversion Rate / Probability  
- Click-to-Purchase Lag  
- Engagement Score  
- High-Intent Session Count  
- Customer Segments (RFM-based)

## Tech Stack

| Layer            | Tool/Technology                         |
|------------------|------------------------------------------|
| Event Simulation | Python, Puppeteer                       |
| Streaming        | Google Pub/Sub                          |
| Data Warehouse   | Google BigQuery (Bronze/Silver/Gold)    |
| Transformation   | dbt (Data Build Tool)                   |
| Machine Learning | BigQuery ML                             |
| Dashboard        | Streamlit                               |

---
## Project Structure
.
├── streamlit_app.py              # Streamlit dashboard
├── publish_events.py            # Event simulator
├── synthetic_*.csv              # Sample datasets
├── live_shopping_dbt/           # dbt models and transformation layers
│   ├── models/
│   ├── seeds/
│   └── dbt_project.yml
└── .streamlit/secrets.toml      # Config (not committed)
---
### How to View the Streamlit Dashboard

To explore the interactive live shopping analytics dashboard on your local machine, follow these steps:

#### Step 1: Clone the Repository
```bash
git clone https://github.com/rimsashrestha/Ecommerce-Live-Shopping-Analytics.git
cd Ecommerce-Live-Shopping-Analytics

### Step 2: Install Dependencies
Make sure you have Python 3.8 or higher installed. Then install the required Python packages:
```bash
pip install -r requirements.txt

### Step 3: Launch the Dashboard
Run the following command to start the Streamlit app:
```bash
streamlit run streamlit_app.py



