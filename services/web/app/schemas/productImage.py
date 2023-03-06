import uuid
from typing import Optional

from pydantic import BaseModel

from .base import AllOptional


# Properties to receive via API on creation
class ProductImageCreateAPI(BaseModel):
    productId: Optional[uuid.UUID] = None
    url: Optional[str] = None


# Properties to receive via API on update
class ProductImageUpdateAPI(ProductImageCreateAPI, metaclass=AllOptional):
    pass


# Properties to receive by CRUD service on creation
class ProductImageCreateCRUD(ProductImageCreateAPI):
    productId: uuid.UUID
    url: str


# Properties to receive by CRUD service on update
class ProductImageUpdateCRUD(ProductImageUpdateAPI):
    pass


# Properties shared by models stored in DB
class ProductImageInDBBase(BaseModel):
    url: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class ProductImage(ProductImageInDBBase):
    pass


# Additional properties stored in DB
class ProductImageInDB(ProductImageInDBBase):
    id: uuid.UUID
    productId: uuid.UUID
