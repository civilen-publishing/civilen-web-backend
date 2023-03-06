import datetime

from app.database.base_class import Base, UUIDMixin
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID


class Errata(Base, UUIDMixin):
    productId = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)