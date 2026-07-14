"""Example 49: A classmethod Factory Returns the Subclass Type."""

from typing import TypeVar  # => imports TypeVar from typing

# => bound="Animal" ties T to Animal or any of its subclasses
T = TypeVar(
    "T", bound="Animal"
)  # => T stands for "whatever concrete subclass calls create()"


class Animal:  # => begins the Animal class body
    @classmethod  # => marks the next method as receiving cls, not self
    def create(
        cls: type[T],
    ) -> T:  # => cls: type[T] lets the return type track the CALLING class
        return cls()  # => NOT "return Animal()" -- cls() adapts to the calling subclass


class Cat(Animal):  # => Cat extends Animal
    pass  # => an intentionally empty body


a: Animal = Animal.create()  # => cls is Animal here, so T resolves to Animal
c: Cat = Cat.create()  # => cls is Cat here -- the SAME method body, T resolves to Cat
print(type(a).__name__, type(c).__name__)  # => each call returned its OWN calling class
# => Output: Animal Cat
# => `cls()` inside a `@classmethod` resolves to whatever class the method was called through
