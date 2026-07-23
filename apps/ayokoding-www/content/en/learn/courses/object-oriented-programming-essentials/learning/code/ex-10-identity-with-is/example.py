"""Example 10: Identity with is."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance


a: Dog = Dog("Rex")  # => constructs exactly one Dog object
b: Dog = a  # => b is a NEW NAME for the SAME object -- no new Dog is constructed here
print(a is b)  # => is compares OBJECT IDENTITY, not field values
# => Output: True
# => `b = a` creates a second name for the same object, not a copy
