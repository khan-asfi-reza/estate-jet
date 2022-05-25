from sqlalchemy import String, Integer
from sqlalchemy import Column

from estatejet.db import Base


class UserItem(Base):
    name = Column(String)
    description = Column(String)
