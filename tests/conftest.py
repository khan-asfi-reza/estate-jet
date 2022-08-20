import inspect
import os
import pkgutil
from importlib import import_module

from pathlib import Path

from tests.fixtures.factories import TortoiseFactory, register

PATH = Path(__file__).resolve().parent


def find_fixture_modules():
    """
    Finds fixtures located in the fixtures directory
    """
    modules = [
        "tests.fixtures.{}".format(name)
        for _, name, is_pkg in pkgutil.iter_modules([os.path.join(PATH, "fixtures")])
        if not is_pkg and not name.startswith("_") and name != "factories"
    ]

    return modules


pytest_plugins = find_fixture_modules()

factories = [
    "tests.fixtures.factories.{}".format(name)
    for _, name, is_pkg in pkgutil.iter_modules(
        [os.path.join(PATH, "fixtures", "factories")]
    )
    if not is_pkg and not name.startswith("_")
]

model_factories = []

for factory in factories:
    module = import_module(factory)
    for cls in inspect.getmembers(module, inspect.isclass):
        klass = cls[1]
        if issubclass(klass, TortoiseFactory) and klass is not TortoiseFactory:
            func, name = register(klass)
            globals()[name] = func
