from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    attributes: Optional[Dict] = {}

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    attributes: Optional[Dict] = None

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    attributes: Dict

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[str]

class RoleResponse(RoleCreate):
    id: str

class ApprovalCreate(BaseModel):
    change_id: str
    user_id: str
    status: str
    comments: Optional[str] = None

class ApprovalUpdate(BaseModel):
    status: Optional[str] = None
    comments: Optional[str] = None

class ApprovalResponse(ApprovalCreate):
    id: str
    created_at: datetime
