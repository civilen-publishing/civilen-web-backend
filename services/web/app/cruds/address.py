from app import models, schemas
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDAddress(CRUDBase[models.Address, schemas.AddressCreateCRUD, schemas.AddressUpdateCRUD]):
    def __init__(self, db_session: Session):
        super(CRUDAddress, self).__init__(models.Address, db_session)
