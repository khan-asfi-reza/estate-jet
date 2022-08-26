from tests.fixtures.factories import TortoiseFactory, FixtureFactory, Faker
from estatejet.apps.company.models import Company, CompanyEmployee


class CompanyFactory(TortoiseFactory):
    name = Faker("company")

    class Meta:
        model = Company
