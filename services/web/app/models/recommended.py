from app.database.base_class import Base, UUIDMixin
from sqlalchemy import Column
from sqlalchemy import Enum as pgEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .product import ProductTypesEnum


class Recommended(Base, UUIDMixin):
    productId = Column(UUID(as_uuid=True), ForeignKey('product.id'), unique=True)
    productType = Column(pgEnum(ProductTypesEnum, name="productType"), nullable=False)