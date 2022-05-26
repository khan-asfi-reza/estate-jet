import typing as t
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, Query
from datetime import datetime

from estatejet.config.settings import Config

engine = create_engine(
    Config.DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    __name__: str
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class BasePyModel(BaseModel):
    id: int
    created_on: datetime
    updated_on: datetime


class TestDatabase:
    connection = None
    engine = None
    conn_string = None
    session = None

    def db_init(self):
        pass

    def create_session(self):
        self.engine = create_engine(Config.TEST_DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self.session()


TestDatabaseLayer = TestDatabase()

Session = TestDatabaseLayer.create_session()


async def startup():
    global Session
    Session = SessionLocal()


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
