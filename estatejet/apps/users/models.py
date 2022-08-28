import re
from enum import Enum

import tortoise.exceptions
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import ValidationError

from estatejet.apps.users.helpers import get_password_hash
from estatejet.db import AbstractModel


def validate_email(email: str):
    """
    Validates a given email

    Args:
        email: Email

    Raises:
        ValidationError

    """

    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        raise ValidationError("Invalid Email")


def validate_phone_number(phone_number: str):
    """
    Validates a given phone_number

    Args:
        phone_number: phone_number

    Raises:
        ValidationError

    """

    if not re.match("^\\+?[1-9][0-9]{7,14}$", phone_number):
        raise ValidationError("Invalid Phone Number")


class RoleEnum(str, Enum):
    AGENT = "AGENT"
    CLIENT = "CLIENT"
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    STAFF = "STAFF"


class Users(AbstractModel):
    """
    The User model
    """
    email = fields.CharField(max_length=32, unique=True, validators=[validate_email])
    first_name = fields.CharField(max_length=255, null=False)
    last_name = fields.CharField(max_length=255, null=False)
    password = fields.CharField(max_length=128, null=True, required=False, )
    profile_picture = fields.CharField(max_length=512, null=True, required=False, )
    phone_number = fields.CharField(max_length=32, validators=[validate_phone_number], required=False, )
    role = fields.CharEnumField(enum_type=RoleEnum, default=RoleEnum.CLIENT)
    is_verified = fields.BooleanField(default=False, required=False, )

    def full_name(self) -> str:
        return f"{self.first_name} {self.full_name}"

    class PydanticMeta:
        exclude = ['is_verified']

    @classmethod
    async def create_and_save_password(cls, **user_data):
        """
        Saves User and Saves Password
        Args:
            **user_data: Dict of user's data

        Returns:
        """
        password = user_data.pop('password', None)
        if not password:
            raise tortoise.exceptions.ValidationError("Invalid Password")
        user = await cls.create(**user_data)
        user.password = get_password_hash(password)
        await user.save()
        return user


UserPydantic = pydantic_model_creator(Users, name="User", exclude=('password',))

UserInPydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True, )
