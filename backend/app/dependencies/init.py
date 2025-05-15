from .auth import get_current_user, check_permission
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()
