import os
import pandas as pd
from datetime import datetime
from instagrapi import Client

# Read credentials from GitHub Secrets
IG_USERNAME = os.environ.get("IG_USERNAME")
IG_PASSWORD = os.environ.get("IG_PASSWORD")

# Authenticate with Instagram directly
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)

# Pull account insights
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

print(f"Successfully pulled live Instagram insights for {today_date}!")
