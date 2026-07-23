"""Example 11: Default Equality Falls Back to Identity."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = (
            name  # => no __eq__ defined -- Python uses object's default comparison
        )


a: Dog = Dog("Rex")  # => first, independent object
b: Dog = Dog("Rex")  # => second, independent object with the SAME name value
print(
    a == b
)  # => without __eq__, == falls back to `is` -- identical VALUES, different OBJECTS
# => Output: False
# => A class with no `__eq__` compares by identity even if `==` is the operator written
