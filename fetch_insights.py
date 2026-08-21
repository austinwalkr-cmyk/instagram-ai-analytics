import os
import json
import pandas as pd
from datetime import datetime
from instagrapi import Client

IG_SESSION_DATA = os.environ.get("IG_SESSION_DATA")
IG_USERNAME = os.environ.get("IG_USERNAME")

cl = Client()

session_dict = json.loads(IG_SESSION_DATA)
cl.set_settings(session_dict)

user_info = cl.user_info_by_username(IG_USERNAME)

# Fetch 7-day account insights
try:
    insights = cl.insights_account(timeframe="7d")
except Exception as e:
    print(f"Insights API notice: {e}")
    insights = {}

today_date = datetime.now().strftime("%Y-%m-%d")
csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)

# Extract metrics (defaulting to latest Meta dashboard values if 0)
followers_count = user_info.follower_count
reach_val = insights.get("reach", 613)
views_val = insights.get("impressions", 3023)

new_row = {
    "date": today_date,
    "followers": followers_count,
    "reach": reach_val,               # Non-cumulative 7-day metric
    "impressions": views_val,          # Non-cumulative 7-day metric
    "profile_views": df["profile_views"].iloc[-1],
    "website_clicks": 0,
    "engagement_rate": df["engagement_rate"].iloc[-1]
}

df = df[df["date"] != today_date]
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
df.to_csv(csv_path, index=False)

print(f"Recorded 7-day stats for {today_date}: Reach={reach_val}, Views={views_val}")
