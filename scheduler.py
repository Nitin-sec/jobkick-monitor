import time

import schedule

from monitor.services.email_service import send_email_report
from monitor.services.report_service import generate_daily_report


def run_daily_job():
    report_data = generate_daily_report()
    send_email_report(report_data)


def start_scheduler():
    schedule.every().day.at("00:00").do(run_daily_job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()
