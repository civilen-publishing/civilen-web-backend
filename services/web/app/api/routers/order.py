import uuid

from app import models, schemas, services
from app.api import dependencies
from app.enums import OrderStatusEnum
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/add")
def add(
    order: schemas.OrderCreateAPI,
    orderService: services.OrderService = Depends(dependencies.getOrderService),
):
    return orderService.add(order)


@router.get("/get/{orderId}")
def get(
    orderId: uuid.UUID,
    orderService: services.OrderService = Depends(dependencies.getOrderService),
):
    return orderService.getWithDetails(orderId)


@router.get("/getAll")
def getAll(
    orderService: services.OrderService = Depends(dependencies.getOrderService),
):
    return orderService.getAll()


@router.get("/filterByStatus/{status}")
def filterByStatus(
    status: OrderStatusEnum,
    orderService: services.OrderService = Depends(dependencies.getOrderService),
):
    return orderService.filterByStatus(status)


@router.post("/confirm/{orderId}")
def confirm(
    orderId: uuid.UUID,
    payload: schemas.ConfirmOrder,
    orderService: services.OrderService = Depends(dependencies.getOrderService),
):
    return orderService.placeOrder(orderId, payload)


@router.get("/payment/success/{paymentId}")
def paymentSuccess(
    paymentId: uuid.UUID,
    orderService: services.OrderService = Depends(dependencies.getOrderService),
):
    return orderService.paymentSuccess(paymentId)


@router.get("/payment/cancel/{paymentId}")
def paymentCancel(
    paymentId: uuid.UUID,
    orderService: services.OrderService = Depends(dependencies.getOrderService),
):
    return orderService.paymentCancel(paymentId)
