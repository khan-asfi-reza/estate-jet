from enum import Enum

from tortoise import fields

from estatejet.db import AbstractModel


class Company(AbstractModel):
    """
    Real Estate Company
    """
    name = fields.CharField(max_length=256)
    license_number = fields.CharField(max_length=512)
    number_of_employees = fields.IntField(default=0)


class RoleEnum(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    TEAM_LEADER = "TEAM_LEADER"
    AGENT = "AGENT"


class CompanyEmployee(AbstractModel):
    """
    Company User Relation Mapping
    """
    user = fields.OneToOneField('users.Users', on_delete=fields.CASCADE)
    company = fields.ForeignKeyField('company.Company', on_delete=fields.CASCADE)
    role = fields.CharEnumField(enum_type=RoleEnum, default=RoleEnum.AGENT)

    def is_admin(self) -> bool:
        """

        Returns: bool, checks if user is admin

        """
        return self.role == RoleEnum.ADMIN

