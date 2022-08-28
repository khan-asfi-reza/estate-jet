import pytest

from estatejet.apps.company.models import Company, CompanyEmployee
from estatejet.apps.users.models import Users
from tests.fixtures.factories.company import CompanyModelFactory, CompanyEmployeeModelFactory


@pytest.mark.anyio
async def test_company_models():
    await CompanyModelFactory.create_batch(10)
    models = await Company.all()
    assert len(models) == 10


@pytest.mark.anyio
async def test_company_employee_models():
    await CompanyEmployeeModelFactory.create_batch(10)
    models = await CompanyEmployee.all()
    assert len(models) == 10
