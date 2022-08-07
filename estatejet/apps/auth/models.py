from typing import Optional

from pydantic import BaseModel


class UserDetails(BaseModel):
    uuid: str
    email: str
    first_name: str
    last_name: str
    profile_picture: str
    role: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    user: UserDetails


class TokenData(BaseModel):
    uuid: Optional[str] = None
