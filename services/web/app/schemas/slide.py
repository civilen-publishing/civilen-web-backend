import uuid
from typing import Optional

from pydantic import BaseModel

from .base import AllOptional, JsonModel


# Properties to receive via API on creation
class SlideCreateAPI(JsonModel):
    title: str
    description: str


# Properties to receive via API on update
class SlideUpdateAPI(SlideCreateAPI, metaclass=AllOptional):
    imageUrl: Optional[str] = None


# Properties to receive by CRUD service on creation
class SlideCreateCRUD(SlideCreateAPI):
    imageUrl: str


# Properties to receive by CRUD service on update
class SlideUpdateCRUD(SlideUpdateAPI):
    pass


# Properties shared by models stored in DB
class SlideInDBBase(BaseModel):
    id: uuid.UUID
    imageUrl: str
    title: str
    description: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Slide(SlideInDBBase):
    pass


# Additional properties stored in DB
class SlideInDB(SlideInDBBase):
    pass
