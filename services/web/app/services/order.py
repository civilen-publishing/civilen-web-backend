import uuid

from app import cruds, schemas
from app.enums import OrderStatusEnum, PaymentVendorEnum, ShippingSpeedEnum
from app.integrations import StripeIntegration, StripeLineItem, VendorsManager
from app.services import emailService

from .base import BaseService
from .payment import PaymentService


class OrderService(BaseService[cruds.CRUDOrder, schemas.OrderCreateAPI, schemas.OrderUpdateAPI, uuid.UUID]):
    def __init__(self, orderCrud: cruds.CRUDOrder):
        super(OrderService, self).__init__(orderCrud)
        self.orderCrud = orderCrud
        self.vendors_manager = VendorsManager()
        self.stripe_manager = StripeIntegration()
        self.productCrud = cruds.CRUDProduct(self.orderCrud.db_session)
        self.paymentService = PaymentService(cruds.CRUDPayment(self.orderCrud.db_session))

    def add(self, order: schemas.OrderCreateAPI):
        orderObject, orderItems, address = self.orderCrud.create(
            schemas.OrderCreateCRUD(
                **order.dict(),
                shippingSpeedCategory=ShippingSpeedEnum.STANDARD,
                status=OrderStatusEnum.WAITING_FOR_CONFIRMATION
            )
        )
        return {
            "orderId": orderObject.id,
            "fulfillmentStatusResult": self.vendors_manager.get_order_fulfillment_status(
                orderObject, orderItems, address
            ),
        }

    def getWithDetails(self, orderId: uuid.UUID) -> tuple[schemas.Order, list[schemas.OrderProduct], schemas.Address]:
        return self.orderCrud.getWithDetails(orderId)

    def filterByStatus(self, status: OrderStatusEnum) -> list[schemas.Order]:
        return self.orderCrud.filterByStatus(status)

    def placeOrder(self, orderId: uuid.UUID, payload: schemas.ConfirmOrder):
        orderObject, orderItems, address = self.getWithDetails(orderId)
        if orderObject.status != OrderStatusEnum.WAITING_FOR_CONFIRMATION:
            return {"error": "Order is already confirmed"}
        order_fulfillment_status = self.vendors_manager.get_order_fulfillment_status(orderObject, orderItems, address)
        if len(order_fulfillment_status.unfulfillablePreviewItems) > 0:
            return {"error": "Order is not fulfillable", "fulfillmentStatusResult": order_fulfillment_status}

        shippingFee = 0
        for item in order_fulfillment_status.shippingSpeedCategories:
            if item["shippingSpeedCategory"] == payload.shippingSpeedCategory.capitalize():
                shippingFee += float(item["fee"])

        paymentItems = [
            StripeLineItem(
                **{
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": item.price * 100,
                        "product_data": {
                            "name": (self.productCrud.get(item.id).title or "Product"),
                        },
                    },
                    "quantity": item.quantity,
                }
            )
            for item in orderItems
        ]
        paymentItems.append(
            StripeLineItem(
                **{
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": shippingFee * 100,
                        "product_data": {
                            "name": "Shipping",
                        },
                    },
                    "quantity": 1,
                }
            )
        )

        self.update(
            orderId,
            schemas.OrderUpdateCRUD(
                status=OrderStatusEnum.PENDING_PAYMENT, shippingSpeedCategory=payload.shippingSpeedCategory
            ),
        )
        total = shippingFee + sum(item.price * 100 for item in orderItems)
        payment = self.paymentService.add(
            schemas.PaymentCreateAPI(total=total, orderId=orderObject.id, vendor=PaymentVendorEnum.STRIPE)
        )

        return {
            "id": orderObject.id,
            "paymentLink": self.stripe_manager.createPaymentLink(payment.id, paymentItems).url,
        }

    def paymentSuccess(self, paymentId: uuid.UUID):
        orderId = self.paymentService.getOrderId(paymentId)
        orderObject, orderItems, address = self.getWithDetails(orderId)
        if orderObject.status != OrderStatusEnum.SHIPPED:
            return {"error": "Order is already shipped"}

        payloads = self.vendors_manager.get_order_fulfillment_payload(orderObject, orderItems, address)

        try:
            # responses = self.vendors_manager.place_order(payloads)
            responses = {}
            for response in responses:
                if "errors" in response:
                    self.update(orderId, schemas.OrderUpdateCRUD(status=OrderStatusEnum.FAILED_BY_VENDOR))
                    emailService.send()
                    return {"error": "Order failed by Amazon"}

            self.update(orderId, schemas.OrderUpdateCRUD(status=OrderStatusEnum.SHIPPED))
            return {"success": "Order shipped"}
        except Exception as e:
            self.update(orderId, schemas.OrderUpdateCRUD(status=OrderStatusEnum.FAILED_BY_VENDOR))
            emailService.send()
            return {"error": "Order failed by Amazon"}

    def paymentCancel(self, paymentId: uuid.UUID):
        orderId = self.paymentService.getOrderId(paymentId)
        self.update(orderId, schemas.OrderUpdateCRUD(status=OrderStatusEnum.CANCELED))
        return {"message": "Order canceled"}
