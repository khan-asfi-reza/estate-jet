from enum import Enum
from uuid import uuid4

from tortoise import fields
from tortoise.models import Model


class Company(Model):
    """
    Real Estate Company
    """
    uuid = fields.UUIDField(default=uuid4, pk=True, unique=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    name = fields.CharField(max_length=256)
    admin = fields.OneToOneField('model.Users', on_delete=fields.SET_NULL, null=True)
    license_number = fields.CharField(max_length=512)


class RoleEnum(str, Enum):
    TEAM_LEADER = "TEAM_LEADER"
    MANAGER = "MANAGER"
    OWNER = "OWNER"
    AGENT = "AGENT"


class CompanyRepresentative(Model):
    """
    Company User Relation Mapping
    """
    uuid = fields.UUIDField(default=uuid4, pk=True, unique=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.OneToOneField('model.Users', on_delete=fields.CASCADE)
    company = fields.ForeignKeyField('model.Company', on_delete=fields.CASCADE)
    role = fields.CharEnumField(enum_type=RoleEnum, default=RoleEnum.AGENT)
