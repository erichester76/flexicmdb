from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies.auth import get_current_user, check_permission
from ..models.itil import Incident, Change
from ..models.user import AuditLog
from ..schemas.itil import IncidentCreate, IncidentUpdate, IncidentResponse, ChangeCreate, ChangeUpdate, ChangeResponse
from ..dependencies import get_db

router = APIRouter()

@router.post("/incidents/", response_model=IncidentResponse)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "incident:write", db)
    db_incident = Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    db.add(AuditLog(
        user_id=current_user.id,
        action="create_incident",
        resource_type="incident",
        resource_id=db_incident.id
    ))
    db.commit()
    return db_incident

@router.get("/incidents/", response_model=List[IncidentResponse])
def list_incidents(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "incident:read", db)
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    if priority:
        query = query.filter(Incident.priority == priority)
    incidents = query.all()
    db.add(AuditLog(
        user_id=current_user.id,
        action="list_incidents",
        resource_type="incident",
        details={"count": len(incidents)}
    ))
    db.commit()
    return incidents
