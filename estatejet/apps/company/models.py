from enum import Enum

from tortoise import fields

from estatejet.db import AbstractModel


class Company(AbstractModel):
    """
    Real Estate Company
    """
    name = fields.CharField(max_length=256)
    admin = fields.OneToOneField('model.Users', on_delete=fields.SET_NULL, null=True)
    license_number = fields.CharField(max_length=512)


class RoleEnum(str, Enum):
    TEAM_LEADER = "TEAM_LEADER"
    MANAGER = "MANAGER"
    OWNER = "OWNER"
    AGENT = "AGENT"


class CompanyEmployee(AbstractModel):
    """
    Company User Relation Mapping
    """
    user = fields.OneToOneField('model.Users', on_delete=fields.CASCADE)
    company = fields.ForeignKeyField('model.Company', on_delete=fields.CASCADE)
    role = fields.CharEnumField(enum_type=RoleEnum, default=RoleEnum.AGENT)
