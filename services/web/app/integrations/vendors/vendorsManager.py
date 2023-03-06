from typing import Any, Protocol, runtime_checkable

from app import schemas
from app.core.config import get_settings
from app.enums import ProductVendorEnum
from pydantic import BaseModel

from .amazon import AmazonIntegration
from .shipbob import ShipBobIntegration

amazon_credentials = dict(
    refresh_token=get_settings().SP_API_REFRESH_TOKEN,
    lwa_app_id=get_settings().SP_API_LWA_APP_ID,
    lwa_client_secret=get_settings().SP_API_LWA_CLIENT_SECRET,
    aws_secret_key=get_settings().SP_API_AWS_SECRET_KEY,
    aws_access_key=get_settings().SP_API_AWS_ACCESS_KEY,
    role_arn=get_settings().SP_API_ROLE_ARN,
)


@runtime_checkable
class VendorInterface(Protocol):
    def create_fulfillment_order(self, payload):
        ...

    def get_fulfillment_status(
        self,
        order: schemas.Order,
        items: list[schemas.AmazonOrderItem | schemas.ShipbobOrderItem],
        address: schemas.Address,
        shippingSpreedCategory: str = "",
    ):
        ...

    def get_fulfillment_order_payload(
        order: schemas.Order,
        items: list[schemas.OrderProduct],
        address: schemas.Address,
    ) -> dict:
        ...


class VendorData(BaseModel):
    controller: VendorInterface

    class Config:
        arbitrary_types_allowed = True


class FulfillmentStatusResult(BaseModel):
    shippingSpeedCategories: list[str]
    unfulfillablePreviewItems: list[Any]


class VendorsManager:
    def __init__(self):
        self.vendors: dict[ProductVendorEnum, VendorData] = {
            ProductVendorEnum.AMAZON: VendorData(
                **{"controller": AmazonIntegration(amazon_credentials, get_settings().SP_API_SELLER_ID)}
            ),
            ProductVendorEnum.SHIPBOB: VendorData(
                **{"controller": ShipBobIntegration(get_settings().SHIPBOB_API_TOKEN)}
            ),
        }

    def get_order_fulfillment_payload(self, order, items, address):
        result: dict[ProductVendorEnum, dict] = {}
        for vendorName in self.vendors:
            vendorItems = list(filter(lambda item: item.vendor == vendorName, items))
            if not vendorItems:
                continue
            result[vendorName] = self.vendors[vendorName].controller.get_fulfillment_order_payload(
                order, vendorItems, address
            )
        return result

    def get_order_fulfillment_status(self, order, items, address) -> FulfillmentStatusResult:
        result = {"shippingSpeedCategories": [], "unfulfillablePreviewItems": []}
        for vendorName in self.vendors:
            vendorItems = list(filter(lambda item: item.vendor == vendorName, items))
            if not vendorItems:
                continue
            order.id = str(order.id)
            order.addressId = str(order.addressId)
            for item in vendorItems:
                item.id = str(item.id)
            vendorResult = self.vendors[vendorName].controller.get_fulfillment_status(order, vendorItems, address)
            result["shippingSpeedCategories"].extend(vendorResult["shippingSpeedCategories"])
            result["unfulfillablePreviewItems"].extend(vendorResult["unfulfillablePreviewItems"])

        return FulfillmentStatusResult(**result)

    def place_order(self, payloads: dict[ProductVendorEnum, dict]):
        result = {}
        for vendorName in payloads:
            result[vendorName] = self.vendors[vendorName].controller.create_fulfillment_order(payloads[vendorName])

        return result
