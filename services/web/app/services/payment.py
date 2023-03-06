import uuid

from app import cruds, schemas

from .base import BaseService


class PaymentService(BaseService[cruds.CRUDPayment, schemas.PaymentCreateAPI, schemas.PaymentUpdateAPI, uuid.UUID]):
    def __init__(self, paymentCrud: cruds.CRUDPayment):
        super(PaymentService, self).__init__(paymentCrud)

    def getOrderId(self, paymentId: uuid.UUID) -> uuid.UUID:
        payment = self.get(paymentId)
        if payment is None:
            return None
        return payment.orderId