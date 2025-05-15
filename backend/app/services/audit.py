from sqlalchemy.orm import Session
from ..models.user import AuditLog
from typing import Optional, Dict

def log_audit(
    db: Session,
    user_id: str,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict] = None
    ):
    
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {}
    )

    db.add(audit_log)
    db.commit()
