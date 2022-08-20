import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from estatejet.apps.users.models import Users
from tests.fixtures.factories.user_factory import UserFactory


@pytest.mark.anyio
async def test_user_factory_model_batch():
    await UserFactory.create_batch(10)
    models = await Users.all()
    assert len(models) == 10


@pytest.mark.anyio
async def test_user_factory(users):
    models = await Users.all()
    assert len(models) == 1


@pytest.mark.anyio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users/",
        json={
            "email": "admin@gmail.com",
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "+919092995525",
            "role": "ADMIN",
            "password": "PASSWORD"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "admin@gmail.com"
    assert "uuid" in data
