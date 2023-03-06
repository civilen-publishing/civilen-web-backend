
from app.database.base_class import Base, UUIDMixin
from sqlalchemy import Column, String


class Address(Base, UUIDMixin):
    addressLine1 = Column(String, nullable=False)
    addressLine2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    stateOrRegion = Column(String, nullable=False)
    districtOrCounty = Column(String, nullable=False)
    postalCode = Column(String, nullable=False)
    countryCode = Column(String, nullable=False)
