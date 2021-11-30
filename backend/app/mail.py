import smtplib
from email.message import EmailMessage
import os

SENDER: str = os.getenv('EMAIL_ADDRESS')
PASSWORD: str = os.getenv('EMAIL_PASSWORD')

def send_verification_code(email: str, email_token: int) -> None:
    """Send email with token to user"""
    msg = EmailMessage()
    msg["subject"] = "Flight Booking App: EMAIL VERIFICATION"
    msg['from'] = SENDER
    msg['to'] = email
    msg.set_content(f"Your verification code: {email_token}")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(msg)