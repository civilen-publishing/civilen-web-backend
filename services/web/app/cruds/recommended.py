from app import models, schemas
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDRecommended(CRUDBase[models.Recommended, schemas.RecommendedCreateCRUD, schemas.RecommendedUpdateCRUD]):
    def __init__(self, db_session: Session):
        super(CRUDRecommended, self).__init__(models.Recommended, db_session)
