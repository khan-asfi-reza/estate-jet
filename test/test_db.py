from estatejet.apps.user.models import User
from estatejet.apps.user.schema import UserCreateModel
from test.utils.db import TestDatabase


class TestUserModel(TestDatabase):

    def test_user_create(self):
        data = self.connection.execute("SELECT 1")
        self.assertIsNotNone(data)
