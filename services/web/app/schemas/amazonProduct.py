import uuid

from pydantic import BaseModel

from .base import AllOptional, JsonModel
from .product import (Product, ProductCreateAPI, ProductCreateCRUD,
                      ProductCreateDB, ProductUpdateAPI, ProductUpdateDB)


# Properties to receive via API on creation
class AmazonProductCreateAPI(ProductCreateAPI, JsonModel):
    asin: str
    displayableOrderComment: str


# Properties to receive via API on update
class AmazonProductUpdateAPI(ProductUpdateAPI, AmazonProductCreateAPI, metaclass=AllOptional):
    pass


# Properties received by database model on creation
class AmazonProductCreateDB(AmazonProductCreateAPI, ProductCreateDB):
    pass


# Properties received by database model on update
class AmazonProductUpdateDB(AmazonProductUpdateAPI, ProductUpdateDB):
    pass


# Properties to receive by CRUD service on creation
class AmazonProductCreateCRUD(AmazonProductCreateAPI, ProductCreateCRUD):
    images: list[str]


# Properties to receive by CRUD service on update
class AmazonProductUpdateCRUD(AmazonProductUpdateAPI):
    images: list[str]


# Properties shared by models stored in DB
class AmazonProductInDBBase(BaseModel):
    id: uuid.UUID
    asin: str
    displayableOrderComment: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class AmazonProduct(AmazonProductInDBBase, Product):
    pass


# Additional properties stored in DB
class AmazonProductInDB(AmazonProductInDBBase):
    pass
