import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from monitor.config import Config


def send_email_report(report_data):
    sender = Config.EMAIL_USER
    receiver = "rheezon.work@gmail.com"

    if not Config.EMAIL_HOST or not sender or not Config.EMAIL_PASS:
        print("Email report skipped: email configuration is incomplete.")
        return False

    try:
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = "Jobkick Daily Report"

        body = (
            f"Total Events: {report_data.get('total_events', 0)}\n"
            f"AI Requests: {report_data.get('ai_requests', 0)}\n"
            f"Total Tokens: {report_data.get('total_tokens', 0)}\n"
            f"Total Cost: ${float(report_data.get('total_cost', 0.0)):.6f}\n"
        )
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(sender, Config.EMAIL_PASS)
            server.sendmail(sender, receiver, message.as_string())

        return True
    except Exception as e:
        print(f"Email report send error: {e}")
        return False
