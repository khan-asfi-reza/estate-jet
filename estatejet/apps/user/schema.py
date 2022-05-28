from pydantic import BaseModel

from estatejet.db.model import BasePyModel


class UserBaseModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone_number: str
    country_code: str
    role: int
    password: str


class UserRetrieveModel(BasePyModel, UserBaseModel):
    pass


class UserCreateModel(UserBaseModel):
    pass
