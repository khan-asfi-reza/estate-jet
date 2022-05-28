from unittest import TestCase

from sqlalchemy.exc import InternalError

from estatejet.db import Base, Database


class TestDatabase(TestCase):

    @staticmethod
    def clear_db(session):
        try:
            meta = Base.metadata
            for table in reversed(meta.sorted_tables):
                session.execute(table.delete())
            session.commit()
        except InternalError:
            pass

    def setUp(self) -> None:
        self.session = Database.session
        self.connection = Database.connection
        self.clear_db(self.session)

    def tearDown(self) -> None:
        self.clear_db(self.session)
