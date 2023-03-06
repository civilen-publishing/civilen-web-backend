from app import schemas, services
from app.api import dependencies
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/get-all", response_model=list[schemas.Payment], dependencies=[Depends(dependencies.getAdmin)])
def getAll(
    paymentService: services.PaymentService = Depends(dependencies.getPaymentService),
) -> list[schemas.Payment]:
    """
    Get all payment from the database and return them as a response
    """
    return paymentService.getAll()
