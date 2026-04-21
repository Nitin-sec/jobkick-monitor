from datetime import datetime, timedelta

from sqlalchemy import func

from monitor.db import SessionLocal
from monitor.models import Event, AIUsage


def generate_daily_report():
    db = SessionLocal()
    try:
        since = datetime.utcnow() - timedelta(hours=24)

        total_events = (
            db.query(func.count(Event.id))
            .filter(Event.created_at >= since)
            .scalar()
            or 0
        )

        ai_aggregate = (
            db.query(
                func.count(AIUsage.id),
                func.coalesce(func.sum(AIUsage.total_tokens), 0),
                func.coalesce(func.sum(AIUsage.estimated_cost), 0.0),
            )
            .filter(AIUsage.created_at >= since)
            .first()
        )

        ai_requests = int(ai_aggregate[0] or 0)
        total_tokens = int(ai_aggregate[1] or 0)
        total_cost = float(ai_aggregate[2] or 0.0)

        return {
            "total_events": int(total_events),
            "ai_requests": ai_requests,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
        }
    except Exception as e:
        print(f"Daily report generation error: {e}")
        return {
            "total_events": 0,
            "ai_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
        }
    finally:
        SessionLocal.remove()
