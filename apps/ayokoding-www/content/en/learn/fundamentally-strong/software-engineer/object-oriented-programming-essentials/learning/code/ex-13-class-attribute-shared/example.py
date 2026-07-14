"""Example 13: A Shared Class Attribute."""


class Dog:  # => begins the Dog class body
    species: str = (
        "canine"  # => declared on the CLASS, not inside __init__ -- one shared value
    )

    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => this one IS per-instance


a: Dog = Dog("Rex")  # => constructs a
b: Dog = Dog("Fido")  # => constructs b
print(a.species, b.species)  # => both instances read the SAME class attribute
# => Output: canine canine
# => A field declared in the class body, not inside `__init__`, is a class attribute
