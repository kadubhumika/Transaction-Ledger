import os
import requests


def send_email_otp(email: str, otp: str) -> bool:
    """
    Sends a real automated login OTP via Brevo's Web HTTP API.
    Bypasses port blocking restrictions on cloud platforms like Render.
    """
    url = "https://brevo.com"
    api_key = os.getenv("SMTP_PASSWORD")

    if not api_key:
        print("❌ Brevo API Error: SMTP_PASSWORD environment variable is missing!")
        return False

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "RBI Ledger",
            "email": "kadubhumika2468@gmail.com"
        },
        "to": [
            {
                "email": email
            }
        ],
        "subject": "RBI Ledger - Your Secure Login OTP",
        "htmlContent": f"""
            <html>
                <body>
                    <h2>Secure Authentication Verification</h2>
                    <p>Your automated login OTP code is <strong>{otp}</strong>.</p>
                    <p>This code is valid for 5 minutes. Please do not share it with anyone.</p>
                </body>
            </html>
        """
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        # ✅ FIXED: Correct list check syntax for successful API responses
        if response.status_code in [200, 201, 202]:
            print(f"🚀 Automated OTP sent successfully to {email} via Brevo Web API!")
            return True
        else:
            print(f"❌ Brevo API Response Error [{response.status_code}]: {response.text}")
            return False

    except Exception as e:
        print(f"❌ HTTP Email Sync Exception: {str(e)}")
        return False
