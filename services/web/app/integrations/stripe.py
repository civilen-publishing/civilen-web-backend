import uuid

import stripe
from app.core.config import get_settings
from pydantic import BaseModel


class StripeProductData(BaseModel):
    name: str


class StripePriceData(BaseModel):
    unit_amount: int
    currency: str
    product_data: StripeProductData


class StripeLineItem(BaseModel):
    price_data: StripePriceData
    quantity: int


class StripeIntegration:
    def __init__(self):
        stripe.api_key = get_settings().STRIPE_SECRET_KEY

    def create_checkout_session(self, line_items: list[StripeLineItem], success_url: str, cancel_url: str):
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[line_item.dict() for line_item in line_items],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )

    def createPaymentLink(self, orderId: uuid.UUID, items: list[StripeLineItem] = []) -> str:
        return self.create_checkout_session(
            items,
            f"{get_settings().DOMAIN_NAME}/api/order/payment/success/{orderId}",
            f"{get_settings().DOMAIN_NAME}/api/order/payment/cancel/{orderId}",
        )
