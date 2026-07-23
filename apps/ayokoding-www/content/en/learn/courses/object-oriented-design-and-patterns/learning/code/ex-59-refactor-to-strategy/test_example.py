"""Example 59: pytest verification that the strategy refactor stays green throughout."""

import pytest

from example import (
    SHIPPING_STRATEGIES,
    bulk_shipping,
    shipping_cost_if_chain,
    shipping_cost_via_strategy,
)


@pytest.mark.parametrize(
    "method,weight,expected",
    [("standard", 3.0, 6.0), ("express", 4.0, 20.0), ("overnight", 2.0, 35.0)],
)  # => same three cases run through both dispatchers, proving the refactor changed nothing observable
def test_old_and_new_dispatchers_agree_on_every_known_method(method: str, weight: float, expected: float) -> None:
    assert shipping_cost_if_chain(method, weight) == expected  # => old if-chain dispatcher
    assert shipping_cost_via_strategy(method, weight) == expected  # => new strategy-table dispatcher


def test_both_dispatchers_reject_an_unknown_method_identically() -> None:
    with pytest.raises(ValueError, match="unknown shipping method"):  # => old dispatcher's error
        shipping_cost_if_chain("teleport", 1.0)
    with pytest.raises(ValueError, match="unknown shipping method"):  # => new dispatcher's error, same message
        shipping_cost_via_strategy("teleport", 1.0)


def test_adding_a_new_strategy_requires_zero_edits_to_the_dispatcher() -> None:
    SHIPPING_STRATEGIES["bulk"] = bulk_shipping  # => registers a fourth strategy at test time
    assert shipping_cost_via_strategy("bulk", 10.0) == 7.0  # => works immediately, no dispatcher code changed
    del SHIPPING_STRATEGIES["bulk"]  # => cleans up so this test does not leak state into other tests


# => Run: pytest -q -- Output: 5 passed
