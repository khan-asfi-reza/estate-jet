from estatejet.apps.user.models import User
from estatejet.apps.user.schema import UserCreateModel
from test.utils.db import TestDatabase


class TestUserModel(TestDatabase):

    def test_user_create(self):
        user = UserCreateModel(email="email@gmail.com",
                               first_name="First Name",
                               last_name="Last Name",
                               country_code="+12",
                               phone_number="123456",
                               role=1,
                               password="Password")

        self.assertEqual(user.email, "email@gmail.com")
        data = User.create(user)
        self.assertEqual(data.email, "email@gmail.com")
