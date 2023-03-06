
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .product import Product


class ShipbobProduct(Product):
    __exclude__ = ["errata", "recommended", "orderItems", "discriminator"]  # Exclude these fields from the response

    id = Column(UUID(as_uuid=True), ForeignKey('product.id'), primary_key=True)
    barcode = Column(String, nullable=False, unique=True)
    gtin = Column(String, nullable=False, unique=True)
    upc = Column(String, nullable=False, unique=True)
    referenceId = Column(String, nullable=False, unique=True)
    shipbobId = Column(String, nullable=False, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "shipbob",
        "inherit_condition": (id == Product.id),
    }