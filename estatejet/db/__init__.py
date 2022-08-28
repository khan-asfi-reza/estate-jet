import datetime
from typing import List
from uuid import UUID, uuid4
from tortoise.models import Model as TortoiseModel
from tortoise import fields

from estatejet.config import INSTALLED_APPS


class AbstractModel(TortoiseModel):
    """
    Abstract Model
    """
    uuid = fields.UUIDField(default=uuid4,
                            pk=True,
                            unique=True,
                            index=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class PydanticAbstract:
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime


def get_tortoise_models() -> dict:
    return {
        app.split('.')[-1]: [f"estatejet.{app}.models"] for app in INSTALLED_APPS
    }
