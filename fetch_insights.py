import os
import json
import pandas as pd
from datetime import datetime
from instagrapi import Client

# Load Session Data & Username from Secrets
IG_SESSION_DATA = os.environ.get("IG_SESSION_DATA")
IG_USERNAME = os.environ.get("IG_USERNAME")

cl = Client()

# Load full saved session settings directly into instagrapi
session_dict = json.loads(IG_SESSION_DATA)
cl.set_settings(session_dict)

# Fetch account insights using pre-authenticated session
insights = cl.insights_account()

today_date = datetime.now().strftime("%Y-%m-%d")
csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)

# Extract metrics
reach_val = insights.get("reach", df["reach"].iloc[-1])
impressions_val = insights.get("impressions", df["impressions"].iloc[-1])
views_val = insights.get("profile_views", df["profile_views"].iloc[-1])

# Append or update today's record
new_row = {
    "date": today_date,
    "followers": cl.user_info_by_username(IG_USERNAME).follower_count,
    "reach": reach_val,
    "impressions": impressions_val,
    "profile_views": views_val,
    "website_clicks": 0,
    "engagement_rate": df["engagement_rate"].iloc[-1]
}

df = df[df["date"] != today_date]
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
df.to_csv(csv_path, index=False)

print(f"Successfully pulled live Instagram insights for {today_date} using pre-authenticated session!")
