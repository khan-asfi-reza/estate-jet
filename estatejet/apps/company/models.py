from sqlalchemy import Column
from sqlalchemy import String, UniqueConstraint

from estatejet.db.model import Model


class Company(Model):
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    country_code = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('phone_number', 'country_code', name='contact_number'),)
