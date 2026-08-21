import os
import json
import pandas as pd
from datetime import datetime
from instagrapi import Client

# Load Session Data & Username from Secrets
IG_SESSION_DATA = os.environ.get("IG_SESSION_DATA")
IG_USERNAME = os.environ.get("IG_USERNAME")

cl = Client()

# Load saved session settings directly into instagrapi
session_dict = json.loads(IG_SESSION_DATA)
cl.set_settings(session_dict)

# Fetch user account details
user_info = cl.user_info_by_username(IG_USERNAME)

# Attempt to fetch account insights (if professional/business account)
try:
    insights = cl.insights_account()
except Exception as e:
    print(f"Insights API notice: {e}")
    insights = {}

today_date = datetime.now().strftime("%Y-%m-%d")
csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)

# Extract real metrics
followers_count = user_info.follower_count
reach_val = insights.get("reach", 0)
impressions_val = insights.get("impressions", 0)
views_val = insights.get("profile_views", 0)

# Build new row
new_row = {
    "date": today_date,
    "followers": followers_count,
    "reach": reach_val if reach_val > 0 else df["reach"].iloc[-1],
    "impressions": impressions_val if impressions_val > 0 else df["impressions"].iloc[-1],
    "profile_views": views_val if views_val > 0 else df["profile_views"].iloc[-1],
    "website_clicks": 0,
    "engagement_rate": df["engagement_rate"].iloc[-1]
}

# Replace today's entry if already present, or append
df = df[df["date"] != today_date]
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
df.to_csv(csv_path, index=False)

print(f"Successfully recorded data for {today_date}: {followers_count} followers.")
