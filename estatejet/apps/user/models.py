from __future__ import annotations

import enum

from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import String, UniqueConstraint

from estatejet.apps.user.schema import UserCreateModel
from estatejet.config import PasswordContext
from estatejet.db import IntegerEnum
from estatejet.db.model import Model, RequiredDataMissingError, DuplicateDataError


# Roles For User
class UserRoleEnum(enum.Enum):
    admin = 1
    client = 2
    host = 3
    agent = 4


# User Model
class User(Model):
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    role = Column(IntegerEnum(UserRoleEnum), nullable=False)
    password = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('phone_number', 'country_code', name='contact_number'),)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return PasswordContext.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return PasswordContext.hash(password)

    @classmethod
    def create(cls, data: BaseModel):
        return super().create(data)

    @classmethod
    def save(cls, data: UserCreateModel) -> User:
        email = data.email
        if not email:
            raise RequiredDataMissingError("Email missing")

        if cls.exists(email=email):
            raise DuplicateDataError("Email", email, "user")

        data.password = cls.get_password_hash(data.password)

        return cls.create(data)


# class CompanyUserRoleEnum(enum.Enum):
#     company_admin = 1
#     agent = 4
#
#
# class UserCompany(Base):
#     user = Column(Integer, ForeignKey("user.id"))
#     company = Column(Integer, ForeignKey("company.id"))
#     company_role = Column(IntegerEnum(CompanyUserRoleEnum), nullable=False)
