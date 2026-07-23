# learning/code/ex-50-example-plus-property/test_example.py
"""Example 50: Pinning a Case with @example."""

from hypothesis import example, given  # => @example PINS one specific case, always run alongside generated ones (co-18)  # fmt: skip
from hypothesis import (
    strategies as st,
)  # => the usual generated-input strategy, unchanged


def double(n: int) -> int:  # => the unit under test
    return n * 2  # => always even, for any integer input


@given(st.integers())  # => co-18: the normal, GENERATED case coverage
@example(0)  # => co-18: a PINNED edge case -- always tested, whether or not Hypothesis would generate it  # fmt: skip
@example(-1)  # => a SECOND pinned case -- negative numbers are worth pinning explicitly too  # fmt: skip
def test_double_is_always_even(x: int) -> None:
    # => both @example(0) and @example(-1) are GUARANTEED to run on every test session,
    # => in addition to whatever values Hypothesis's own random generation picks (co-18)
    assert (x * 2) % 2 == 0  # => the invariant: double() output is divisible by 2 for any integer  # fmt: skip
