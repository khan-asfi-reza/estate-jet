import enum

from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy import Column, ForeignKey

from estatejet.db import Base, IntegerEnum


class UserRoleEnum(enum.Enum):
    admin = 1
    client = 2
    host = 3
    agent = 4


class User(Base):
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    role = Column(IntegerEnum(UserRoleEnum), nullable=False)
    password = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('phone_number', 'country_code', name='contact_number'),)


class CompanyUserRoleEnum(enum.Enum):
    company_admin = 1
    agent = 4


class UserCompany(Base):
    user = Column(Integer, ForeignKey("user.id"))
    company = Column(Integer, ForeignKey("company.id"))
    company_role = Column(IntegerEnum(CompanyUserRoleEnum), nullable=False)
