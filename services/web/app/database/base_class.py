import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    __exclude__ = []  # List of columns to exclude from the to_dict method

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Generate __repr__ automatically
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({', '.join(f'{key}={value!r}' for key, value in self.__dict__.items())} )"

    def to_dict(self, exclude: list = [], includeRelations: bool = True) -> dict:
        exclude = exclude + self.__exclude__
        columns = {
            column.name: getattr(self, column.name) for column in self.__table__.columns if column.name not in exclude
        }
        # add the inherited columns
        for column in self.__mapper__.columns:
            if column.name not in exclude:
                columns[column.name] = getattr(self, column.name)
        if includeRelations:
            for relation in self.__mapper__.relationships:
                if relation.key not in exclude:
                    columns[relation.key] = getattr(self, relation.key)
        return columns


class TimestampMixin(object):
    created_at: datetime.datetime = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Column(
        DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class SoftDeleteMixin(object):
    is_deleted: bool = Column(Boolean, nullable=False, default=False)
    deleted_at: datetime.datetime = Column(DateTime, nullable=True)


class UUIDMixin(object):
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)


class InheritanceMixin(object):
    discriminator: str = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "base",
    }
