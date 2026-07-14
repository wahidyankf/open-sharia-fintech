"""Example 3: Define an Instance Method."""


class Dog:  # => begins the Dog class body
    def __init__(
        self, name: str
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => per-instance state, unrelated to the method below

    def bark(
        self,
    ) -> str:  # => an instance method: self is bound automatically on d.bark()
        return "woof"  # => a method body is ordinary Python code, same as any function


d: Dog = Dog("Rex")  # => constructs d
print(
    d.bark()
)  # => d.bark() implicitly passes d as self -- no argument needed at the call site
# => Output: woof
# => `d.bark()` and `def bark(self)` are two halves of the same mechanism: the dot-call syntax implicitly supplies `self`
