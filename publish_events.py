from google.cloud import pubsub_v1
import pandas as pd
import json
import time

# --- CONFIG ---
project_id = "live-shopping-analytics-466418"
topic_id = "live-shopping-events"
csv_file = "/Users/sarahxiong/Desktop/Live_shopping_project/synthetic_5k_live_shopping_events.csv"  # update path if needed

# --- SETUP ---
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

df = pd.read_csv(csv_file)

# --- SIMULATE EVENTS ---
for i, row in df.iterrows():
    message = json.dumps(row.to_dict()).encode("utf-8")
    publisher.publish(topic_path, message)
    print(f"Published event {i+1}")
    time.sleep(0.5)  # 5 events/second (smooth for demo)
 

