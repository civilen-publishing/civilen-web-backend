from app.database.base_class import Base, UUIDMixin
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ProductImage(Base, UUIDMixin):
    url = Column(String, nullable=False)
    productId = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    product = relationship("Product", back_populates="images")
