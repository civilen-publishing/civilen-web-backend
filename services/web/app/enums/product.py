from enum import Enum, unique


@unique
class ProductTypesEnum(Enum):
    BOOK = "BOOK"
    BOOKLET = "BOOKLET"
    CARD = "CARD"

@unique
class ProductStatusEnum(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

@unique
class ProductVendorEnum(Enum):
    AMAZON = "AMAZON"
    SHIPBOB = "SHIPBOB"
