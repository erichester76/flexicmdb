from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from .entity import Base
import uuid
from datetime import datetime

class AuditLog(Base):
    tablename = "audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String)
    details = Column(JSON, default={})
    timestamp = Column(DateTime, default=datetime.utcnow)
