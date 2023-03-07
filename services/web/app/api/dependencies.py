from typing import Generator

from app import cruds, schemas, services
from app.core.security import loginManager
from app.database.session import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


################# CRUDs #################
def getAddressCRUD(db: Session = Depends(get_db)) -> cruds.CRUDAddress:
    return cruds.CRUDAddress(db)


def getAdminCRUD(db: Session = Depends(get_db)) -> cruds.CRUDAdmin:
    return cruds.CRUDAdmin(db)


def getErrataCRUD(db: Session = Depends(get_db)) -> cruds.CRUDErrata:
    return cruds.CRUDErrata(db)


def getOrderCRUD(db: Session = Depends(get_db)) -> cruds.CRUDOrder:
    return cruds.CRUDOrder(db)


def getProductCRUD(db: Session = Depends(get_db)) -> cruds.CRUDProduct:
    return cruds.CRUDProduct(db)


def getRecommendedCRUD(db: Session = Depends(get_db)) -> cruds.CRUDRecommended:
    return cruds.CRUDRecommended(db)


def getSlideCRUD(db: Session = Depends(get_db)) -> cruds.CRUDSlide:
    return cruds.CRUDSlide(db)


def getAmazonProductCRUD(db: Session = Depends(get_db)) -> cruds.CRUDAmazonProduct:
    return cruds.CRUDAmazonProduct(db)


def getShipbobProductCRUD(db: Session = Depends(get_db)) -> cruds.CRUDShipbobProduct:
    return cruds.CRUDShipbobProduct(db)

def getPaymentCRUD(db: Session = Depends(get_db)):
    return cruds.CRUDPayment(db)

################# Admin #################
def getAdmin(token: schemas.Admin = Depends(loginManager)) -> schemas.Admin:
    """
    Get the admin from the token

    **Note:** This function is used as a dependency for the admin endpoints
    """
    return token


################# Services #################
def getSlideService(crud: cruds.CRUDSlide = Depends(getSlideCRUD)) -> services.SlideService:
    """
    Get the slide service

    **Note:** This function is used as a dependency for the slide endpoints
    """
    return services.SlideService(crud)


def getProductService(crud: cruds.CRUDProduct = Depends(getProductCRUD)) -> services.ProductService:
    """
    Get the product service

    **Note:** This function is used as a dependency for the product endpoints
    """
    return services.ProductService(crud)


def getErrataService(crud: cruds.CRUDErrata = Depends(getErrataCRUD)) -> services.ErrataService:
    """
    Get the errata service

    **Note:** This function is used as a dependency for the errata endpoints
    """
    return services.ErrataService(crud)


def getRecommendedService(crud: cruds.CRUDRecommended = Depends(getRecommendedCRUD)) -> services.RecommendedService:
    """
    Get the recommended service

    **Note:** This function is used as a dependency for the recommended endpoints
    """
    return services.RecommendedService(crud)


def getOrderService(crud: cruds.CRUDOrder = Depends(getOrderCRUD)) -> services.OrderService:
    """
    Get the order service

    **Note:** This function is used as a dependency for the order endpoints
    """
    return services.OrderService(crud)


def getAmazonProductService(crud: cruds.CRUDAmazonProduct = Depends(getAmazonProductCRUD)) -> services.AmazonProductService:
    """
    Get the amazon product service

    **Note:** This function is used as a dependency for the amazon product endpoints
    """
    return services.AmazonProductService(crud)


def getShipbobProductService(
    crud: cruds.CRUDShipbobProduct = Depends(getShipbobProductCRUD),
) -> services.ShipbobProductService:
    """
    Get the Shipbob product service

    **Note:** This function is used as a dependency for the Shipbob product endpoints
    """
    return services.ShipbobProductService(crud)


def getPaymentService(
    crud: cruds.CRUDPayment = Depends(getPaymentCRUD),
) -> services.PaymentService:
    """
    Get the Payment service

    **Note:** This function is used as a dependency for the Payment endpoints
    """
    return services.PaymentService(crud)
