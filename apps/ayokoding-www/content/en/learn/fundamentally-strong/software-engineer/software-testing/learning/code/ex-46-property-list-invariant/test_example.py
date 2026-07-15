# learning/code/ex-46-property-list-invariant/test_example.py
"""Example 46: Property -- A List Invariant."""

from hypothesis import (
    given,
)  # => same property-test decorator as prior examples (co-18)
from hypothesis import strategies as st  # => st.lists(st.integers()) generates lists of VARYING length and content (co-20)  # fmt: skip


@given(st.lists(st.integers()))  # => co-18/co-20: empty lists, single-item lists, duplicates -- all generated  # fmt: skip
def test_sorted_preserves_length_and_orders_elements(xs: list[int]) -> None:
    result = sorted(xs)  # => act: the built-in sorted(), the unit under test in this example  # fmt: skip

    # invariant 1: sorting can never add or remove elements -- only reorder them
    assert len(result) == len(
        xs
    )  # => length invariant, checked across every generated list

    # invariant 2: every adjacent pair in the result must be non-decreasing
    for i in range(len(result) - 1):  # => walks every adjacent pair once
        assert result[i] <= result[i + 1]  # => the ORDERING invariant itself -- true for a genuinely sorted list  # fmt: skip
