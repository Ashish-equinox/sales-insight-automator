import smtplib
from email.mime.text import MIMEText

EMAIL = "ashishequinox007@gmail.com"
APP_PASSWORD = "rivjuqfxnmwzcsnd"

def send_email(to_email, summary):

    msg = MIMEText(summary)
    msg["Subject"] = "AI Sales Summary"
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())