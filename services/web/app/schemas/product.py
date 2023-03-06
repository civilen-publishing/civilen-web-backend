import uuid
from typing import Optional

from app.enums import ProductStatusEnum, ProductTypesEnum, ProductVendorEnum
from pydantic import BaseModel, Extra

from .base import AllOptional, JsonModel
from .productImage import ProductImage


# Properties to receive via API on creation
class ProductCreateAPI(JsonModel):
    title: str
    description: str
    price: float
    type: ProductTypesEnum
    sku: str
    isbn: str
    keyProductFeatures: str
    printLength: int


# Properties to receive via API on update
class ProductUpdateAPI(ProductCreateAPI, metaclass=AllOptional):
    status: Optional[ProductStatusEnum] = None
    images: Optional[list[ProductImage]] = None


# Properties received by database model on creation
class ProductCreateDB(ProductCreateAPI):
    status: Optional[ProductStatusEnum] = ProductStatusEnum.ACTIVE
    vendor: ProductVendorEnum
    images: list[str] = []


# Properties received by database model on update
class ProductUpdateDB(ProductUpdateAPI):
    pass


# Properties to receive by CRUD service on creation
class ProductCreateCRUD(ProductCreateAPI):
    status: Optional[ProductStatusEnum] = ProductStatusEnum.ACTIVE
    vendor: ProductVendorEnum
    images: list[str] = []


# Properties to receive by CRUD service on update
class ProductUpdateCRUD(ProductUpdateAPI):
    pass


# Properties shared by models stored in DB
class ProductInDBBase(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: float
    type: ProductTypesEnum
    status: ProductStatusEnum
    vendor: ProductVendorEnum
    sku: str
    isbn: str
    keyProductFeatures: str
    printLength: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Product(ProductInDBBase):
    images: list[ProductImage]


class OrderProduct(ProductInDBBase):
    images: list[ProductImage]
    quantity: int
    sku: str

    class Config:
        extra = Extra.allow


# Additional properties stored in DB
class ProductInDB(ProductInDBBase):
    pass
