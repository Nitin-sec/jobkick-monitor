from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.sql import func
from monitor.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())
    user_id = Column(Integer, nullable=True)
    session_id = Column(String(255), nullable=True)
    service_name = Column(String(100), nullable=True, index=True)
    event_metadata = Column(JSON, nullable=True)
    status = Column(String(50), nullable=False, default="success", server_default="success")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)


class AIUsage(Base):
    __tablename__ = "ai_usage"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    user_id = Column(Integer, nullable=True, index=True)
    api_provider = Column(String(50), nullable=False, index=True)
    model_name = Column(String(150), nullable=False, index=True)
    endpoint = Column(String(100), nullable=False, index=True)
    tokens_input = Column(Integer, nullable=False, default=0, server_default="0")
    tokens_output = Column(Integer, nullable=False, default=0, server_default="0")
    total_tokens = Column(Integer, nullable=False, default=0, server_default="0")
    estimated_cost = Column(Float, nullable=False, default=0.0, server_default="0")
    api_key_hash = Column(String(64), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="success", server_default="success", index=True)
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)