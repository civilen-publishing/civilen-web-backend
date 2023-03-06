from typing import Any, Generic, List, Optional, Type, TypeVar

from app.cruds import base
from app.database import base_class
from pydantic import BaseModel

CrudClass = TypeVar("CrudClass", bound=base.CRUDBase)
ModelType = TypeVar("ModelType", bound=base_class.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
IdType = TypeVar("IdType", bound=Any)

class BaseService(Generic[CrudClass,CreateSchemaType, UpdateSchemaType, IdType]):
    def __init__(self, crud: Type[CrudClass]):
        self.crud = crud

    def add(self, obj: CreateSchemaType) -> ModelType:
        return self.crud.create(obj)

    def get(self, id: IdType) -> Optional[ModelType]:
        return self.crud.get(id)

    def getAll(self) -> List[ModelType]:
        return self.crud.list()

    def update(self, id: IdType, obj: UpdateSchemaType) -> Optional[ModelType]:
        return self.crud.update(id, obj)

    def delete(self, id: IdType) -> None:
        self.crud.delete(id)