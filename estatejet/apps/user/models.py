import enum

from sqlalchemy import Column
from sqlalchemy import String, UniqueConstraint

from estatejet.db import IntegerEnum
from estatejet.db.model import Model


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

    def save(self, **kwargs):
        """
        TODO: Encrypt password
        :param kwargs:
        :return:
        """

# class CompanyUserRoleEnum(enum.Enum):
#     company_admin = 1
#     agent = 4
#
#
# class UserCompany(Base):
#     user = Column(Integer, ForeignKey("user.id"))
#     company = Column(Integer, ForeignKey("company.id"))
#     company_role = Column(IntegerEnum(CompanyUserRoleEnum), nullable=False)
