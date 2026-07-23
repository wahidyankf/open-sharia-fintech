"""Example 52: Decorator Avoids the Subclass Explosion of Coffee Add-Ons."""

import abc  # => imports the abc module


class Beverage(abc.ABC):  # => shared by BOTH the subclass version and the decorator version
    @abc.abstractmethod
    def cost(self) -> float:  # => no body -- required by every concrete beverage
        ...  # => the ellipsis stub -- concrete beverages below fill this in


class Coffee(Beverage):  # => the base drink, with no add-ons at all
    def cost(self) -> float:  # => defines the cost() method
        return 2.0  # => returns this value to the caller


# => THE SUBCLASS-EXPLOSION APPROACH: one class per COMBINATION of add-ons
class CoffeeWithMilk(Beverage):  # => covers ONLY the "milk alone" combination
    def cost(self) -> float:  # => defines the cost() method
        return 2.0 + 0.5  # => duplicates Coffee's base price PLUS one add-on's price

    # => a SECOND add-on (sugar) needs CoffeeWithSugar, AND CoffeeWithMilkAndSugar too --
    # => N independent add-ons need up to 2**N subclasses to cover every combination


# => THE DECORATOR APPROACH: one wrapper class PER add-on, composed at runtime
class BeverageDecorator(Beverage):  # => wraps ANY Beverage, itself IS-A Beverage too
    def __init__(self, wrapped: Beverage) -> None:  # => the constructor
        self._wrapped: Beverage = wrapped  # => the beverage (or ANOTHER decorator) being wrapped

    def cost(self) -> float:  # => defines the cost() method
        return self._wrapped.cost()  # => the base case -- subclasses below ADD to this


class MilkDecorator(BeverageDecorator):  # => adds ONE thing: milk's price, to WHATEVER it wraps
    def cost(self) -> float:  # => defines the cost() method
        return super().cost() + 0.5  # => delegates, then adds its own contribution


class SugarDecorator(BeverageDecorator):  # => adds ONE thing: sugar's price, to WHATEVER it wraps
    def cost(self) -> float:  # => defines the cost() method
        return super().cost() + 0.25  # => delegates, then adds its own contribution


exploded: Beverage = CoffeeWithMilk()  # => the subclass-explosion version, milk only
print(exploded.cost())  # => matches the decorator version below for THIS one combination
# => Output: 2.5

milk_only: Beverage = MilkDecorator(Coffee())  # => ONE decorator, composed at runtime
print(milk_only.cost())  # => the SAME result as CoffeeWithMilk, with no dedicated subclass
# => Output: 2.5

milk_and_sugar: Beverage = SugarDecorator(MilkDecorator(Coffee()))  # => TWO add-ons, STACKED -- no CoffeeWithMilkAndSugar class needed anywhere
print(milk_and_sugar.cost())  # => a combination the subclass approach would need a THIRD class for
# => Output: 2.75
# => N decorator classes cover EVERY combination of N add-ons -- the subclass approach needs up to 2**N classes
