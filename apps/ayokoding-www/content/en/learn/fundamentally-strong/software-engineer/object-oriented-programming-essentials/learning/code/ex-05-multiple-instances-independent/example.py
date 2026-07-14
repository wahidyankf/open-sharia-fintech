"""Example 5: Multiple Instances Stay Independent."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => each Dog() call creates a SEPARATE self.name binding


rex: Dog = Dog("Rex")  # => first instance, its own name attribute
fido: Dog = Dog("Fido")  # => second instance, a completely different name attribute
print(rex.name, fido.name)  # => neither instance's name leaked into the other
# => Output: Rex Fido
# => Instance attributes set inside `__init__` are per-object by default
