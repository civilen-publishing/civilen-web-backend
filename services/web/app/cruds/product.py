import uuid

from app import models, schemas
from app.core import utils
from app.enums import ProductVendorEnum
from sqlalchemy.orm import Session

from .amazonProduct import CRUDAmazonProduct
from .base import CRUDBase
from .shipbobProduct import CRUDShipbobProduct


class CRUDProduct(CRUDBase[models.Product, schemas.ProductCreateDB, schemas.ProductUpdateDB]):
    def __init__(self, db_session: Session):
        super(CRUDProduct, self).__init__(models.Product, db_session)
        self.uploadPath = "./uploads/images/products"
        self.vendors: dict[ProductVendorEnum, CRUDBase] = {
            ProductVendorEnum.AMAZON: CRUDAmazonProduct(self.db_session),
            ProductVendorEnum.SHIPBOB: CRUDShipbobProduct(self.db_session),
        }

        self.interfaces = {
            ProductVendorEnum.AMAZON: schemas.AmazonProduct,
            ProductVendorEnum.SHIPBOB: schemas.ShipbobProduct,
        }

    def get(self, productId: uuid.UUID) -> schemas.AmazonProduct | schemas.ShipbobProduct:
        rawProduct: models.Product | None = self.db_session.query(self.model).get(productId)
        if rawProduct is None:
            return None
        return self.interfaces[rawProduct.vendor](**rawProduct.to_dict())

    def create(self, obj: schemas.ProductCreateCRUD) -> models.Product:
        db_obj: models.Product = super().create(schemas.ProductCreateDB(**obj.dict()))
        for image in obj.images:
            self.db_session.add(models.ProductImage(productId=db_obj.id, url=image))
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj

    def update(self, productId: uuid.UUID, obj: schemas.ProductUpdateCRUD) -> models.Product:
        product = super().update(productId, schemas.ProductUpdateDB(**obj.dict(exclude={"images"})))

        # Delete Images that are not in the list
        for image in product.images:
            if image.url not in obj.images:
                utils.removeFile(image.url)
                self.db_session.delete(image)

        # Add Images that are not in the database
        for image in obj.images:
            if image not in [image.url for image in product.images]:
                self.db_session.add(models.ProductImage(productId=product.id, url=image))

        self.db_session.commit()
        self.db_session.refresh(product)
        return product

    def list(self, skip: int = 0, limit: int = 100, type: str = None) -> list[models.Product]:
        if type is None:
            products = super().list(skip, limit)
        else:
            products = self.db_session.query(self.model).filter(self.model.type == type).offset(skip).limit(limit).all()

        for product in products:
            product.images = (
                self.db_session.query(models.ProductImage).filter(models.ProductImage.productId == product.id).all()
            )

        return products

    def getSku(self, id: uuid.UUID) -> str:
        product = self.get(id)
        if product is None:
            return ""
        return self.vendors[product.vendor].get(product.id).sku
