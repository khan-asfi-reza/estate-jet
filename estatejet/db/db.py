import typing as t
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from estatejet.config.settings import Config


class DatabaseSessionLayer:
    connection = None
    engine = None
    conn_string = None
    session = None

    def __init__(self, database_url=None):
        if database_url is None:
            database_url = Config.PYTEST_DATABASE_URL

        self.engine = create_engine(database_url)

    def create_session(self):
        Base.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self.session()


class_registry: t.Dict = {}


# Base Class for models and database registry
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


# Base Pydantic Model
class BasePyModel(BaseModel):
    id: int
    created_on: datetime
    updated_on: datetime


# Global Session, Engine
DatabaseLayer = DatabaseSessionLayer()
Session = DatabaseLayer.create_session()
engine = DatabaseLayer.engine


# On App Startup Run This Function
async def startup():
    global Session, DatabaseLayer, engine
    DatabaseLayer = DatabaseSessionLayer(Config.DATABASE_URL)
    Session = DatabaseLayer.create_session()
    engine = DatabaseLayer.engine
