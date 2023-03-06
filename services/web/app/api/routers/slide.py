import uuid
from typing import Any

from app import schemas, services
from app.api import dependencies
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

router = APIRouter()


@router.post("/add", response_model=schemas.Slide | Any, dependencies=[Depends(dependencies.getAdmin)])
def add(
    slide: schemas.SlideCreateAPI,
    slideService: services.SlideService = Depends(dependencies.getSlideService),
    image: UploadFile = File(...),
) -> schemas.Slide:
    """
    Add a slide to the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """

    if not slideService.validateImage(image):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid image format")

    return slideService.add(slide, image)


@router.get("/get/{slideId}", response_model=schemas.Slide)
def get(
    slideId: uuid.UUID,
    slideService: services.SlideService = Depends(dependencies.getSlideService),
) -> schemas.Slide:
    """
    Get a slide from the database and return it as a response
    """
    return slideService.get(slideId)


@router.get("/get-all", response_model=list[schemas.Slide])
def getAll(
    slideService: services.SlideService = Depends(dependencies.getSlideService),
) -> list[schemas.Slide]:
    """
    Get all slides from the database and return them as a response
    """
    return slideService.getAll()


@router.put("/update/{slideId}", response_model=schemas.Slide, dependencies=[Depends(dependencies.getAdmin)])
def update(
    slideId: uuid.UUID,
    slide: schemas.SlideUpdateAPI,
    slideService: services.SlideService = Depends(dependencies.getSlideService),
) -> schemas.Slide:
    """
    Update a slide in the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    return slideService.update(slideId, slide)


@router.delete("/delete/{slideId}", dependencies=[Depends(dependencies.getAdmin)])
def delete(
    slideId: uuid.UUID,
    slideService: services.SlideService = Depends(dependencies.getSlideService),
) -> schemas.Slide:
    """
    Delete a slide from the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    slideService.delete(slideId)
    return {"message": "Slide deleted successfully"}
