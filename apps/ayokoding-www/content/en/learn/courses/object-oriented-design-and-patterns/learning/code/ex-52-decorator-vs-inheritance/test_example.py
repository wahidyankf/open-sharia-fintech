"""Example 52: pytest verification for Decorator vs the Subclass Explosion."""

from example import Coffee, CoffeeWithMilk, MilkDecorator, SugarDecorator


def test_decorator_matches_the_dedicated_subclass_for_one_add_on() -> None:
    assert MilkDecorator(Coffee()).cost() == CoffeeWithMilk().cost()


def test_stacking_two_decorators_needs_no_dedicated_combination_class() -> None:
    # => no "CoffeeWithMilkAndSugar" class exists anywhere in example.py
    combo = SugarDecorator(MilkDecorator(Coffee()))
    assert combo.cost() == 2.75


def test_three_decorators_stack_just_as_easily_as_two() -> None:
    # => proof this scales: a THIRD add-on needs one more wrapper class, not more combinations
    combo = SugarDecorator(MilkDecorator(SugarDecorator(Coffee())))
    assert combo.cost() == 3.0  # => 2.0 base + 0.25 + 0.5 + 0.25


# => Run: pytest -- Output: 3 passed
