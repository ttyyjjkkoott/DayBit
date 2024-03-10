# Author: tyjkot
# Created: Feb 18th, 2024
# Updated: Mar 9th, 2024
# Daily Bitcoin 9:00 AM Text Message

import os
import requests
import smtplib
from email.message import EmailMessage
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Constants
BITCOIN_API_URL = "https://blockchain.info/q/getblockcount"
BLOCK_REWARD_HALVING_INTERVAL = 210000
SECONDS_IN_A_DAY = 86400
AVERAGE_BLOCKS_PER_DAY = 144

def get_current_block_height():
    response = requests.get(BITCOIN_API_URL)
    return int(response.text)

def get_reward_halving_timestamp(current_block_height):
    blocks_to_halving = BLOCK_REWARD_HALVING_INTERVAL - (current_block_height % BLOCK_REWARD_HALVING_INTERVAL)
    blocks_to_halving_seconds = blocks_to_halving * SECONDS_IN_A_DAY
    return int(time.time()) + blocks_to_halving_seconds

def get_bitcoin_price():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    return response.json()['bpi']['USD']['rate_float']

def compose_email(bitcoin_price, days_left, blocks_left):
    subject = "Bitcoin Update"
    message_body = f"Bitcoin ${bitcoin_price:.2f}\n{blocks_left} blocks left\n{days_left:.2f} days till 4th halving"
    return subject, message_body

def send_email(subject, message_body):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(message_body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Text sent successfully!")
    except Exception as e:
        print(f"Error sending text: {e}")

def main():
    current_block_height = get_current_block_height()
    halving_timestamp = get_reward_halving_timestamp(current_block_height)
    blocks_left = BLOCK_REWARD_HALVING_INTERVAL - (current_block_height % BLOCK_REWARD_HALVING_INTERVAL)
    days_left = blocks_left / AVERAGE_BLOCKS_PER_DAY
    bitcoin_price = get_bitcoin_price()

    subject, message_body = compose_email(bitcoin_price, days_left, blocks_left)
    send_email(subject, message_body)

if __name__ == "__main__":
    main()
