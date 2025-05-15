from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class EntityCreate(BaseModel):
    type: str
    name: str
    attributes: Optional[Dict] = {}
    status: Optional[str] = "active"

class EntityUpdate(BaseModel):
    name: Optional[str] = None
    attributes: Optional[Dict] = None
    status: Optional[str] = None

class EntityResponse(EntityCreate):
    id: str
