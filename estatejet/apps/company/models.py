import enum

from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy import Column

from estatejet.db import Base, IntegerEnum


class User(Base):
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    country_code = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('phone_number', 'country_code', name='contact_number'),)
