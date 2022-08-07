from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from tortoise.queryset import QuerySetSingle

from estatejet.apps.auth.models import TokenData
from estatejet.apps.users.models import Users
from estatejet.config import OAuth2Scheme, SECRET_KEY, ALGORITHM, REFRESH_KEY


async def auth_user(token: str = Depends(OAuth2Scheme)) -> Users:
    """

    Args:
        token: Token | bearer Token

    Returns: QuerySetSingle[Users]

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uuid: str = payload.get("sub")
        if uuid is None:
            raise credentials_exception
        token_data = TokenData(uuid=uuid)
    except JWTError:
        raise credentials_exception
    user = await Users.get_or_none(uuid=token_data.uuid)
    if user is None:
        raise credentials_exception
    return user


async def refresh_token_user(token: str) -> Users:
    """

    Args:
        token: str

    Returns: User

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, REFRESH_KEY, algorithms=[ALGORITHM])
        uuid: str = payload.get("sub")
        if uuid is None:
            raise credentials_exception
        token_data = TokenData(uuid=uuid)
    except JWTError:
        raise credentials_exception
    user = await Users.get_or_none(uuid=token_data.uuid)
    if user is None:
        raise credentials_exception
    return user
