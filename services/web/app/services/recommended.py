import uuid

from app import cruds, schemas

from .base import BaseService


class RecommendedService(
    BaseService[cruds.CRUDRecommended, schemas.RecommendedCreateAPI, schemas.RecommendedUpdateAPI, uuid.UUID]
):
    def __init__(self, recommendedCrud: cruds.CRUDRecommended):
        super(RecommendedService, self).__init__(recommendedCrud)
        self.recommendedCrud = recommendedCrud
        self.productCrud = cruds.CRUDProduct(self.recommendedCrud.db_session)

    def add(self, recommended: schemas.RecommendedCreateAPI) -> schemas.Recommended:
        product = self.productCrud.get(recommended.productId)
        recommendedObject = self.recommendedCrud.create(
            schemas.RecommendedCreateCRUD(**recommended.dict(), productType=product.type)
        )
        return schemas.Recommended(**recommendedObject.to_dict(), product=product)

    def get(self, recommendedId: uuid.UUID) -> schemas.Recommended:
        recommendedObject = self.recommendedCrud.get(recommendedId)
        product = self.productCrud.get(recommendedObject.productId)
        return schemas.Recommended(**recommendedObject.to_dict(), product=product)

    def getAll(self) -> list[schemas.Recommended]:
        recommendedObjects = self.recommendedCrud.list()
        recommendedProducts = [
            schemas.Recommended(
                **recommendedObject.to_dict(), product=self.productCrud.get(recommendedObject.productId)
            )
            for recommendedObject in recommendedObjects
        ]
        return recommendedProducts
