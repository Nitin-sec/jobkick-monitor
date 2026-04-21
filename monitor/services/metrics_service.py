from sqlalchemy import func

from monitor.db import SessionLocal
from monitor.models import AIUsage, Event


def get_dashboard_metrics():
    db = SessionLocal()
    try:
        total_ai_calls = int(db.query(func.count(AIUsage.id)).scalar() or 0)
        total_success_calls = int(
            db.query(func.count(AIUsage.id))
            .filter(AIUsage.status == "success")
            .scalar()
            or 0
        )
        total_failed_calls = int(
            db.query(func.count(AIUsage.id))
            .filter(AIUsage.status != "success")
            .scalar()
            or 0
        )
        total_tokens = int(
            db.query(func.coalesce(func.sum(AIUsage.total_tokens), 0)).scalar() or 0
        )
        total_cost = float(
            db.query(func.coalesce(func.sum(AIUsage.estimated_cost), 0.0)).scalar() or 0.0
        )
        total_events = int(db.query(func.count(Event.id)).scalar() or 0)

        jobs_per_user_rows = (
            db.query(Event.user_id, func.count(Event.id).label("jobs_sent"))
            .filter(Event.user_id.isnot(None))
            .filter(Event.event_type == "job_notification_sent")
            .group_by(Event.user_id)
            .order_by(func.count(Event.id).desc())
            .all()
        )

        jobs_sent_per_user = [
            {"user_id": int(row.user_id), "jobs_sent": int(row.jobs_sent)}
            for row in jobs_per_user_rows
        ]

        # Temporary debug logs for validating metrics in runtime.
        print("AI calls:", total_ai_calls)
        print("AI success calls:", total_success_calls)
        print("AI failed calls:", total_failed_calls)
        print("AI total tokens:", total_tokens)
        print("AI total cost:", total_cost)
        print("Total events:", total_events)
        print("Jobs sent per user:", jobs_sent_per_user)

        return {
            "ai_metrics": {
                "total_calls": total_ai_calls,
                "success_calls": total_success_calls,
                "failed_calls": total_failed_calls,
                "total_tokens": total_tokens,
                "total_cost": total_cost,
            },
            "user_metrics": {
                "jobs_sent_per_user": jobs_sent_per_user,
            },
            "system_metrics": {
                "total_events": total_events,
            },
        }
    except Exception as e:
        print(f"Dashboard metrics generation error: {e}")
        return {
            "ai_metrics": {
                "total_calls": 0,
                "success_calls": 0,
                "failed_calls": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
            },
            "user_metrics": {
                "jobs_sent_per_user": [],
            },
            "system_metrics": {
                "total_events": 0,
            },
        }
    finally:
        SessionLocal.remove()
