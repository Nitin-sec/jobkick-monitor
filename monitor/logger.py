from monitor.db import SessionLocal
from monitor.models import Event

def log_event(event_type, user_id=None, session_id=None, service_name=None, event_metadata=None, status="success"):
    db = SessionLocal()
    try:
        event = Event(
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            service_name=service_name,
            event_metadata=event_metadata,
            status=status
        )
        db.add(event)
        db.commit()
        return event.id
    except Exception as e:
        db.rollback()
        print(f"Logging error: {e}")
        return None
    finally:
        SessionLocal.remove()