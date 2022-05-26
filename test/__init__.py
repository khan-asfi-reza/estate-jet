class Parent:

    @classmethod
    def create(cls):
        print(cls.__name__)


class Child(Parent):

    def __str__(self):
        return "Childdds"


Child().create()
