from monitor.services.metrics_service import get_dashboard_metrics


def generate_daily_report():
    return get_dashboard_metrics()
