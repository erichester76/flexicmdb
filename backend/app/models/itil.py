from sqlalchemy import Column, String, ForeignKey, DateTime
from .entity import Base
import uuid
from datetime import datetime

class Incident(Base):
    tablename = "incidents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="open")
    priority = Column(String, default="low")
    entity_id = Column(String, ForeignKey("entities.id"), nullable=True)
    assignee_id = Column(String, ForeignKey("users.id"), nullable=True)

class Change(Base):
    tablename = "changes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="requested")
    risk_level = Column(String, default="low")
    entity_id = Column(String, ForeignKey("entities.id"), nullable=True)
    requestor_id = Column(String, ForeignKey("users.id"), nullable=True)
    approver_id = Column(String, ForeignKey("users.id"), nullable=True)
    planned_start = Column(DateTime)
    planned_end = Column(DateTime)
