from app import models, schemas
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDErrata(CRUDBase[models.Errata, schemas.ErrataCreateCRUD, schemas.ErrataUpdateCRUD]):
    def __init__(self, db_session: Session):
        super(CRUDErrata, self).__init__(models.Errata, db_session)
