# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


import yaml
from app import cruds, schemas
from app.core.security import passwordManager
from app.database import base  # noqa: F401
from pydantic import BaseModel
from sqlalchemy.orm import Session


class Admin(BaseModel):
    name: str
    email: str
    username: str
    password: str
    isSuperAdmin: bool


class SeederInput(BaseModel):
    admins: list[Admin]


class Seeder:
    def __init__(self, db: Session):
        self.db = db
        self._admin = cruds.CRUDAdmin(db)

    def seed(self, data: SeederInput):
        for admin in data.admins:
            if not self._admin.getByUsername(admin.username):
                admin.password = passwordManager.getPasswordHash(admin.password)
                self._admin.create(schemas.AdminCreateCRUD(**admin.dict()))


def init_db(db: Session) -> None:
    with open("/src/seed.yml") as f:
        data = yaml.safe_load(f)
        seeder = Seeder(db)
        try:
            seeder.seed(SeederInput(**data))
        except Exception as e:
            db.rollback()
        else:
            db.commit()
