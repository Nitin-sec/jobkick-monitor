from monitor.logger import log_event


def log_user_event(user_id, session_id, service_name, metadata, status="success"):
    log_event("user_event", user_id, session_id, service_name, metadata, status)


def log_system_event(service_name, metadata, status="success"):
    log_event("system_event", None, None, service_name, metadata, status)


def log_job_notification_sent(user_id, service_name="jobkick_monitor", metadata=None, status="success"):
    """
    Canonical event logger for notification metrics.
    """
    log_event(
        "job_notification_sent",
        user_id=user_id,
        session_id=None,
        service_name=service_name,
        event_metadata=metadata or {},
        status=status,
    )