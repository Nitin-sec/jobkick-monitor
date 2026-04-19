from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from monitor.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100))
    timestamp = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, nullable=True)
    session_id = Column(String(255), nullable=True)
    service_name = Column(String(100))
    event_metadata = Column(JSON)
    status = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())