from pydantic import BaseModel
from sqlalchemy.orm import Query

from estatejet.db import Base, Session


class Model(Base):
    __abstract__ = True

    @classmethod
    def create(cls, data: BaseModel):
        db_object = cls(**data.dict())
        Session.add(db_object)
        Session.commit()
        Session.refresh(db_object)
        return db_object

    @staticmethod
    def update(query: Query, **kwargs):
        for field in kwargs:
            setattr(query, field, kwargs[field])
        Session.commit()

    @classmethod
    def get(cls, index: int) -> Query:
        return Session.query(cls).filter(cls.id == index).first()

    @classmethod
    def filter(cls, **kwargs) -> Query:
        filter_set = []
        for args in kwargs:
            filter_set.append(getattr(cls, args) == kwargs[args])

        return Session.query(cls).filter(*filter_set)