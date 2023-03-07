import uuid

from app import cruds, schemas
from app.core import utils
from app.enums.product import ProductVendorEnum
from fastapi import UploadFile

from .amazonProduct import AmazonProductService
from .base import BaseService
from .shipbobProduct import ShipbobProductService


class ProductService(BaseService[cruds.CRUDProduct, schemas.ProductCreateCRUD, schemas.ProductUpdateCRUD, uuid.UUID]):
    def __init__(self, productCrud: cruds.CRUDProduct):
        super(ProductService, self).__init__(productCrud)
        self.productCrud = productCrud
        self.amazonProductService = AmazonProductService(cruds.CRUDAmazonProduct(db_session=productCrud.db_session))
        self.shipbobProductService = ShipbobProductService(cruds.CRUDShipbobProduct(db_session=productCrud.db_session))

        
    def delete(self, productId: uuid.UUID) -> None:
        product = self.productCrud.get(productId)
        for image in product.images:
            utils.removeFile(image)

        if product.vendor == ProductVendorEnum.AMAZON:
            self.amazonProductService.delete(productId)
        elif product.vendor == ProductVendorEnum.SHIPBOB:
            self.shipbobProductService.delete(productId)


    def validateImages(self, images: list[UploadFile]) -> bool:
        return all([utils.validateImage(image) for image in images])

    def getBySku(self, sku: str):
        return self.amazonProductService.getBySku(sku)
