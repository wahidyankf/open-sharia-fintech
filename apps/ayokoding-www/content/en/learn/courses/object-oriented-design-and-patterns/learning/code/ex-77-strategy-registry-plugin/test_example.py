"""Example 77: pytest verification that a third-party strategy loads without editing checkout()."""

import pytest

from example import BlackFridayPricing, PricingStrategyRegistry, StandardPricing, checkout


def test_built_in_strategy_prices_at_face_value() -> None:
    registry = PricingStrategyRegistry()
    registry.register("standard", StandardPricing())
    assert checkout(registry, "standard", 100.0) == 100.0


def test_third_party_strategy_registers_and_loads_without_a_core_edit() -> None:
    registry = PricingStrategyRegistry()
    registry.register("standard", StandardPricing())
    registry.register("black-friday", BlackFridayPricing())  # => a plugin, added purely by calling register()
    assert checkout(registry, "black-friday", 100.0) == 60.0  # => checkout() itself was never touched


def test_looking_up_an_unregistered_strategy_raises_a_clear_error() -> None:
    registry = PricingStrategyRegistry()
    with pytest.raises(KeyError, match="no pricing strategy registered"):
        checkout(registry, "nonexistent", 100.0)


# => Run: pytest -q -- Output: 3 passed
