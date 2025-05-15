from pydantic import BaseModel
from typing import Optional

class IPAddressCreate(BaseModel):
    address: str
    subnet: str
    entity_id: Optional[str] = None
    status: Optional[str] = "allocated"

class IPAddressUpdate(BaseModel):
    address: Optional[str] = None
    subnet: Optional[str] = None
    status: Optional[str] = None
    entity_id: Optional[str] = None

class IPAddressResponse(IPAddressCreate):
    id: str
