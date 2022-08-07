from datetime import datetime, timedelta
from typing import Optional, Union

from jose import jwt

from estatejet.apps.users.models import Users
from estatejet.config import PasswordContext, SECRET_KEY, ALGORITHM, REFRESH_KEY


def verify_password(plain_password, hashed_password) -> bool:
    """
    Verifies Password
    Args:
        plain_password: str
        hashed_password: str

    Returns: bool | Checks if password is valid

    """
    return PasswordContext.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str) -> Union[Users, bool]:
    """

    Args:
        email: str | Email address
        password: str | User Password

    Returns:

    """
    user = await Users.get_or_none(email=email).only(
        'uuid', 'email', 'first_name', 'last_name', 'role', 'profile_picture', 'password'
    )
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create Access Token for User
    Args:
        data: dict
        expires_delta: Optional[timedelta]

    Returns: token

    """
    to_encode = data.copy()
    to_encode["token_type"] = "access_token"
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create Refresh Token for User
    Args:
        data: dict

    Returns: token

    """
    to_encode = data.copy()
    to_encode["token_type"] = "refresh_token"
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt
