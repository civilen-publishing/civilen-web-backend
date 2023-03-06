import uuid
from typing import List, Tuple

from app import models, schemas
from app.enums import OrderStatusEnum, ProductVendorEnum
from sqlalchemy.orm import Session

from .address import CRUDAddress
from .base import CRUDBase
from .product import CRUDProduct


class CRUDOrder(CRUDBase[models.Order, schemas.OrderCreateDB, schemas.OrderUpdateDB]):
    def __init__(self, db_session: Session):
        super(CRUDOrder, self).__init__(models.Order, db_session)
        self.orderItemModel = models.OrderItem
        self.addressCRUD = CRUDAddress(db_session)
        self.productCRUD = CRUDProduct(db_session)

    def getWithDetails(self, id: uuid.UUID) -> Tuple[schemas.Order, list[schemas.OrderProduct], schemas.Address]:
        order = self.get(id)

        orderItems: list[models.OrderItem] = (
            self.db_session.query(self.orderItemModel).filter(self.orderItemModel.orderId == order.id).all()
        )
        address = schemas.Address(**self.addressCRUD.get(order.addressId).to_dict())

        orderItemsOut: list[schemas.OrderProduct] = []
        for orderItem in orderItems:
            product = self.productCRUD.get(orderItem.productId)
            if product is None:
                continue
            sku = self.productCRUD.getSku(product.id)
            orderItemOut = schemas.OrderProduct(**product.dict(exclude={"sku"}), quantity=orderItem.quantity, sku=sku)
            if orderItemOut.vendor == ProductVendorEnum.AMAZON:
                orderItemOut.sellerFulfillmentOrderItemId = str(orderItemOut.id)
                orderItemOut.sellerSku = sku
            if orderItemOut.vendor == ProductVendorEnum.SHIPBOB:
                orderItemOut.reference_id = product.referenceId
            orderItemsOut.append(orderItemOut)
        return (order, orderItemsOut, address)

    def create(self, obj: schemas.OrderCreateCRUD) -> tuple[schemas.Order, list[schemas.OrderProduct], schemas.Address]:
        address = self.addressCRUD.create(obj.address)
        db_obj = super().create(schemas.OrderCreateDB(**obj.dict(), addressId=address.id))

        orderItemsOut: list[schemas.OrderProduct] = []
        for orderItem in obj.orderItems:
            item = self.orderItemModel(**schemas.OrderItemCreateCRUD(orderId=db_obj.id, **orderItem.dict()).dict())
            self.db_session.add(item)
            self.db_session.commit()
            product = self.productCRUD.get(orderItem.productId)
            if product is None:
                continue
            sku = self.productCRUD.getSku(product.id)
            orderItemOut = schemas.OrderProduct(**product.dict(exclude={"sku"}), quantity=item.quantity, sku=sku)
            if orderItemOut.vendor == ProductVendorEnum.AMAZON:
                orderItemOut.sellerFulfillmentOrderItemId = str(orderItemOut.id)
                orderItemOut.sellerSku = sku
            if orderItemOut.vendor == ProductVendorEnum.SHIPBOB:
                orderItemOut.reference_id = product.referenceId
            orderItemsOut.append(orderItemOut)

        self.db_session.commit()
        self.db_session.refresh(db_obj)

        return (db_obj, orderItemsOut, obj.address)

    def filterByStatus(
        self, status: OrderStatusEnum, skip: int = 0, limit: int = 100
    ) -> list[tuple[schemas.Order, List[schemas.OrderProduct], schemas.Address]]:
        orders = self.db_session.query(self.model).filter(self.model.status == status).offset(skip).limit(limit).all()
        result = []
        for order in orders:
            result.append(self.getWithDetails(order.id))

        return result
