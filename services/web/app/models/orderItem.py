from app.database.base_class import Base, UUIDMixin
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class OrderItem(Base, UUIDMixin):
    productId = Column(UUID(as_uuid=True), ForeignKey("product.id"))
    orderId = Column(UUID(as_uuid=True), ForeignKey("order.id"))
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="orderItems")
