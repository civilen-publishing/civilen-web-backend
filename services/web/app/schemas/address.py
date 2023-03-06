import uuid
from typing import Optional

from pydantic import BaseModel

from .base import AllOptional


# Properties to receive via API on creation
class AddressCreateAPI(BaseModel):
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    stateOrRegion: str
    districtOrCounty: str
    postalCode: str
    countryCode: str


# Properties to receive via API on update
class AddressUpdateAPI(AddressCreateAPI, metaclass=AllOptional):
    pass


# Properties to receive by CRUD service on creation
class AddressCreateCRUD(AddressCreateAPI):
    pass


# Properties to receive by CRUD service on update
class AddressUpdateCRUD(AddressUpdateAPI):
    pass


# Properties shared by models stored in DB
class AddressInDBBase(BaseModel):
    addressLine1: str
    addressLine2: str
    city: str
    stateOrRegion: str
    districtOrCounty: str
    postalCode: str
    countryCode: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Address(AddressInDBBase):
    pass


# Additional properties stored in DB
class AddressInDB(AddressInDBBase):
    id: uuid.UUID
