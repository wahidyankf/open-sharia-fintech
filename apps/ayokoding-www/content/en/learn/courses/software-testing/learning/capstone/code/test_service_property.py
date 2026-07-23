"""Capstone Step 3: a Hypothesis property test asserting compute_subtotal() is order-independent."""
# The invariant: summing a list of prices gives the SAME result regardless of the list's
# order -- true for any correct summation, and a genuinely useful property because it holds
# over infinitely many inputs, not just the three hand-picked cases test_service_unit.py checks.
# See the capstone overview's Run block for this test genuinely CATCHING a seeded regression as
# TWO distinct failures (Hypothesis's shrinking reduces each to its own minimal counterexample),
# then passing again once the regression is reverted.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from hypothesis import given  # => co-18: the decorator that turns a plain function into a property  # fmt: skip
from hypothesis import strategies as st  # => co-20: generates the price lists this property checks  # fmt: skip

from service import compute_subtotal  # => co-01: the SAME pure function Step 1's unit tests checked  # fmt: skip


@given(  # => co-20: Hypothesis GENERATES many price lists -- not three hand-picked examples  # fmt: skip
    prices=st.lists(
        st.floats(
            min_value=0, max_value=1000, allow_nan=False, allow_infinity=False
        ),  # => co-20: bounded, finite floats  # fmt: skip
        min_size=0,  # => co-20: includes the empty-list edge case in every run  # fmt: skip
        max_size=10,  # => co-20: caps list size -- keeps each generated case fast to check  # fmt: skip
    )
)
def test_property_subtotal_is_order_independent(
    prices: list[float],
) -> None:  # => co-18: the invariant
    forward = compute_subtotal(prices)  # => the ORIGINAL order  # fmt: skip
    reversed_total = compute_subtotal(list(reversed(prices)))  # => the SAME items, REVERSED order  # fmt: skip
    assert forward == reversed_total  # => co-18/co-19: true for a CORRECT sum, for EVERY generated list  # fmt: skip
