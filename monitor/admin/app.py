from flask import Flask, jsonify, request
from monitor.db import SessionLocal
from monitor.models import Event, AIUsage
from monitor.services.ai_service import track_ai_success, track_ai_failure

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/events")
def get_events():
    db = SessionLocal()
    try:
        events = db.query(Event).order_by(Event.created_at.desc()).limit(50).all()
        return jsonify([
            {
                "id": e.id,
                "event_type": e.event_type,
                "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                "user_id": e.user_id,
                "session_id": e.session_id,
                "service_name": e.service_name,
                "event_metadata": e.event_metadata,
                "status": e.status,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in events
        ])
    except Exception as e:
        return jsonify({"error": "failed_to_fetch_events", "detail": str(e)}), 500
    finally:
        SessionLocal.remove()


@app.route("/ai-usage", methods=["POST"])
def create_ai_usage():
    payload = request.get_json(silent=True) or {}

    user_id = payload.get("user_id")
    api_provider = payload.get("api_provider")
    model_name = payload.get("model_name")
    endpoint = payload.get("endpoint")
    tokens_input = payload.get("tokens_input", 0)
    tokens_output = payload.get("tokens_output", 0)
    estimated_cost = payload.get("estimated_cost", 0.0)
    api_key = payload.get("api_key", "")
    status = payload.get("status", "success")
    error_message = payload.get("error_message")

    if not api_provider or not model_name or not endpoint:
        return jsonify({"error": "api_provider, model_name, and endpoint are required"}), 400

    if status == "failure":
        usage_id = track_ai_failure(
            user_id=user_id,
            api_provider=api_provider,
            model_name=model_name,
            endpoint=endpoint,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            estimated_cost=estimated_cost,
            api_key=api_key,
            error_message=error_message or "unknown_error",
        )
    else:
        usage_id = track_ai_success(
            user_id=user_id,
            api_provider=api_provider,
            model_name=model_name,
            endpoint=endpoint,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            estimated_cost=estimated_cost,
            api_key=api_key,
        )

    if usage_id is None:
        return jsonify({"error": "failed_to_log_ai_usage"}), 500

    return jsonify({"status": "success", "id": usage_id}), 201


@app.route("/ai-usage", methods=["GET"])
def get_ai_usage():
    db = SessionLocal()
    try:
        usage_records = db.query(AIUsage).order_by(AIUsage.created_at.desc()).limit(50).all()
        return jsonify([
            {
                "id": u.id,
                "timestamp": u.timestamp.isoformat() if u.timestamp else None,
                "user_id": u.user_id,
                "api_provider": u.api_provider,
                "model_name": u.model_name,
                "endpoint": u.endpoint,
                "tokens_input": u.tokens_input,
                "tokens_output": u.tokens_output,
                "total_tokens": u.total_tokens,
                "estimated_cost": u.estimated_cost,
                "api_key_hash": u.api_key_hash,
                "status": u.status,
                "error_message": u.error_message,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in usage_records
        ])
    except Exception as e:
        return jsonify({"error": "failed_to_fetch_ai_usage", "detail": str(e)}), 500
    finally:
        SessionLocal.remove()