import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import markdown
from openai import OpenAI

# 1. Load Secrets
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECIPIENT_EMAIL_SECRET = os.environ.get("RECIPIENT_EMAIL", "")

# Parse multiple recipients (comma-separated)
recipients = [email.strip() for email in RECIPIENT_EMAIL_SECRET.split(",") if email.strip()]

# 2. Read the last two weeks of data from CSV
csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)

if len(df) >= 2:
    previous_stats = df.iloc[-2].to_dict()
    latest_stats = df.iloc[-1].to_dict()
else:
    previous_stats = "No previous week data available yet."
    latest_stats = df.iloc[-1].to_dict()

# 3. Build Prompt for OpenAI
prompt = f"""
You are an expert Instagram growth strategist for Halton Tennis Centre.

Compare this week's 7-day performance data with last week's data and write a concise weekly executive report.

NOTE ON METRICS:
- Reach, Views, and Profile Views represent 7-day snapshot metrics (non-cumulative).
- Followers represent the total cumulative account count.
- Always refer to content impressions as "Views".

PREVIOUS WEEK METRICS:
{previous_stats}

CURRENT WEEK METRICS:
{latest_stats}

Please structure your response with the following Markdown headings:

### 1. Executive Summary
Briefly summarize key wins and performance changes week-over-week.

### 2. Retrospective Performance Review
Compare current numbers to the previous week's metrics. Clearly list Followers, Reach, Views, Profile Views, Website Clicks, and Engagement Rate alongside their calculated change.

### 3. Action Items for Next Week
Provide 3 specific, actionable growth strategies tailored to Halton Tennis Centre for the upcoming week.
"""

# 4. Generate AI Insight via OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
ai_analysis_md = response.choices[0].message.content

# 5. Convert Markdown to HTML
html_content = markdown.markdown(ai_analysis_md)

email_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2 style="color: #1a365d;">Weekly Instagram Analytics & AI Report</h2>
    <p><strong>Date:</strong> {latest_stats.get('date')}</p>
    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;"/>
    {html_content}
    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;"/>
    <p style="font-size: 12px; color: #777; text-align: center;">
      Halton Tennis Centre • Chestnut End, Halton Village, Aylesbury, HP22 5PD
    </p>
  </body>
</html>
"""

# 6. Compose and Send Email
msg = MIMEMultipart('alternative')
msg['From'] = SENDER_EMAIL
msg['To'] = ", ".join(recipients)
msg['Subject'] = f"Weekly Instagram Analytics Report - {latest_stats.get('date')}"

msg.attach(MIMEText(email_html, 'html'))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, recipients, msg.as_string())

print(f"Report successfully sent to: {', '.join(recipients)}")
