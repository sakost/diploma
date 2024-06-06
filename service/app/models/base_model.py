from __future__ import annotations

import datetime
from typing import TypeVar
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, MetaData
from sqlalchemy.orm import as_declarative, declared_attr

from app.utils.text_formatter import camel_to_snake_formatter


T = TypeVar("T", bound="BaseModel")

metadata = MetaData()


@as_declarative(metadata=metadata)
class BaseModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    created_at = Column(
        DateTime(timezone=True), index=True, default=datetime.datetime.utcnow()
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=datetime.datetime.utcnow(),
        default=datetime.datetime.utcnow(),
    )

    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return camel_to_snake_formatter(str(cls.__name__))  # pylint: disable=no-member

    @declared_attr
    def __table_args__(cls):
        return {
            "schema": "resources_schema",
        }
