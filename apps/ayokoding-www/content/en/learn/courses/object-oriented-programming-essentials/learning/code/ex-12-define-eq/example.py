"""Example 12: Define __eq__ for Value Comparison."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance

    def __eq__(
        self, other: object
    ) -> bool:  # => other is `object`, not Dog -- must narrow it
        if not isinstance(
            other, Dog
        ):  # => guards against comparing a Dog to an unrelated type
            return NotImplemented  # => lets Python try the other object's __eq__ next
        return self.name == other.name  # => value equality: same name means equal dogs


a: Dog = Dog("Rex")  # => constructs a
b: Dog = Dog("Rex")  # => a different object, but the same name
print(a == b)  # => now == compares VALUES, not identity
# => Output: True
# => `__eq__` should `isinstance`-check `other` first and return `NotImplemented` for unrelated types
