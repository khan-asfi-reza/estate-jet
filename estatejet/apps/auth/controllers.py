from datetime import timedelta

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from estatejet.apps.auth.helpers import authenticate_user, create_access_token, create_refresh_token
from estatejet.apps.auth.middleware import refresh_token_user
from estatejet.apps.auth.models import Token
from estatejet.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix='/auth',
)


class FormData(BaseModel):
    email: str
    password: str


@router.post("/token", response_model=Token)
async def login(form_data: FormData):
    """
    User Login returns access token and refresh token
    """
    user = await authenticate_user(
        form_data.email, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.uuid)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.uuid)},
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "uuid": str(user.uuid),
            "profile_picture": user.profile_picture,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
    }


class RefreshTokenModel(BaseModel):
    refresh_token: str


@router.post('/refresh', response_model=Token)
async def refresh(body: RefreshTokenModel):
    """
    Returns `AccessToken` from refresh token
    """
    user = await refresh_token_user(body.refresh_token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.uuid)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.uuid)},
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "uuid": str(user.uuid),
            "profile_picture": user.profile_picture,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
    }
