import uuid

from pydantic import BaseModel, EmailStr

from .base import AllOptional


# Properties to receive via API on creation
class AdminCreateAPI(BaseModel):
    name: str
    username: str
    email: EmailStr
    isSuperAdmin: bool


# Properties to receive via API on update
class AdminUpdateAPI(AdminCreateAPI, metaclass=AllOptional):
    pass


# Properties to receive by CRUD service on creation
class AdminCreateCRUD(AdminCreateAPI):
    name: str
    email: EmailStr
    username: str
    password: str


# Properties to receive by CRUD service on update
class AdminUpdateCRUD(AdminUpdateAPI):
    pass


# Properties shared by models stored in DB
class AdminInDBBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Admin(AdminInDBBase):
    pass


# Additional properties stored in DB
class AdminInDB(AdminInDBBase):
    id: uuid.UUID
    email: EmailStr
    username: str
    isSuperAdmin: bool
    password: str


# ====================== Additional Schemas ======================

# Properties to receive via API on Login
class AdminLoginAPIResponse(BaseModel):
    access_token: str
    token_type: str
