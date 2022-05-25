from pydantic import BaseModel


class UserItemBase(BaseModel):
    name: str
    description: str


class UserItem(UserItemBase):
    class Config:
        orm_mode = True
