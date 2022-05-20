import typing as t
from sqlalchemy import create_engine, Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

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
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
