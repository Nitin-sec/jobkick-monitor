from monitor.logger import log_event

def log_user_event(user_id, session_id, service_name, metadata, status="success"):
    log_event("user_event", user_id, session_id, service_name, metadata, status)

def log_system_event(service_name, metadata, status="success"):
    log_event("system_event", None, None, service_name, metadata, status)