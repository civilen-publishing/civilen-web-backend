from app.database.base_class import Base, TimestampMixin, UUIDMixin
from app.enums import PaymentStatusEnum, PaymentVendorEnum
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Payment(Base, UUIDMixin, TimestampMixin):
    __exclude__ = ["order"]  # Exclude these fields from the response (see app/database/base_class.py)

    vendor = Column(Enum(PaymentVendorEnum), nullable=False)
    orderId = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
    paymentDate = Column(DateTime, nullable=True)

    order = relationship("Order", back_populates="payment")
