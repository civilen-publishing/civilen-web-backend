import uuid

from pydantic import BaseModel

from .base import AllOptional, JsonModel
from .product import (Product, ProductCreateAPI, ProductCreateCRUD,
                      ProductCreateDB, ProductUpdateAPI, ProductUpdateDB)


# Properties to receive via API on creation
class ShipbobProductCreateAPI(ProductCreateAPI, JsonModel):
    barcode: str
    gtin: str
    upc: str
    referenceId: str
    shipbobId: str

# Properties to receive via API on update
class ShipbobProductUpdateAPI(ProductUpdateAPI, ShipbobProductCreateAPI, metaclass=AllOptional):
    pass
# Properties received by database model on creation
class ShipbobProductCreateDB(ShipbobProductCreateAPI, ProductCreateDB):
    pass


# Properties received by database model on update
class ShipbobProductUpdateDB(ShipbobProductUpdateAPI, ProductUpdateDB):
    pass


# Properties to receive by CRUD service on creation
class ShipbobProductCreateCRUD(ShipbobProductCreateAPI, ProductCreateCRUD):
    images: list[str]


# Properties to receive by CRUD service on update
class ShipbobProductUpdateCRUD(ShipbobProductUpdateAPI):
    images: list[str]


# Properties shared by models stored in DB
class ShipbobProductInDBBase(BaseModel):
    id: uuid.UUID
    barcode: str
    gtin: str
    upc: str
    referenceId: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class ShipbobProduct(ShipbobProductInDBBase, Product):
    pass


# Additional properties stored in DB
class ShipbobProductInDB(ShipbobProductInDBBase):
    shipbobId: str

