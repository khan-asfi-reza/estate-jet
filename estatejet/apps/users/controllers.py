import tortoise.exceptions
from fastapi import APIRouter, HTTPException, status

from estatejet.apps.users.models import UserPydantic, UserInPydantic, Users

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('/', response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    try:
        user_obj = await Users.create_and_save_password(
            **user.dict(exclude_unset=True)
        )
        return await UserPydantic.from_tortoise_orm(
            user_obj
        )
    except tortoise.exceptions.ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e.__str__()}",
        )
