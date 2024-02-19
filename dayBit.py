# created by tyjkot - Feb 18th, 2024
# Daily Bitcoin 9:00 AM Text Message

import os
from dotenv import load_dotenv
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Get gmail credentials
load_dotenv()

# Fetch Bitcoin price (you can use any API)
response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
bitcoin_data = response.json()
bitcoin_price = int(bitcoin_data["bpi"]["USD"]["rate_float"])

# Calculate days until the next halving (April 22, 2024)
halving_date = "2024-04-22"
days_until_halving = (datetime.strptime(halving_date, "%Y-%m-%d") - datetime.now()).days

# Compose the email message
subject = "Bitcoin Update"
message_body = f"Bitcoin ${bitcoin_price}\n{days_until_halving} days till 4th halving"

# Set up Gmail credentials
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
recipient_email = os.getenv("RECIPIENT_EMAIL")

# Create the email
msg = MIMEText(message_body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = recipient_email

# Send the email using Gmail
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")