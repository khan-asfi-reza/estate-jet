from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str


class Item(ItemBase):
    class Config:
        orm_mode = True
