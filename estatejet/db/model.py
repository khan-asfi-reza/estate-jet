from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.orm import Query

from estatejet.db import Base, Database


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


class RequiredDataMissingError(Exception):
    def __init__(self, missing_data):
        super().__init__(f"{missing_data} is required")


class DuplicateDataError(Exception):
    def __init__(self, key, value, table):
        super().__init__(f"Duplicate {key} found, {key}:{value} already exists in table '{table}'")


class Model(Base):
    __abstract__ = True

    @classproperty
    def db(self):
        return Database.session

    @classmethod
    def create(cls, data: BaseModel):
        db_object = cls(**data.dict())
        cls.db.add(db_object)
        cls.db.commit()
        cls.db.refresh(db_object)
        return db_object

    @classmethod
    def update(cls, query: Query, **kwargs) -> Query:
        for field in kwargs:
            setattr(query, field, kwargs[field])
        cls.db.commit()
        return query

    @classmethod
    def get(cls, index: int) -> Query:
        return cls.db.query(cls).filter(cls.id == index).first()

    @classmethod
    def filter(cls, **kwargs) -> Query:
        filter_set = []
        for args in kwargs:
            filter_set.append(getattr(cls, args) == kwargs[args])

        return cls.db.query(cls).filter(*filter_set)

    @classmethod
    def exists(cls, **kwargs) -> bool:
        return cls.filter(**kwargs).first() is not None


class BasePyModel(BaseModel):
    id: int
    created_on: datetime
    updated_on: datetime
