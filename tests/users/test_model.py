import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from estatejet.apps.auth.helpers import verify_password
from estatejet.apps.users.models import Users
from tests.fixtures.factories.user_factory import UserModelFactory, UserData


@pytest.mark.anyio
async def test_user_factory_model_batch():
    await UserModelFactory.create_batch(10)
    models = await Users.all()
    assert len(models) == 10


@pytest.mark.anyio
async def test_user_factory(users):
    models = await Users.all()
    assert len(models) == 1


@pytest.mark.anyio
async def test_user_data(users):
    raw_data = users.get_data()
    assert users.password != raw_data.password
    assert verify_password(raw_data.password, users.password)


@pytest.mark.anyio
async def test_create_user(client: AsyncClient, user_data: UserData):
    response = await client.post(
        "/users/",
        json=user_data.get_dict()
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == user_data.email
    assert "uuid" in data


@pytest.mark.anyio
async def test_user_duplicate_data_error(client: AsyncClient, user_data: UserData):
    await test_create_user(
        client, user_data
    )
    response = await client.post(
        "/users/",
        json=user_data.get_dict()
    )
    assert response.status_code == 422
