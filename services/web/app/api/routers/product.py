import uuid

from app import models, schemas, services
from app.api import dependencies
from app.enums import ProductVendorEnum
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

router = APIRouter()


@router.post("/amazon/add/", response_model=schemas.AmazonProduct, dependencies=[Depends(dependencies.getAdmin)])
def add(
    product: schemas.AmazonProductCreateAPI,
    amazonProductService: services.AmazonProductService = Depends(dependencies.getAmazonProductService),
    images: list[UploadFile] = File(...),
) -> schemas.Product:
    """
    Add a product to the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    if not amazonProductService.validateImages(images):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid image format")
    return amazonProductService.add(product, images)


@router.post("/shipbob/add/", response_model=schemas.ShipbobProduct, dependencies=[Depends(dependencies.getAdmin)])
def add(
    product: schemas.ShipbobProductCreateAPI,
    shipbobProductService: services.ShipbobProductService = Depends(dependencies.getShipbobProductService),
    images: list[UploadFile] = File(...),
) -> schemas.Product:
    """
    Add a product to the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    if not shipbobProductService.validateImages(images):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid image format")
    return shipbobProductService.add(product, images)


@router.get("/get/{productId}")
def get(
    productId: uuid.UUID, productService: services.ProductService = Depends(dependencies.getProductService)
) -> schemas.Product:
    """
    Get a product from the database and return it as a response
    """
    product = productService.get(productId)
    if product.vendor == ProductVendorEnum.AMAZON:
        return schemas.AmazonProduct(**product.to_dict())
    elif product.vendor == ProductVendorEnum.SHIPBOB:
        return schemas.ShipbobProduct(**product.to_dict())
    return product


@router.get("/getAll")
def getAll(productService: services.ProductService = Depends(dependencies.getProductService)) -> list[schemas.Product]:
    """
    Get all products from the database and return them as a response
    """
    products = productService.getAll()
    for product in products:
        if product.vendor == ProductVendorEnum.AMAZON:
            product = schemas.AmazonProduct(**product.to_dict())
        elif product.vendor == ProductVendorEnum.SHIPBOB:
            product = schemas.ShipbobProduct(**product.to_dict())

    return products


@router.put("/update/amazon/{productId}", dependencies=[Depends(dependencies.getAdmin)])
def update(
    productId: uuid.UUID,
    product: schemas.AmazonProductUpdateAPI,
    images: list[UploadFile] = File(
        ...,
    ),
    productService: services.AmazonProductService = Depends(dependencies.getAmazonProductService),
) -> schemas.Product:
    """
    Update a product in the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    return productService.update(productId, product, images)


@router.put("/update/shipbob/{productId}", dependencies=[Depends(dependencies.getAdmin)])
def update(
    productId: uuid.UUID,
    product: schemas.ShipbobProductUpdateAPI,
    images: list[UploadFile] = File(
        ...,
    ),
    productService: services.ShipbobProductService = Depends(dependencies.getShipbobProductService),
) -> schemas.Product:
    """
    Update a product in the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    return productService.update(productId, product, images)


@router.delete("/delete/{productId}", dependencies=[Depends(dependencies.getAdmin)])
def delete(
    productId: uuid.UUID, productService: services.ProductService = Depends(dependencies.getProductService)
) -> schemas.Product:
    """
    Delete a product from the database and return it as a response

    **Note:** This endpoint is only accessible to admins
    """
    productService.delete(productId)
    return {"message": "Product deleted successfully"}
