import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI

# 1. Load Secrets
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

# 2. Read latest CSV data
csv_path = "data/sample_data.csv"
df = pd.read_csv(csv_path)
latest_stats = df.tail(1).to_dict(orient="records")[0]

# 3. Generate AI Summary
client = OpenAI(api_key=OPENAI_API_KEY)
prompt = f"Analyze these weekly Instagram metrics and provide a brief executive summary with 3 key action items: {latest_stats}"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
ai_analysis = response.choices[0].message.content

# 4. Compose and Send Email
msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = RECIPIENT_EMAIL
msg['Subject'] = f"Weekly Instagram Analytics Report - {latest_stats['date']}"

body = f"Here is your weekly Instagram performance report:\n\n{ai_analysis}\n\nRaw Metrics:\n{latest_stats}"
msg.attach(MIMEText(body, 'plain'))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

print("Report successfully generated and emailed!")
