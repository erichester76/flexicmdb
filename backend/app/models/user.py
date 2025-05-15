from sqlalchemy import Column, String, JSON, ForeignKey, Boolean, DateTime
from .entity import Base
import uuid
from datetime import datetime

class User(Base):
    tablename = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    attributes = Column(JSON, default={})

class Role(Base):
    tablename = "roles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
permissions = Column(JSON, nullable=False)

class UserRole(Base):
    tablename = "user_roles"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    role_id = Column(String, ForeignKey("roles.id"), primary_key=True)

class Approval(Base):
    tablename = "approvals"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    change_id = Column(String, ForeignKey("changes.id"))
    user_id = Column(String, ForeignKey("users.id"))
    status = Column(String, nullable=False)
    comments = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
