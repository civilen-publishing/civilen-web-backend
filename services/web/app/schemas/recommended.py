import uuid

from app.enums import ProductTypesEnum
from pydantic import BaseModel

from .amazonProduct import AmazonProduct
from .base import AllOptional
from .shipbobProduct import ShipbobProduct


# Properties to receive via API on creation
class RecommendedCreateAPI(BaseModel):
    productId: uuid.UUID


# Properties to receive via API on update
class RecommendedUpdateAPI(RecommendedCreateAPI, metaclass=AllOptional):
    pass


# Properties to receive by CRUD service on creation
class RecommendedCreateCRUD(RecommendedCreateAPI):
    productType: ProductTypesEnum


# Properties to receive by CRUD service on update
class RecommendedUpdateCRUD(RecommendedUpdateAPI):
    pass


# Properties shared by models stored in DB
class RecommendedInDBBase(BaseModel):
    id: uuid.UUID

    class Config:
        orm_mode = True


# Additional properties to return via API
class Recommended(RecommendedInDBBase):
    product: AmazonProduct | ShipbobProduct


# Additional properties stored in DB
class RecommendedInDB(RecommendedInDBBase):
    productType: str
