from app.database.base_class import Base, InheritanceMixin, UUIDMixin
from app.enums import ProductStatusEnum, ProductTypesEnum, ProductVendorEnum
from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.orm import relationship


# This is the Product table that all other tables will reference (Polymorphic)
class Product(Base, UUIDMixin, InheritanceMixin):
    __exclude__ = ["errata", "recommended", "orderItems", "discriminator"]  # Exclude these fields from the response

    title = Column(String, nullable=False)  # might be referenced as name
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)  # might be referenced as unitPrice
    type = Column(Enum(ProductTypesEnum), nullable=False)
    status = Column(Enum(ProductStatusEnum), nullable=False, default=ProductStatusEnum.ACTIVE)
    vendor = Column(Enum(ProductVendorEnum), nullable=False)
    sku = Column(String, nullable=False, unique=True)
    isbn = Column(String, nullable=False, unique=True)
    keyProductFeatures = Column(String, nullable=False)
    printLength = Column(Integer, nullable=False)

    images = relationship("ProductImage", cascade="all, delete-orphan")
    recommended = relationship("Recommended", cascade="all, delete-orphan", uselist=False)  # One to One
    errata = relationship("Errata", cascade="all, delete-orphan", uselist=False)  # One to One
    orderItems = relationship("OrderItem", cascade="all, delete-orphan")
