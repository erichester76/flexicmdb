from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies.auth import get_current_user, check_permission
from ..models.ipam import IPAddress
from ..models.user import AuditLog
from ..schemas.ipam import IPAddressCreate, IPAddressUpdate, IPAddressResponse
from ..dependencies import get_db

router = APIRouter()

@router.post("/", response_model=IPAddressResponse)
def create_ip_address(
    ip: IPAddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "ip:write", db)
    if not ip.address.replace(".", "").isdigit():
        raise HTTPException(status_code=400, detail="Invalid IP address")
    db_ip = IPAddress(**ip.dict())
    db.add(db_ip)
    db.commit()
    db.refresh(db_ip)
    db.add(AuditLog(
        user_id=current_user.id,
        action="create_ip_address",
        resource_type="ip_address",
        resource_id=db_ip.id
    ))
    db.commit()
    return db_ip

@router.get("/", response_model=List[IPAddressResponse])
def list_ip_addresses(
    subnet: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "ip:read", db)
    query = db.query(IPAddress)
    if subnet:
       query = query.filter(IPAddress.subnet == subnet)
    if status:
       query = query.filter(IPAddress.status == status)
    ips = query.all()
    db.add(AuditLog(
        user_id=current_user.id,
        action="list_ip_addresses",
        resource_type="ip_address",
        details={"count": len(ips)}
    ))
    db.commit()
    return ips

@router.get("/{ip_id}", response_model=IPAddressResponse)
def get_ip_address(
    ip_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "ip:read", db)
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
    if not ip:
        raise HTTPException(status_code=404, detail="IP address not found")
    db.add(AuditLog(
        user_id=current_user.id,
        action="get_ip_address",
        resource_type="ip_address",
        resource_id=ip_id
    ))
    db.commit()
    return ip

@router.patch("/{ip_id}", response_model=IPAddressResponse)
def update_ip_address(
    ip_id: str,
    update: IPAddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "ip:write", db)
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
    if not ip:
        raise HTTPException(status_code=404, detail="IP address not found")
    for key, value in update.dict(exclude_unset=True).items():
        if key == "address" and value.replace(".", "").isdigit():
            setattr(ip, key, value)
        elif key != "address":
            setattr(ip, key, value)
        db.commit()
        db.refresh(ip)
        db.add(AuditLog(
            user_id=current_user.id,
            action="update_ip_address",
            resource_type="ip_address",
            resource_id=ip_id,
            details=update.dict(exclude_unset=True)
        ))
    db.commit()
    return ip

@router.delete("/{ip_id}")
def delete_ip_address(
    ip_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "ip:delete", db)
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
    if not ip:
        raise HTTPException(status_code=404, detail="IP address not found")
    db.delete(ip)
    db.commit()
    db.add(AuditLog(
        user_id=current_user.id,
        action="delete_ip_address",
        resource_type="ip_address",
        resource_id=ip_id
    ))
    db.commit()
    return {"status": "deleted"}
