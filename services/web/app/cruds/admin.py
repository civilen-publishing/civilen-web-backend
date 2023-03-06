from app import models, schemas
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDAdmin(CRUDBase[models.Admin, schemas.AdminCreateCRUD, schemas.AdminUpdateCRUD]):
    def __init__(self, db_session: Session):
        super(CRUDAdmin, self).__init__(models.Admin, db_session)

    def getByUsername(self, username: str) -> models.Admin:
        return self.db_session.query(self.model).filter(self.model.username == username).first()