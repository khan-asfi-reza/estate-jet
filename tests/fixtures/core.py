import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from logging import Logger

from estatejet.config import PYTEST_DATABASE_URL
from estatejet.db import get_tortoise_models
from estatejet.main import app

DB_URL = PYTEST_DATABASE_URL

logger = Logger(__name__)


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules=get_tortoise_models(), _create_db=create_db
    )
    if create_db:
        logger.info(f"Database created! {db_url = }", )
    if schemas:
        await Tortoise.generate_schemas()
        logger.info("Success to generate schemas")


async def init(db_url: str = DB_URL):
    """
    Initialize Database
    """
    await init_db(db_url, True, True)


@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        logger.info("Client is ready")
        yield client


@pytest.fixture(scope="function", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()
