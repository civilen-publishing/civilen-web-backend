
from app.database.base_class import Base, UUIDMixin
from sqlalchemy import Boolean, Column, String


class Admin(Base, UUIDMixin):
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    isSuperAdmin = Column(Boolean, default=False)
