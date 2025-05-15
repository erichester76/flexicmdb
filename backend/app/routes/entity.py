from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies.auth import get_current_user, check_permission
from ..models.entity import Entity
from ..models.user import AuditLog
from ..schemas.entity import EntityCreate, EntityUpdate, EntityResponse
from ..dependencies import get_db

router = APIRouter()

@router.post("/", response_model=EntityResponse)
def create_entity(
    entity: EntityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "cmdb:write", db)
    db_entity = Entity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    db.add(AuditLog(
        user_id=current_user.id,
        action="create_entity",
        resource_type="entity",
        resource_id=db_entity.id
    ))
    db.commit()
    return db_entity

@router.get("/", response_model=List[EntityResponse])
def list_entities(
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "cmdb:read", db)
   
    query = db.query(Entity)
    if type:
        query = query.filter(Entity.type == type)
    if status:
        query = query.filter(Entity.status == status)
   
    entities = query.all()
    db.add(AuditLog(
        user_id=current_user.id,
        action="list_entities",
        resource_type="entity",
        details={"count": len(entities)}
    ))
    db.commit()
    return entities

@router.get("/{entity_id}", response_model=EntityResponse)
def get_entity(
    entity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "cmdb:read", db)
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    db.add(AuditLog(
        user_id=current_user.id,
        action="get_entity",
        resource_type="entity",
        resource_id=entity_id
    ))
    db.commit()
    return entity

@router.patch("/{entity_id}", response_model=EntityResponse)
def update_entity(
    entity_id: str,
    update: EntityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "cmdb:write", db)
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(entity, key, value)
        db.commit()
        db.refresh(entity)
        db.add(AuditLog(
            user_id=current_user.id,
            action="update_entity",
            resource_type="entity",
            resource_id=entity_id,
            details=update.dict(exclude_unset=True)
        ))
    db.commit()
    return entity

@router.delete("/{entity_id}")
def delete_entity(
    entity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    check_permission(current_user, "cmdb:delete", db)
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    db.delete(entity)
    db.commit()
    db.add(AuditLog(
        user_id=current_user.id,
        action="delete_entity",
        resource_type="entity",
        resource_id=entity_id
    ))
    db.commit()
    return {"status": "deleted"}
