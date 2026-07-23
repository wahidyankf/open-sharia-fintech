# learning/code/ex-45-property-commutative/test_example.py
"""Example 45: Property -- Commutativity."""

from hypothesis import given  # => same property-test decorator as ex-43/44 (co-18)
from hypothesis import strategies as st  # => TWO independent integer strategies this time  # fmt: skip


def add(a: int, b: int) -> int:  # => the unit under test
    return a + b  # => a pure function -- exactly what a property test is best suited to exercise  # fmt: skip


@given(st.integers(), st.integers())  # => co-18: TWO generated arguments, one strategy each  # fmt: skip
def test_add_is_commutative(a: int, b: int) -> None:
    # => COMMUTATIVE means order doesn't matter: a+b must equal b+a for EVERY pair
    # => Hypothesis generates, including negative numbers, zero, and large magnitudes (co-18)
    assert add(a, b) == add(b, a)  # => the invariant: swapping argument order never changes the result  # fmt: skip
