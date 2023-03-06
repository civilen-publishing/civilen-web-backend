import uuid
from typing import Optional

from pydantic import BaseModel

from .amazonProduct import AmazonProduct
from .base import AllOptional
from .shipbobProduct import ShipbobProduct


# Properties to receive via API on creation
class ErrataCreateAPI(BaseModel):
    productId: uuid.UUID
    content: str


# Properties to receive via API on update
class ErrataUpdateAPI(ErrataCreateAPI, metaclass=AllOptional):
    content: Optional[str] = None


# Properties to receive by CRUD service on creation
class ErrataCreateCRUD(ErrataCreateAPI):
    pass


# Properties to receive by CRUD service on update
class ErrataUpdateCRUD(ErrataUpdateAPI):
    pass


# Properties shared by models stored in DB
class ErrataInDBBase(BaseModel):
    id: uuid.UUID
    content: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Errata(ErrataInDBBase):
    product: AmazonProduct | ShipbobProduct


# Additional properties stored in DB
class ErrataInDB(ErrataInDBBase):
    productId: uuid.UUID
