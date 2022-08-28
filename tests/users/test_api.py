from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

from tests.fixtures.factories.user_factory import UserData


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
