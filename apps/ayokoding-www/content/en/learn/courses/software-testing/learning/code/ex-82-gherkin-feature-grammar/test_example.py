"""Example 82: Gherkin Grammar -- Feature / Scenario / Given / And / When / Then, Parsed for Real."""
# There is no @and decorator in pytest-bdd's API -- Gherkin's And/But simply repeat the TYPE of
# the step immediately before them, and this file proves it by binding an "And" with plain @given.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from pytest_bdd import given, scenario, then, when  # => co-29: Gherkin's And/But INHERIT the type  # fmt: skip
# => of the step before them -- pytest-bdd binds an "And" using the SAME decorator as its Given/When/Then


@scenario(  # => co-29: pytest-bdd PARSES the .feature file below -- this is not hand-written prose  # fmt: skip
    "features/checkout_eligibility.feature",
    "A cart with items is eligible for checkout",
)
def test_a_cart_with_items_is_eligible_for_checkout() -> None:  # => co-29: the parsed scenario's name  # fmt: skip
    """The Gherkin grammar drives this test -- Feature/Scenario/Given/And/When/Then, all present."""  # fmt: skip


@given("an empty cart", target_fixture="cart")  # => co-29: the Given keyword  # fmt: skip
def an_empty_cart() -> list[str]:  # => co-29: the very first step in the scenario  # fmt: skip
    return []  # => co-29: an empty list represents an empty cart  # fmt: skip


@given("the cart has 2 items added to it")  # => co-29: "And" after a Given IS a Given -- same binder  # fmt: skip
def the_cart_has_2_items(cart: list[str]) -> None:  # => co-29: receives the SAME "cart" fixture  # fmt: skip
    cart.append("item-1")  # => co-29: And-steps read the SAME Gherkin grammar as Given/When/Then  # fmt: skip
    cart.append("item-2")  # => co-29: the SECOND item -- cart now genuinely has two entries  # fmt: skip


@when(
    "the shopper checks checkout eligibility", target_fixture="is_eligible"
)  # => co-29: When
def checks_checkout_eligibility(cart: list[str]) -> bool:  # => co-29: the ACTION step of the scenario  # fmt: skip
    return len(cart) > 0  # => co-29: eligibility rule -- a non-empty cart may check out  # fmt: skip


@then("the cart is eligible for checkout")  # => co-29: the Then keyword  # fmt: skip
def the_cart_is_eligible(is_eligible: bool) -> None:  # => co-29: requests the WHEN step's fixture  # fmt: skip
    assert is_eligible is True  # => co-29: ties the Gherkin outcome to a real Python assertion  # fmt: skip
