from sqlalchemy import Column, String, ForeignKey
from .entity import Base
import uuid

class IPAddress(Base):
    tablename = "ip_addresses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    address = Column(String, nullable=False, unique=True)
    subnet = Column(String, nullable=False)
    status = Column(String, default="allocated")
    entity_id = Column(String, ForeignKey("entities.id"), nullable=True)
