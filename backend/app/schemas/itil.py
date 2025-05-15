from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncidentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "low"
    entity_id: Optional[str] = None
    assignee_id: Optional[str] = None

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[str] = None

class IncidentResponse(IncidentCreate):
    id: str
    status: str

class ChangeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    risk_level: Optional[str] = "low"
    entity_id: Optional[str] = None
    requestor_id: Optional[str] = None
    approver_id: Optional[str] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None

class ChangeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    risk_level: Optional[str] = None
    requestor_id: Optional[str] = None
    approver_id: Optional[str] = None
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None

class ChangeResponse(ChangeCreate):
    id: str
    status: str
