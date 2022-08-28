import pytest

from estatejet.apps.auth.helpers import verify_password
from estatejet.apps.users.models import Users
from tests.fixtures.factories.user_factory import UserModelFactory


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

