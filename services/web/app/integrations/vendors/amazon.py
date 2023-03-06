import datetime

from app import schemas
from sp_api.api import FulfillmentOutbound
from sp_api.base import Marketplaces


class AmazonIntegration:
    def __init__(
        self,
        credentials,
        sellerId,
        marketplace=Marketplaces.US,
    ):
        self.credentials = credentials
        self.marketplace = marketplace
        self.sellerId = sellerId
        self.fulfillment_outbound = FulfillmentOutbound(credentials=self.credentials)

    def get_fulfillment_order_payload(
        self,
        order: schemas.Order,
        items: list[schemas.OrderProduct],
        address: schemas.Address,
    ):
        return {
            "items": [
                schemas.AmazonOrderItem(
                    price=item.price,
                    quantity=item.quantity,
                    sellerFulfillmentOrderItemId=str(item.id),
                    sellerSku=item.sku,
                )
                for item in items
            ],
            "destinationAddress": {**address.dict(), "phone": order.phone, "name": order.name},
            "shippingSpreedCategory": order.shippingSpeedCategory,
            "sellerFulfillmentOrderId": order.id,
            "displayableOrderId": order.id,
            "displayableOrderDateTime": datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ"),
        }

    def create_fulfillment_order(self, payload):
        return self.fulfillment_outbound.create_fulfillment_order(**payload)

    def get_fulfillment_status(
        self,
        order: schemas.Order,
        items: list[schemas.AmazonOrderItem],
        address: schemas.Address,
        shippingSpreedCategory: str = "",
    ):
        payload = {
            "items": [item.dict(exclude={"status", "vendor", "type"}) for item in items],
            "address": {**address.dict(), "phone": order.phone, "name": order.name},
            "shippingSpreedCategories": [shippingSpreedCategory],
        }
        try:
            response = self.fulfillment_outbound.get_fulfillment_preview(**payload).payload.get("fulfillmentPreviews", [])

            result = {
                "shippingSpeedCategories": [],
                "unfulfillablePreviewItems": [],
            }

            for item in response:
                fees = item.get("estimatedFees", [])
                for fee in fees:
                    if fee.get("name") == "FBAPerUnitFulfillmentFee":
                        result["shippingSpeedCategories"].append(
                            {
                                "shippingSpeedCategory": item.get("shippingSpeedCategory"),
                                "fee": fee.get("amount").get("value"),
                            }
                        )
                result["unfulfillablePreviewItems"].extend(item.get("unfulfillablePreviewItems"))

            return result
        except Exception as e:
            print(e)
            return {
                "shippingSpeedCategories": [],
                "unfulfillablePreviewItems": [],
            }
