import uuid

from app import schemas, services
from app.api import dependencies
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/add", response_model=schemas.Errata, dependencies=[Depends(dependencies.getAdmin)])
def add(
    errata: schemas.ErrataCreateAPI,
    errataService: services.ErrataService = Depends(dependencies.getErrataService),
) -> schemas.Errata:
    """
    Add an errata to the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    return errataService.add(errata)


@router.get("/get/{errataId}", response_model=schemas.Errata)
def get(
    errataId: uuid.UUID,
    errataService: services.ErrataService = Depends(dependencies.getErrataService),
) -> schemas.Errata:
    """
    Get an errata from the database and return it as a response
    """
    return errataService.get(errataId)


@router.get("/get-all", response_model=list[schemas.Errata])
def getAll(
    errataService: services.ErrataService = Depends(dependencies.getErrataService),
) -> list[schemas.Errata]:
    """
    Get all erratas from the database and return them as a response
    """
    return errataService.getAll()


@router.put("/update/{errataId}", response_model=schemas.Errata, dependencies=[Depends(dependencies.getAdmin)])
def update(
    errataId: uuid.UUID,
    errata: schemas.ErrataUpdateAPI,
    errataService: services.ErrataService = Depends(dependencies.getErrataService),
) -> schemas.Errata:
    """
    Update an errata in the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    return errataService.update(errataId, errata)


@router.delete("/delete/{errataId}", dependencies=[Depends(dependencies.getAdmin)])
def delete(
    errataId: uuid.UUID,
    errataService: services.ErrataService = Depends(dependencies.getErrataService),
) -> schemas.Errata:
    """
    Delete an errata from the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    errataService.delete(errataId)
    return {"message": "Successfully deleted errata"}