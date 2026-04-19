from flask import Flask, jsonify
from monitor.db import SessionLocal
from monitor.models import Event

app = Flask(__name__)

@app.route("/health")
def health():
    return "OK"

@app.route("/events")
def get_events():
    db = SessionLocal()
    try:
        events = db.query(Event).order_by(Event.created_at.desc()).limit(50).all()
        return jsonify([
            {
                "id": e.id,
                "event_type": e.event_type,
                "user_id": e.user_id,
                "session_id": e.session_id,
                "service_name": e.service_name,
                "event_metadata": e.event_metadata,
                "status": e.status,
                "created_at": str(e.created_at)
            }
            for e in events
        ])
    finally:
        db.close()