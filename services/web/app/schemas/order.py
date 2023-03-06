import uuid
from typing import Optional

from app.enums import OrderStatusEnum, ShippingSpeedEnum
from pydantic import BaseModel, EmailStr

from .address import Address
from .base import AllOptional
from .orderItem import OrderItem, OrderItemCreateAPI


# Properties to receive via API on creation
class OrderCreateAPI(BaseModel):
    name: str
    email: EmailStr
    address: Address
    phone: str
    orderItems: list[OrderItemCreateAPI]


# Properties to receive via API on update
class OrderUpdateAPI(OrderCreateAPI, metaclass=AllOptional):
    shippingSpeedCategory: Optional[ShippingSpeedEnum] = None


# Properties received by database model on creation
class OrderCreateDB(BaseModel):
    name: str
    email: EmailStr
    phone: str
    status: OrderStatusEnum
    shippingSpeedCategory: ShippingSpeedEnum
    addressId: uuid.UUID


# Properties received by database model on update
class OrderUpdateDB(OrderUpdateAPI):
    pass


# Properties to receive by CRUD service on creation
class OrderCreateCRUD(OrderCreateAPI):
    status: OrderStatusEnum
    shippingSpeedCategory: ShippingSpeedEnum
    address: Optional[Address] = None


# Properties to receive by CRUD service on update
class OrderUpdateCRUD(OrderUpdateAPI):
    pass


# Properties shared by models stored in DB
class OrderInDBBase(BaseModel):
    id: uuid.UUID
    status: OrderStatusEnum
    shippingSpeedCategory: ShippingSpeedEnum
    addressId: uuid.UUID
    name: str
    email: EmailStr
    phone: str
    orderItems: list[OrderItem]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Order(OrderInDBBase):
    address: Address


# Additional properties stored in DB
class OrderInDB(OrderInDBBase):
    pass


class ConfirmOrder(BaseModel):
    shippingSpeedCategory: str
