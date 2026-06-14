import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_otp(email: str, otp: str) -> bool:
    """
    Sends a real automated login OTP via the standard smtplib module using Brevo SMTP.
    """
    # Create the email container
    msg = MIMEMultipart()
    msg["Subject"] = "RBI Ledger - Your Secure Login OTP"

    # ✅ FIX: Hardcode your real verified sender email here instead of os.getenv("SMTP_USER")
    msg["From"] = "kadubhumika2468@gmail.com"
    msg["To"] = email

    # Email body content
    body = f"Your automated login OTP code is {otp}. This code is valid for 5 minutes."
    msg.attach(MIMEText(body, "plain"))

    try:
        # Establish connection using your .env variables
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT", 587)))
        server.starttls()  # Secure the connection

        # Authenticate using Brevo SMTP account credentials
        server.login(
            os.getenv("SMTP_USER"),
            os.getenv("SMTP_PASSWORD")
        )

        # Send the payload using the real email address header
        server.sendmail(msg["From"], email, msg.as_string())
        server.quit()

        print(f"🚀 Automated OTP sent successfully to {email} via smtplib!")
        return True

    except Exception as e:
        print(f"❌ smtplib Automation Error: {str(e)}")
        return False
