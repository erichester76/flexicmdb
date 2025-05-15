from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Entity(Base):
    tablename = "entities"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    attributes = Column(JSON, default={})
    status = Column(String, default="active")

class Relationship(Base):
    tablename = "relationships"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("entities.id"))
    target_id = Column(String, ForeignKey("entities.id"))
    type = Column(String)
