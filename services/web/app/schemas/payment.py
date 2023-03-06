import datetime
import uuid
from typing import Optional

from app.enums import PaymentStatusEnum, PaymentVendorEnum
from pydantic import BaseModel

from .base import AllOptional


# Properties to receive via API on creation
class PaymentCreateAPI(BaseModel):
    vendor: PaymentVendorEnum
    total: float
    orderId: uuid.UUID


# Properties to receive via API on update
class PaymentUpdateAPI(PaymentCreateAPI, metaclass=AllOptional):
    status: Optional[PaymentStatusEnum] = PaymentStatusEnum.PENDING
    paymentDate: Optional[datetime.datetime] = None


# Properties to receive by CRUD service on creation
class PaymentCreateCRUD(PaymentCreateAPI):
    pass


# Properties to receive by CRUD service on update
class PaymentUpdateCRUD(PaymentUpdateAPI):
    pass


# Properties shared by models stored in DB
class PaymentInDBBase(BaseModel):
    id: uuid.UUID
    vendor: PaymentVendorEnum
    orderId: uuid.UUID
    total: float
    status: PaymentStatusEnum
    paymentDate: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Payment(PaymentInDBBase):
    pass


# Additional properties stored in DB
class PaymentInDB(PaymentInDBBase):
    pass
