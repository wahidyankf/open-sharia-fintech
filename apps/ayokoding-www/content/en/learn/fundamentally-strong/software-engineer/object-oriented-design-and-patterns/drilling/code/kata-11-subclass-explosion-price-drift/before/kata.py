"""Kata 11 (before): subclass explosion -- CoffeeWithMilkAndSugar hardcodes a price that drifts from Coffee's own price."""


class Coffee:
    def cost(self) -> float:
        return 2.00


class CoffeeWithMilk(Coffee):
    def cost(self) -> float:
        return 2.50  # hardcoded: base 2.00 + 0.50, duplicated by hand


class CoffeeWithMilkAndSugar(CoffeeWithMilk):
    def cost(self) -> float:
        return 2.75  # hardcoded AGAIN -- if Coffee.cost() ever changes, this number silently goes stale


Coffee.cost = lambda self: 3.00  # type: ignore[method-assign]  # simulates a LATER price bump to the base Coffee
print(CoffeeWithMilkAndSugar().cost())  # expected 3.75 (3.00 + 0.50 + 0.25) -- still shows the STALE 2.75
