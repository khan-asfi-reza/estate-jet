import typing as t
from sqlalchemy import create_engine, Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from estatejet.config.settings import Config

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


class DatabaseSessionLayer:
    connection = None
    engine = None
    conn_string = None
    session = None

    # Creates Engine
    def create_engine(self, database_url=None):
        if database_url is None:
            database_url = Config.TEST_DATABASE_URL

        self.engine = create_engine(database_url)

    # Creates all tables and schemas
    def create_metadata(self):
        Base.metadata.create_all(self.engine)

    # Create a database connection
    def create_connection(self):
        self.connection = self.engine.connect()

    # Initialize a session
    def create_session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    # Initialize a session
    def init_session(self):
        session = self.create_session()
        try:
            yield session()
        finally:
            session().close()

    # Gets a session
    def get_session(self):
        return next(self.init_session())

    # Initialize Connection and session along with engine
    def __init__(self, database_url=None):
        self.create_engine(database_url)
        self.create_connection()
        self.session = self.get_session()


# Global Session, Engine
Database = DatabaseSessionLayer()


# On App Startup Run This Function
async def startup():
    global Database
    Database = DatabaseSessionLayer(Config.DATABASE_URL)
    Database.create_metadata()
