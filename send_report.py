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

recipients = [email.strip() for email in RECIPIENT_EMAIL_SECRET.split(",") if email.strip()]

# 2. Read last two weeks of data
csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)

if len(df) >= 2:
    prev = df.iloc[-2].to_dict()
    curr = df.iloc[-1].to_dict()
else:
    prev = df.iloc[-1].to_dict()
    curr = df.iloc[-1].to_dict()

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

recipients = [email.strip() for email in RECIPIENT_EMAIL_SECRET.split(",") if email.strip()]

# 2. Read last two weeks of data
csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)

if len(df) >= 2:
    prev = df.iloc[-2].to_dict()
    curr = df.iloc[-1].to_dict()
else:
    prev = df.iloc[-1].to_dict()
    curr = df.iloc[-1].to_dict()

# Helper function to compute change
def calc_change(curr_val, prev_val, is_pct=False):
    try:
        c, p = float(curr_val), float(prev_val)
        diff = c - p
        if p == 0:
            pct_change = 0
        else:
            pct_change = (diff / p) * 100
        
        if is_pct:
            return f"{diff:+.1f}% pts"
        
        sign = "+" if diff > 0 else ""
        return f"{sign}{int(diff):,} ({pct_change:+.1f}%)"
    except:
        return "N/A"

# 3. Build Strict, Bulletproof HTML Table in Python
metrics_table_html = f"""
<table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
  <thead>
    <tr style="background-color: #f8fafc; text-align: left; border-bottom: 2px solid #e2e8f0;">
      <th style="padding: 10px; border: 1px solid #e2e8f0;">Metric</th>
      <th style="padding: 10px; border: 1px solid #e2e8f0;">Previous Week</th>
      <th style="padding: 10px; border: 1px solid #e2e8f0;">Current Week</th>
      <th style="padding: 10px; border: 1px solid #e2e8f0;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Followers</strong></td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(prev.get('followers',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(curr.get('followers',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{calc_change(curr.get('followers',0), prev.get('followers',0))}</td>
    </tr>
    <tr style="background-color: #f9f9f9;">
      <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Reach (7d)</strong></td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(prev.get('reach',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(curr.get('reach',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{calc_change(curr.get('reach',0), prev.get('reach',0))}</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Views (7d)</strong></td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(prev.get('views',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(curr.get('views',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{calc_change(curr.get('views',0), prev.get('views',0))}</td>
    </tr>
    <tr style="background-color: #f9f9f9;">
      <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Profile Views (7d)</strong></td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(prev.get('profile_views',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(curr.get('profile_views',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{calc_change(curr.get('profile_views',0), prev.get('profile_views',0))}</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Website Clicks</strong></td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(prev.get('website_clicks',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{int(curr.get('website_clicks',0)):,}</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{calc_change(curr.get('website_clicks',0), prev.get('website_clicks',0))}</td>
    </tr>
    <tr style="background-color: #f9f9f9;">
      <td style="padding: 8px; border: 1px solid #e2e8f0;"><strong>Engagement Rate</strong></td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{prev.get('engagement_rate',0)}%</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{curr.get('engagement_rate',0)}%</td>
      <td style="padding: 8px; border: 1px solid #e2e8f0;">{calc_change(curr.get('engagement_rate',0), prev.get('engagement_rate',0), is_pct=True)}</td>
    </tr>
  </tbody>
</table>
"""

# 4. Prompt OpenAI ONLY for text analysis
prompt = f"""
You are an expert Instagram growth strategist for Halton Tennis Centre.

Analyze the performance changes and provide ONLY two sections in Markdown:

### 1. Executive Summary
A concise paragraph highlighting key shifts in performance.

### 2. Action Items for Next Week
3 numbered, specific, practical growth recommendations.

Do NOT include any metrics lists or tables in your response.

PREVIOUS WEEK: {prev}
CURRENT WEEK: {curr}
"""

client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2  # Low temperature ensures highly consistent AI tone
)

ai_analysis_html = markdown.markdown(response.choices[0].message.content)

# 5. Assemble Structured Master HTML
email_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 650px; margin: 0 auto; padding: 20px;">
    <h2 style="color: #1a365d; margin-bottom: 5px;">Weekly Instagram Analytics Report</h2>
    <p style="color: #666; font-size: 14px; margin-top: 0;"><strong>Date:</strong> {curr.get('date')}</p>
    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;"/>
    
    {ai_analysis_html}

    <h3 style="color: #1a365d; margin-top: 25px;">3. Retrospective Performance Review</h3>
    {metrics_table_html}

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;"/>
    <p style="font-size: 12px; color: #777; text-align: center;">
      Halton Tennis Centre • Chestnut End, Halton Village, Aylesbury, HP22 5PD
    </p>
  </body>
</html>
"""

# 6. Send Email
msg = MIMEMultipart('alternative')
msg['From'] = SENDER_EMAIL
msg['To'] = ", ".join(recipients)
msg['Subject'] = f"Weekly Instagram Analytics Report - {curr.get('date')}"

msg.attach(MIMEText(email_html, 'html'))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, recipients, msg.as_string())

print("Consistently formatted report sent successfully!")

# 4. Prompt OpenAI ONLY for text analysis
prompt = f"""
You are an expert Instagram growth strategist for Halton Tennis Centre.

Analyze the performance changes and provide ONLY two sections in Markdown:

### 1. Executive Summary
A concise paragraph highlighting key shifts in performance.

### 2. Action Items for Next Week
3 numbered, specific, practical growth recommendations.

Do NOT include any metrics lists or tables in your response.

PREVIOUS WEEK: {prev}
CURRENT WEEK: {curr}
"""

client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2  # Low temperature ensures highly consistent AI tone
)

ai_analysis_html = markdown.markdown(response.choices[0].message.content)

# 5. Assemble Structured Master HTML
email_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 650px; margin: 0 auto; padding: 20px;">
    <h2 style="color: #1a365d; margin-bottom: 5px;">Weekly Instagram Analytics Report</h2>
    <p style="color: #666; font-size: 14px; margin-top: 0;"><strong>Date:</strong> {curr.get('date')}</p>
    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;"/>
    
    {ai_analysis_html}

    <h3 style="color: #1a365d; margin-top: 25px;">3. Retrospective Performance Review</h3>
    {metrics_table_html}

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;"/>
    <p style="font-size: 12px; color: #777; text-align: center;">
      Halton Tennis Centre • Chestnut End, Halton Village, Aylesbury, HP22 5PD
    </p>
  </body>
</html>
"""

# 6. Send Email
msg = MIMEMultipart('alternative')
msg['From'] = SENDER_EMAIL
msg['To'] = ", ".join(recipients)
msg['Subject'] = f"Weekly Instagram Analytics Report - {curr.get('date')}"

msg.attach(MIMEText(email_html, 'html'))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, recipients, msg.as_string())

print("Consistently formatted report sent successfully!")
