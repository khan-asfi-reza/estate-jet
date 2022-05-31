from estatejet.apps.user.models import User
from estatejet.apps.user.schema import UserCreateModel
from estatejet.db.model import DuplicateDataError
from test.utils.db import TestDatabase


class TestUserModel(TestDatabase):

    @staticmethod
    def user_details():
        return UserCreateModel(email="email@gmail.com",
                               first_name="First Name",
                               last_name="Last Name",
                               country_code="+12",
                               phone_number="123456",
                               role=1,
                               password="Password")

    def test_user_create(self):
        user = self.user_details()

        data = User.save(user)
        self.assertEqual(data.email, "email@gmail.com")
        self.assertNotEqual(data.password, "Password")

    def test_duplicate(self):
        try:
            user = self.user_details()
            User.save(user)
        except Exception as e:
            self.assertIs(e, DuplicateDataError)
