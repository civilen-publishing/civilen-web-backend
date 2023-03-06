from app.database.base_class import Base, UUIDMixin
from sqlalchemy import Column, String


class Slide(Base, UUIDMixin):
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    imageUrl = Column(String, nullable=False)
