from app import models, schemas
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDPayment(CRUDBase[models.Payment, schemas.PaymentCreateCRUD, schemas.PaymentUpdateCRUD]):
    def __init__(self, db_session: Session):
        super(CRUDPayment, self).__init__(models.Payment, db_session)
