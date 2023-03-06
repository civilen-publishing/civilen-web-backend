from app import schemas, services
from app.api import dependencies
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class Response(BaseModel):
    erratas: list[schemas.Errata]
    products: list[schemas.Product]
    recommended: list[schemas.Recommended]
    slides: list[schemas.Slide]

@router.get("/get-all", response_model=Response)
def getAll(
    errataService: services.ErrataService = Depends(dependencies.getErrataService),
    productService: services.ProductService = Depends(dependencies.getProductService),
    recommendedService: services.RecommendedService = Depends(dependencies.getRecommendedService),
    slideService: services.SlideService = Depends(dependencies.getSlideService),
):
    return {
        "erratas": errataService.getAll(),
        "products": productService.getAll(),
        "recommended": recommendedService.getAll(),
        "slides": slideService.getAll(),
    }
