from estatejet.apps.users.models import Users, RoleEnum
from tests.fixtures.factories import TortoiseFactory, Faker, FixtureFactory


class UserBaseFactory:
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = Faker("password")
    profile_picture = Faker("url")
    phone_number = Faker("phone_number")
    role = Faker("enum", RoleEnum)
    is_verified = Faker("boolean")


class UserModelFactory(UserBaseFactory, TortoiseFactory):
    class Meta:
        model = Users

    def create_method(self):
        return Users.create_and_save_password


class UserData(UserBaseFactory, FixtureFactory):
    """
    User Data Model
    """
    exclude = ["is_verified", ]
