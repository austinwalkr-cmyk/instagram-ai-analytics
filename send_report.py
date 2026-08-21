import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)

if len(df) >= 2:
    previous_stats = df.iloc[-2].to_dict()
    latest_stats = df.iloc[-1].to_dict()
else:
    previous_stats = "No previous week data available yet."
    latest_stats = df.iloc[-1].to_dict()

prompt = f"""
You are an expert Instagram growth strategist for Halton Tennis Centre.

Compare this week's 7-day performance data with last week's data.

NOTE: Reach and Views are 7-day snapshot metrics (not cumulative totals). 
Followers represent cumulative account total. Use the term "Views" instead of "Impressions".

PREVIOUS WEEK METRICS:
{previous_stats}

CURRENT WEEK METRICS:
{latest_stats}

Please structure your response with:
### 1. Executive Summary
### 2. Retrospective Performance Review
### 3. Action Items for Next Week
"""

client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
ai_analysis_md = response.choices[0].message.content

html_content = markdown.markdown(ai_analysis_md)

email_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2>Weekly Instagram Analytics & AI Report</h2>
    <p><strong>Date:</strong> {latest_stats.get('date')}</p>
    <hr/>
    {html_content}
    <hr/>
    <p style="font-size: 12px; color: #777;">Halton Tennis Centre • Chestnut End, Halton Village, Aylesbury, HP22 5PD</p>
  </body>
</html>
"""

msg = MIMEMultipart('alternative')
msg['From'] = SENDER_EMAIL
msg['To'] = RECIPIENT_EMAIL
msg['Subject'] = f"Weekly Instagram Report - {latest_stats.get('date')}"

msg.attach(MIMEText(email_html, 'html'))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

print("Report sent using 'Views' metric!")
