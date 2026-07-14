"""Example 28: self Is Just an Explicit First Argument."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance

    def bark(
        self,
    ) -> str:  # => self here is the SAME parameter Dog.bark(d) passes explicitly
        return f"{self.name} says woof"  # => returns this value to the caller


d: Dog = Dog("Rex")  # => constructs d
via_instance: str = (
    d.bark()
)  # => the familiar dot-call syntax -- self is bound implicitly
via_class: str = Dog.bark(
    d
)  # => the SAME call, with self passed explicitly as an argument
print(via_instance == via_class)  # => both forms are exactly equivalent
# => Output: True
# => `self` is not magic
