import uuid

from app import cruds, schemas
from app.core import utils
from app.enums import ProductVendorEnum
from fastapi import UploadFile

from .base import BaseService


class AmazonProductService(
    BaseService[cruds.CRUDAmazonProduct, schemas.AmazonProductCreateAPI, schemas.AmazonProductUpdateAPI, uuid.UUID]
):
    def __init__(self, amazonProductCrud: cruds.CRUDAmazonProduct):
        super(AmazonProductService, self).__init__(amazonProductCrud)
        self.uploadPath = "/src/uploads/images/products"
        self.productCrud = cruds.CRUDProduct(db_session=amazonProductCrud.db_session)

    def add(self, product: schemas.AmazonProductCreateAPI, images: list[UploadFile]) -> schemas.AmazonProduct:
        imagePaths = [utils.saveFile(image, self.uploadPath, uuid.uuid4().hex) for image in images]
        try:
            product = self.crud.create(
                schemas.AmazonProductCreateCRUD(
                    **product.dict(exclude={"images"}), images=imagePaths, vendor=ProductVendorEnum.AMAZON
                )
            )
        except Exception as e:
            for imagePath in imagePaths:
                utils.removeFile(imagePath)
            raise e
        return schemas.AmazonProduct(**product.to_dict())

    def update(
        self, productId: int, product: schemas.AmazonProductUpdateAPI, images: list[UploadFile]
    ) -> schemas.AmazonProduct:
        imagePaths = [utils.saveFile(image, self.uploadPath, uuid.uuid4().hex) for image in images]
        allPaths = imagePaths + product.images if product.images else []
        try:
            product = self.crud.update(
                productId, schemas.AmazonProductUpdateCRUD(**product.dict(exclude={"images"}), images=allPaths)
            )
        except Exception as e:
            for imagePath in imagePaths:
                utils.removeFile(imagePath)
            raise e

        return schemas.AmazonProduct(**product.to_dict())

    def delete(self, productId: int) -> None:
        product = self.crud.get(productId)
        for image in product.images:
            utils.removeFile(image)
        self.crud.delete(productId)

    def validateImages(self, images: list[UploadFile]) -> bool:
        return all([utils.validateImage(image) for image in images])

    def getBySku(self, sku: str):
        return self.crud.getBySku(sku)
