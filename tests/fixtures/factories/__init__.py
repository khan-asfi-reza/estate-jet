import inspect
from typing import TypeAlias, Type, Union, Optional
from uuid import uuid4

import inflection as inflection
import pytest
from faker import Faker as PytestFaker
from tortoise import Model


class Faker:
    fake = PytestFaker()

    def __init__(self, key=None, value=None, args=None):
        """
        Call
        """
        if not args:
            args = []
        self.args = args
        self.provider = None
        self.value = value

        if key == "phone_number":
            self.value = self.fake_phone_number()

        elif key == "enum":
            self.value = self.fake.random_choices(list(self.value))[0].value

        elif key == "password":
            self.value = uuid4().hex

        elif key:
            self.provider = getattr(self.fake, key)

    def fake_phone_number(self):
        return ("+"
                f"{self.fake.random_number(3)}"
                f"{self.fake.random_number(4)}"
                f"{self.fake.random_number(4)}"
                f"{self.fake.random_number(4)}")

    def generate(self):
        """
        Returns: generated Value
        """
        if self.provider:
            return self.provider(*self.args)
        return self.value


IGNORE_ATTRS = ["Meta", "Data", "exclude", "attributes", "object_set"]


class Factory:
    exclude = []
    object_set = False

    class Data:
        """
        Data Structure for Model Data
        """

        def __init__(self, **entries):
            self.__dict__.update(entries)

    def __init__(self):
        self.attributes: Optional[dict] = None

    async def set_attributes(self):
        self.attributes = await self.__get_attributes()

    async def __get_attributes(self):
        """
        Get model attributes
        """
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        attribute_value = [a for a in attributes if (
                not (
                        a[0].startswith('__')
                        and a[0].endswith('__'))
                and a[0] not in IGNORE_ATTRS
                and a[0] not in self.exclude
        )
                           ]
        attrs = {}
        for x, y in attribute_value:
            if type(y) is Faker:
                y = y.generate()
            elif issubclass(y, TortoiseFactory):
                factory = await create_factory(y)
                y = await factory.create_object()
            setattr(self, x, y)
            attrs.update({f"{x}": y})
        self.object_set = True
        return attrs

    def get_dict(self) -> dict:
        """
        Get raw data as dictionary
        Returns: dict
        """
        if not self.attributes:
            return {}
        data = {}
        for key, attr in self.attributes.items():
            if type(attr) is Factory:
                data.update(
                    {
                        key: attr.get_dict()
                    }
                )
            else:
                data.update({key: attr})
        return data

    def get_data(self) -> Data:
        """
        Get data as Data Class
        Returns: Data
        """
        data = self.get_dict()
        return self.Data(**data)


class FixtureFactory(Factory):
    """
    Pydantic Model Factory
    """


class TortoiseFactory(Factory):
    class Meta:
        """
        Meta Class for Factory where the model is contained
        """
        model: Model = None

    def create_method(self):
        """
        Model Create Method
        Returns: Callable
        """
        return self.Meta.model.create

    async def create_object(self):
        """
        Create Singular Object
        """
        if not self.object_set:
            await self.set_attributes()
        args = self.attributes
        obj = await self.create_method()(**args)
        setattr(obj, "get_data", self.get_data)
        setattr(obj, "get_dict", self.get_dict)
        return obj

    @classmethod
    async def create_batch(cls, number):
        """
        Create multiple batches of object
        """
        return [await cls().create_object() for i in range(number)]


FactoryType: TypeAlias = Type[TortoiseFactory]
DataFactoryType: TypeAlias = Type[FixtureFactory]


async def create_factory(factory: Union[FactoryType, DataFactoryType]):
    fact = factory()
    await fact.set_attributes()
    return fact


def register_model_factory(factory_class: FactoryType, name=""):
    if not name:
        name = inflection.underscore(factory_class.Meta.model.__name__)

    assert factory_class.Meta.model is not None, "Invalid Factory"

    @pytest.mark.anyio
    @pytest.fixture(name=name)
    async def fn():
        fact = await create_factory(factory_class)
        obj = await fact.create_object()
        return obj

    return fn, name


def register_data_factory(factory_class: DataFactoryType, name=""):
    if not name:
        name = inflection.underscore(factory_class.__name__)

    @pytest.mark.anyio
    @pytest.fixture(name=name)
    async def fn():
        fact = await create_factory(factory_class)
        return fact

    return fn, name
