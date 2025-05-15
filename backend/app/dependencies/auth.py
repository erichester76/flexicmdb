from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..models.user import User, Role, UserRole
from ..dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

Placeholder: Replace with real JWT decoding (e.g., fastapi-users)
user = db.query(User).filter(User.email == "placeholder@example.com").first()
if not user or not user.is_active:
raise HTTPException(status_code=401, detail="Invalid or inactive user")
return user

def check_permission(user: User, permission: str, db: Session):
roles = db.query(Role).join(UserRole).filter(UserRole.user_id == user.id).all()
for role in roles:
if permission in role.permissions:
return True
raise HTTPException(status_code=403, detail="Insufficient permissions")
