"""Kata 11 (after): Decorator wraps the CURRENT Coffee price, so a base price change is picked up automatically."""

from typing import Protocol


class CoffeeLike(Protocol):
    def cost(self) -> float: ...


class Coffee:
    def cost(self) -> float:
        return 3.00  # the "later" price, current from the start this time


class MilkDecorator:  # => co-21: wraps ANY CoffeeLike, adds its own delta on top of whatever cost() returns NOW
    def __init__(self, wrapped: CoffeeLike) -> None:
        self._wrapped = wrapped

    def cost(self) -> float:
        return self._wrapped.cost() + 0.50


class SugarDecorator:
    def __init__(self, wrapped: CoffeeLike) -> None:
        self._wrapped = wrapped

    def cost(self) -> float:
        return self._wrapped.cost() + 0.25


coffee_with_milk_and_sugar = SugarDecorator(MilkDecorator(Coffee()))
print(coffee_with_milk_and_sugar.cost())  # always reflects Coffee's CURRENT price, no stale hardcoded total
