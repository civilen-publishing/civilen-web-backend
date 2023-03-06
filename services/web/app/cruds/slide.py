
from app import models, schemas
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDSlide(CRUDBase[models.Slide, schemas.SlideCreateCRUD, schemas.SlideUpdateCRUD]):
    def __init__(self, db_session: Session):
        super(CRUDSlide, self).__init__(models.Slide, db_session)