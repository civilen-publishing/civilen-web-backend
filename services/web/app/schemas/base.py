import json
from typing import Optional

from pydantic import BaseModel, main


class JsonModel(BaseModel):
    """
    A Pydantic model that can be converted to and from JSON
    This is useful for converting SQLAlchemy models to JSON
    **Note:** This class is not meant to be used directly
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AllOptional(main.ModelMetaclass):
    """
    A metaclass that makes all fields optional
    """

    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)
