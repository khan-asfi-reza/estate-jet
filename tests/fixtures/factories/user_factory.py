from estatejet.apps.users.models import Users
from tests.fixtures.factories import TortoiseFactory, Faker, register


class UserFactory(TortoiseFactory):
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = "fake_test_password"
    profile_picture = Faker("url")
    phone_number = Faker("phone_number")
    role = "ADMIN"
    is_verified = Faker("boolean")

    class Meta:
        model = Users

    def create_method(self):
        return Users.create_and_save_password
