class Another:
    value: str

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Parent:
    val: Another

    def __init__(self, obj: Another):
        self.val = obj

    def reset(self, obj: Another):
        self.val = obj


A = Parent(Another("Item 1"))

B = A.val

print(B)

A.reset(Another("Item 2"))

print(B)