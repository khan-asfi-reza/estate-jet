import inspect
from typing import TypeAlias, Type

import inflection as inflection
import pytest
from faker import Faker as PytestFaker
from tortoise import Model


class Faker:
    fake = PytestFaker()

    def __init__(self, key=None, value=None):
        """
        Call
        """
        self.provider = None
        self.value = value
        if key:
            self.provider = getattr(self.fake, key)

        if key == "phone_number":
            self.provider = None
            self.value = self.fake_phone_number()

    def fake_phone_number(self):
        return (
            "+"
            f"{self.fake.random_number(3)}"
            f"{self.fake.random_number(4)}"
            f"{self.fake.random_number(4)}"
            f"{self.fake.random_number(4)}"
        )

    def generate(self):
        """
        Returns: generated Value
        """
        if self.provider:
            return self.provider()
        return self.value


class TortoiseFactory:
    class Data:
        """
        Data Structure for Model Data
        """

        def __init__(self, **entries):
            self.__dict__.update(entries)

    class Meta:
        """
        Meta Class for Factory where the model is contained
        """
        model: Model = None

    def __get_attributes(self):
        """
        Get model attributes
        """
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        attribute_value = [a for a in attributes if (
                not (a[0].startswith('__') and a[0].endswith('__')) and a[0] != "Meta"
        )]
        attrs = {}
        for x, y in attribute_value:
            if type(y) is Faker:
                y = y.generate()
            attrs.update({
                f"{x}": y
            })
        return attrs

    async def create_object(self):
        """
        Create Singular Object
        """
        args = self.__get_attributes()
        return await self.create_method()(**args)

    def get_dict(self) -> dict:
        """
        Get raw data as dictionary
        Returns: dict
        """
        return self.__get_attributes()

    def get_data(self) -> Data:
        """
        Get data as Data Class
        Returns: Data
        """
        return self.Data(**self.__get_attributes())

    def create_method(self):
        """
        Model Create Method
        Returns: Callable
        """
        return self.Meta.model.create

    @classmethod
    async def create_batch(cls, number):
        """
        Create multiple batches of object
        """
        return [
            await cls().create_object() for i in range(number)
        ]


FactoryType: TypeAlias = Type[TortoiseFactory]


def register(factory_class: FactoryType, name=""):
    if not name:
        name = inflection.underscore(factory_class.Meta.model.__name__)

    assert factory_class.Meta.model is not None, "Invalid Factory"

    @pytest.mark.anyio
    @pytest.fixture(name=name)
    async def fn(*args, **kwargs):
        fact = factory_class()
        obj = await fact.create_object()
        return obj

    return fn, name
