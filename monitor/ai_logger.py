import hashlib

from monitor.db import SessionLocal
from monitor.models import AIUsage


def log_ai_usage(
    user_id=None,
    api_provider=None,
    model_name=None,
    endpoint=None,
    tokens_input=0,
    tokens_output=0,
    estimated_cost=0.0,
    api_key="",
    status="success",
    error_message=None,
):
    db = SessionLocal()
    try:
        safe_tokens_input = int(tokens_input or 0)
        safe_tokens_output = int(tokens_output or 0)
        total_tokens = safe_tokens_input + safe_tokens_output
        safe_estimated_cost = float(estimated_cost or 0.0)
        safe_api_key = str(api_key or "")
        api_key_hash = hashlib.sha256(safe_api_key.encode("utf-8")).hexdigest()

        usage = AIUsage(
            user_id=user_id,
            api_provider=str(api_provider or ""),
            model_name=str(model_name or ""),
            endpoint=str(endpoint or ""),
            tokens_input=safe_tokens_input,
            tokens_output=safe_tokens_output,
            total_tokens=total_tokens,
            estimated_cost=safe_estimated_cost,
            api_key_hash=api_key_hash,
            status=str(status or "success"),
            error_message=error_message,
        )
        db.add(usage)
        db.commit()
        return usage.id
    except Exception as e:
        db.rollback()
        print(f"AI usage logging error: {e}")
        return None
    finally:
        SessionLocal.remove()
