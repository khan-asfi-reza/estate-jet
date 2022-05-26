from unittest import TestCase

from estatejet.db import Base, TestDatabaseLayer, Session


class TestDatabase(TestCase):

    @staticmethod
    def clear_db(session):
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    def setUp(self) -> None:
        self.session = Session
        self.clear_db(self.session)

    def tearDown(self) -> None:
        self.clear_db(self.session)