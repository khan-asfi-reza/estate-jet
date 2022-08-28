from estatejet.apps.company.models import Company, RoleEnum, CompanyEmployee
from tests.fixtures.factories import TortoiseFactory, Faker, Factory
from tests.fixtures.factories.user_factory import UserModelFactory


class CompanyBaseFactory:
    name = Faker("company")
    license_number = Faker("uuid4", args=[str])


class CompanyModelFactory(CompanyBaseFactory, TortoiseFactory):
    class Meta:
        model = Company


class CompanyEmployeeBaseFactory:
    user = UserModelFactory
    company = CompanyModelFactory
    role = Faker("enum", RoleEnum)


class CompanyEmployeeModelFactory(CompanyEmployeeBaseFactory, TortoiseFactory):
    class Meta:
        model = CompanyEmployee

