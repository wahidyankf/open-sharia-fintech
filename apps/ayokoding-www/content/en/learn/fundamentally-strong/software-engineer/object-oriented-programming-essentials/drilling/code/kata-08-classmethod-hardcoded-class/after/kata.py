"""Kata 8 (after): cls() adapts to whichever class create() was actually called on."""

from typing import TypeVar

T = TypeVar("T", bound="Animal")


class Animal:
    @classmethod
    def create(cls: type[T]) -> T:
        return cls()  # adapts to the CALLING class


class Cat(Animal):
    pass


c = Cat.create()
print(type(c).__name__)
