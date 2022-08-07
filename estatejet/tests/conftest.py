import asyncio

import pytest
from starlette.testclient import TestClient
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError, OperationalError

from db import get_tortoise_models
from estatejet.main import app


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = "sqlite://memory"

    async def _init_db() -> None:
        await Tortoise.init(db_url=db_url, modules={"modules": get_tortoise_models()})
        try:
            await Tortoise._drop_databases()
        except (DBConnectionError, OperationalError):  # pragma: nocoverage
            pass

        await Tortoise.init(db_url=db_url, modules={"modules": get_tortoise_models()}, _create_db=True)
        await Tortoise.generate_schemas(safe=False)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_init_db())

    request.addfinalizer(lambda: loop.run_until_complete(Tortoise._drop_databases()))


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
