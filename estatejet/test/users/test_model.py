import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

from db import get_tortoise_models
from main import app
from apps.users.models import Users
from config import settings
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture()
def client() -> Generator:
    initializer(get_tortoise_models(), db_url=settings.PYTEST_DATABASE_URL)
    with TestClient(app) as c:
        yield c
    finalizer()


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "email": "admin1@gmail.com",
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "+919092995525",
            "role": "ADMIN",
            "password": "PASSWORD"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "admin1@gmail.com"
    assert "uuid" in data
