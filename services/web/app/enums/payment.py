from enum import Enum, unique


@unique
class PaymentVendorEnum(Enum):
    STRIPE = "STRIPE"

@unique
class PaymentStatusEnum(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
