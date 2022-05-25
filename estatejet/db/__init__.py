from .db import *
from sqlalchemy import TypeDecorator, Enum


class IntegerEnum(TypeDecorator):
    impl = db.Integer()

    @property
    def python_type(self):
        return int

    def process_literal_param(self, value, dialect):
        return super(self).process_literal_param(self, value, dialect)

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, Enum):
            return value
        elif isinstance(value, int):
            return value
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)
