"""Example 14: An Instance Attribute Shadows the Class Attribute."""


class Dog:  # => begins the Dog class body
    species: str = "canine"  # => the shared default every instance starts out reading

    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance


a: Dog = Dog("Rex")  # => constructs a
b: Dog = Dog("Fido")  # => constructs b
a.species = (
    "wolf"  # => creates a NEW instance attribute on a, shadowing the class attribute
)
# => this does NOT touch Dog.species or b.species at all
print(
    a.species, b.species
)  # => a now reads its own shadow; b still reads the class value
# => Output: wolf canine
# => `a.species = "wolf"` never mutates `Dog.species`
