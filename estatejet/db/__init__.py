from typing import List
from uuid import uuid4

from tortoise.models import Model as TortoiseModel
from tortoise import fields

from estatejet.config import INSTALLED_APPS


class Model(TortoiseModel):
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


def get_tortoise_models() -> List:
    return [
        f"estatejet.{app}.models" for app in INSTALLED_APPS
    ]
