from typing import Optional

from app import models, schemas
from app.core import utils
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDShipbobProduct(
    CRUDBase[models.ShipbobProduct, schemas.ShipbobProductCreateCRUD, schemas.ShipbobProductUpdateCRUD]
):
    def __init__(self, db_session: Session):
        super(CRUDShipbobProduct, self).__init__(models.ShipbobProduct, db_session)

    def create(self, obj: schemas.ShipbobProductCreateCRUD) -> models.ShipbobProduct:
        db_obj: models.ShipbobProduct = super().create(schemas.ShipbobProductCreateDB(**obj.dict(exclude={"images"})))

        for image in obj.images:
            self.db_session.add(models.ProductImage(productId=db_obj.id, url=image))

        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj

    def update(self, productId: str, obj: schemas.ShipbobProductUpdateCRUD) -> models.ShipbobProduct:
        product = super().update(
            productId, schemas.ShipbobProductUpdateDB(**obj.dict(exclude={"images"}, exclude_none=True))
        )

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

    def list(self, skip: int = 0, limit: int = 100, type: Optional[str] = None) -> list[models.ShipbobProduct]:
        if type is None:
            products = super().list(skip, limit)
        else:
            products = self.db_session.query(self.model).filter(self.model.type == type).offset(skip).limit(limit).all()

        for product in products:
            product.images = (
                self.db_session.query(models.ProductImage).filter(models.ProductImage.productId == product.id).all()
            )

        return products

    def getBySku(self, sku: str) -> models.ShipbobProduct:
        return self.db_session.query(self.model).filter(self.model.sku == sku).first()
