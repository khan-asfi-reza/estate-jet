from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Query

from estatejet.db import Base, Database


class Model(Base):
    __abstract__ = True
    db = Database.session

    @classmethod
    def create(cls, data: BaseModel):
        db_object = cls(**data.dict())
        cls.db.add(db_object)
        cls.db.commit()
        cls.db.refresh(db_object)
        return db_object

    @classmethod
    def update(cls, query: Query, **kwargs):
        for field in kwargs:
            setattr(query, field, kwargs[field])
        cls.db.commit()

    @classmethod
    def get(cls, index: int) -> Query:
        return cls.db.query(cls).filter(cls.id == index).first()

    @classmethod
    def filter(cls, **kwargs) -> Query:
        filter_set = []
        for args in kwargs:
            filter_set.append(getattr(cls, args) == kwargs[args])

        return cls.db.query(cls).filter(*filter_set)


class BasePyModel(BaseModel):
    id: int
    created_on: datetime
    updated_on: datetime