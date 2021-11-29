import smtplib
from email.message import EmailMessage
import os

SENDER: str = os.getenv('EMAIL_ADDRESS')
PASSWORD: str = os.getenv('EMAIL_PASSWORD')

def send_token(email: str, email_token: str) -> None:
    """Send email with token to user"""
    msg = EmailMessage()
    msg["subject"] = "EMAIL VERIFICATION"
    msg['from'] = SENDER
    msg['to'] = email
    msg.set_content(email_token)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)