import uuid

from app import cruds, schemas

from .base import BaseService


class ErrataService(BaseService[cruds.CRUDErrata, schemas.ErrataCreateAPI, schemas.ErrataUpdateAPI, uuid.UUID]):
    def __init__(self, errataCrud: cruds.CRUDErrata):
        super(ErrataService, self).__init__(errataCrud)
        self.errataCrud = errataCrud
        self.productCrud = cruds.CRUDProduct(self.errataCrud.db_session)

    def add(self, errata: schemas.ErrataCreateAPI) -> schemas.Errata:
        product = self.productCrud.get(errata.productId)
        errataObject = self.errataCrud.create(errata)
        return schemas.Errata(**errataObject.to_dict(), product=product)

    def get(self, errataId: uuid.UUID) -> schemas.Errata:
        errataObject = self.errataCrud.get(errataId)
        product = self.productCrud.get(errataObject.productId)
        return schemas.Errata(**errataObject.to_dict(), product=product)

    def getAll(self) -> list[schemas.Errata]:
        errataObjects = self.errataCrud.list()
        erratas = []
        for errataObject in errataObjects:
            product = self.productCrud.get(errataObject.productId)
            erratas.append(schemas.Errata(**errataObject.to_dict(), product=product))
        return erratas

    def update(self, errataId: uuid.UUID, errata: schemas.ErrataUpdateAPI) -> schemas.Errata:
        errataObject = self.errataCrud.update(errataId, errata)
        product = self.productCrud.get(errataObject.productId)
        return schemas.Errata(**errataObject.to_dict(), product=product)
