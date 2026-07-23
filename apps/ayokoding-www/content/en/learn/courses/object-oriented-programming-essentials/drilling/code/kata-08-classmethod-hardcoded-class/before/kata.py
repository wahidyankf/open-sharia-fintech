"""Kata 8 (before): a classmethod factory hardcodes the base class name."""


class Animal:
    @classmethod
    def create(cls) -> "Animal":
        return (
            Animal()
        )  # hardcoded -- ignores whichever class create() was actually called on


class Cat(Animal):
    pass


c = Cat.create()
print(type(c).__name__)
