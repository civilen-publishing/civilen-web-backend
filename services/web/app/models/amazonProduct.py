from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .product import Product


class AmazonProduct(Product):
    __exclude__ = ["errata", "recommended", "orderItems", "discriminator"]  # Exclude these fields from the response

    id = Column(UUID(as_uuid=True), ForeignKey("product.id"), primary_key=True)
    asin = Column(String, nullable=False, unique=True)
    displayableOrderComment = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "amazon",
        "inherit_condition": (id == Product.id),
    }
