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

        ai_metrics = report_data.get("ai_metrics", {})
        user_metrics = report_data.get("user_metrics", {})
        jobs_sent_per_user = user_metrics.get("jobs_sent_per_user", [])

        top_users_lines = []
        for user_data in jobs_sent_per_user[:5]:
            user_id = user_data.get("user_id")
            jobs_sent = user_data.get("jobs_sent", 0)
            top_users_lines.append(f"User {user_id} -> {jobs_sent} jobs")

        top_users_text = "\n".join(top_users_lines) if top_users_lines else "No user job data available."

        body = (
            "=== Jobkick Daily Report ===\n\n"
            f"AI Calls: {ai_metrics.get('total_calls', 0)}\n"
            f"Success: {ai_metrics.get('success_calls', 0)}\n"
            f"Failed: {ai_metrics.get('failed_calls', 0)}\n"
            f"Total Tokens: {ai_metrics.get('total_tokens', 0)}\n"
            f"Total Cost: ${float(ai_metrics.get('total_cost', 0.0)):.6f}\n\n"
            "Top Users:\n"
            f"{top_users_text}\n"
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
