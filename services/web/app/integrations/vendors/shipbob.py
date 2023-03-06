import requests
from app import schemas


class ShipBobIntegration:
    def __init__(self, shipbob_api_token):
        self.api_url = "https://api.shipbob.com/1.0"
        self.headers = {"Authorization": f"Bearer {shipbob_api_token}"}
        self.channel_id = self.__get_channel_id()

    def __get_channel_id(self) -> str:
        response = requests.get(f"{self.api_url}/channel", headers=self.headers)
        return str(response.json()[0]["id"])

    def get_fulfillment_order_payload(
        self,
        order: schemas.Order,
        items: list[schemas.OrderProduct],
        address: schemas.Address,
    ):
        return {
            "shipping_method": order.shippingSpeedCategory,
            "recipient": {
                "name": order.name,
                "address": {
                    "address1": address.addressLine1,
                    "address2": address.addressLine2 if address.addressLine2 else "",
                    "city": address.city,
                    "state": address.stateOrRegion,
                    "country": address.countryCode,
                    "zip_code": address.postalCode,
                },
                "email": order.email,
                "phone_number": order.phone,
            },
            "products": [
                {
                    "id": item.id,
                    "quantity": item.quantity,
                }
                for item in items
            ],
            "reference_id": str(order.id),
        }

    def create_fulfillment_order(self, payload):
        response = requests.post(
            f"{self.api_url}/order",
            headers={**self.headers, "shipbob_channel_id": self.channel_id},
            json=payload,
        )

        return response.json()

    def get_fulfillment_status(
        self,
        _: schemas.Order,
        items: list[schemas.ShipbobOrderItem],
        address: schemas.Address,
        shippingSpreedCategory: str = "Standard",
    ):
        payload = {
            "products": [item.dict(exclude={"status", "vendor", "type"}) for item in items],
            "address": {
                "address1": address.addressLine1,
                "address2": address.addressLine2 if address.addressLine2 else "",
                "city": address.city,
                "state": address.stateOrRegion,
                "country": address.countryCode,
                "zip_code": address.postalCode,
            },
            "shipping_methods": [shippingSpreedCategory],
        }

        productsResponse = requests.get(
            f"{self.api_url}/product", headers={**self.headers, "shipbob_channel_id": self.channel_id}
        )

        estimateResponse = requests.post(
            f"{self.api_url}/estimate", headers={**self.headers, "shipbob_channel_id": self.channel_id}, json=payload
        )

        if estimateResponse.json().get("statusCode") == 404 or  len(productsResponse.json()) == 0:
            return {
                "shippingSpeedCategories": [],
                "unfulfillablePreviewItems": [],
            }

        result = {
            "shippingSpeedCategories": [],
            "unfulfillablePreviewItems": [],
        }

        for item in items:
            if not any(product["reference_id"] == item.reference_id for product in productsResponse.json()):
                result["unfulfillablePreviewItems"].append(item.reference_id)

        for estimate in estimateResponse.json():
            result["shippingSpeedCategories"].append(
                {"shippingSpeedCategory": estimate["shipping_method"], "fee": estimate["estimated_price"]}
            )

        return result
