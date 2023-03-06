from app.database.base_class import Base, UUIDMixin
from app.enums import OrderStatusEnum, ShippingSpeedEnum
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Order(Base, UUIDMixin):
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    addressId = Column(UUID(as_uuid=True), ForeignKey("address.id"))
    phone = Column(String, nullable=False)
    status = Column(
        Enum(OrderStatusEnum, name="status", create_type=False),
        nullable=False,
        default=OrderStatusEnum.WAITING_FOR_CONFIRMATION,
    )
    shippingSpeedCategory = Column(
        Enum(ShippingSpeedEnum, name="shippingSpeedCategory", create_type=False),
        nullable=False,
        default=ShippingSpeedEnum.STANDARD,
    )
    orderItems = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order")
