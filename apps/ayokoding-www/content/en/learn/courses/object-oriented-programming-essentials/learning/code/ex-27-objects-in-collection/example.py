"""Example 27: Objects in a Collection."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance


dogs: list[Dog] = [
    Dog("Rex"),
    Dog("Fido"),
    Dog("Max"),
]  # => three independent Dog instances
names: list[str] = [
    dog.name for dog in dogs
]  # => iteration yields each object, in order
print(names)  # => confirms the iteration order matches construction order
# => Output: ['Rex', 'Fido', 'Max']
# => `list[Dog]` is a list of objects like any other
