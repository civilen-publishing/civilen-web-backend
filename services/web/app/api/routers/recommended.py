import uuid

from app import schemas, services
from app.api import dependencies
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/add", response_model=schemas.Recommended, dependencies=[Depends(dependencies.getAdmin)])
def add(
    recommended: schemas.RecommendedCreateAPI,
    recommendedService: services.RecommendedService = Depends(dependencies.getRecommendedService),
) -> schemas.Recommended:
    """
    Add a recommended to the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    return recommendedService.add(recommended)


@router.get("/get/{recommendedId}", response_model=schemas.Recommended)
def get(
    recommendedId: uuid.UUID,
    recommendedService: services.RecommendedService = Depends(dependencies.getRecommendedService),
) -> schemas.Recommended:
    """
    Get a recommended from the database and return it as a response
    """
    return recommendedService.get(recommendedId)


@router.get("/get-all", response_model=list[schemas.Recommended])
def getAll(
    recommendedService: services.RecommendedService = Depends(dependencies.getRecommendedService),
) -> list[schemas.Recommended]:
    """
    Get all recommended Products from the database and return them as a response
    """
    return recommendedService.getAll()


@router.delete("/delete/{recommendedId}", dependencies=[Depends(dependencies.getAdmin)])
def delete(
    recommendedId: uuid.UUID,
    recommendedService: services.RecommendedService = Depends(dependencies.getRecommendedService),
) -> schemas.Recommended:
    """
    Delete a recommended from the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    recommendedService.delete(recommendedId)
    return {"message": "Recommended deleted successfully"}