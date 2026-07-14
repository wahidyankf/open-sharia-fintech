"""Example 41: A Subclass Inherits Fields and Methods."""


class Animal:  # => begins the Animal class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => defined ONCE, on the base class


class Cat(Animal):  # => Cat inherits EVERYTHING Animal defines, with no body of its own
    pass  # => an intentionally empty body


c: Cat = Cat(
    "Whiskers"
)  # => Animal.__init__ ran, even though Cat wrote no __init__ itself
print(c.name)  # => the inherited field, set by the inherited __init__
# => Output: Whiskers
# => A subclass with no `__init__` of its own falls back to the nearest ancestor's `__init__` automatically
