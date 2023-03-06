import uuid

from pydantic import BaseModel

from .base import AllOptional


# Properties to receive via API on creation
class OrderItemCreateAPI(BaseModel):
    productId: uuid.UUID
    quantity: int


# Properties to receive via API on update
class OrderItemUpdateAPI(OrderItemCreateAPI, metaclass=AllOptional):
    pass


# Properties to receive by CRUD service on creation
class OrderItemCreateCRUD(OrderItemCreateAPI):
    orderId: uuid.UUID


# Properties to receive by CRUD service on update
class OrderItemUpdateCRUD(OrderItemUpdateAPI):
    pass


# Properties shared by models stored in DB
class OrderItemInDBBase(BaseModel):
    id: uuid.UUID
    productId: uuid.UUID
    quantity: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class OrderItem(OrderItemInDBBase):
    pass


# Additional properties stored in DB
class OrderItemInDB(OrderItemInDBBase):
    orderId: uuid.UUID


# ====================== Additional Schemas ======================

# Properties to Send to amazon
class AmazonOrderItem(BaseModel):
    quantity: int
    price: float
    sellerSku: str
    sellerFulfillmentOrderItemId: str


# Properties to Send to shipbob
class ShipbobOrderItem(BaseModel):
    id: int
    reference_id: str
    quantity: int

    class Config:
        orm_mode = True
        fields = {"reference_id": "referenceId"}
