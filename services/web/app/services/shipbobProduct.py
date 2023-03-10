import uuid

from app import cruds, schemas
from app.core import utils
from app.enums import ProductVendorEnum
from fastapi import UploadFile

from .base import BaseService


class ShipbobProductService(
    BaseService[cruds.CRUDShipbobProduct, schemas.ShipbobProductCreateAPI, schemas.ShipbobProductUpdateAPI, uuid.UUID]
):
    def __init__(self, shipbobProductCrud: cruds.CRUDShipbobProduct):
        super(ShipbobProductService, self).__init__(shipbobProductCrud)
        self.uploadPath = "/src/uploads/images/products"
        self.productCrud = cruds.CRUDProduct(db_session=shipbobProductCrud.db_session)

    def add(self, product: schemas.ShipbobProductCreateAPI, images: list[UploadFile]) -> schemas.ShipbobProduct:
        imagePaths = [utils.saveFile(image, self.uploadPath, uuid.uuid4().hex) for image in images]
        try:
            product = self.crud.create(
                schemas.ShipbobProductCreateCRUD(
                    **product.dict(exclude={"images"}), images=imagePaths, vendor=ProductVendorEnum.SHIPBOB
                )
            )
        except Exception as e:
            for imagePath in imagePaths:
                utils.removeFile(imagePath)
            raise e
        return schemas.ShipbobProduct(**product.to_dict())

    def update(
        self, productId: uuid.UUID, product: schemas.ShipbobProductUpdateAPI, images: list[UploadFile]
    ) -> schemas.ShipbobProduct:
        imagePaths = [utils.saveFile(image, self.uploadPath, uuid.uuid4().hex) for image in images]
        allPaths = imagePaths + product.images if product.images else []
        try:
            product = self.crud.update(
                productId, schemas.ShipbobProductUpdateCRUD(**product.dict(exclude={"images"}), images=allPaths)
            )
        except Exception as e:
            for imagePath in imagePaths:
                utils.removeFile(imagePath)
            raise e

        return schemas.ShipbobProduct(**product.to_dict())

    def delete(self, productId: uuid.UUID) -> None:
        product = self.crud.get(productId)
        for image in product.images:
            utils.removeFile(image.path)
        self.crud.delete(productId)

    def validateImages(self, images: list[UploadFile]) -> bool:
        return all([utils.validateImage(image) for image in images])

    def getBySku(self, sku: str):
        return self.crud.getBySku(sku)
