# learning/code/ex-47-shrinking-minimal-counterexample/test_example.py
"""Example 47: Shrinking to a Minimal Counterexample."""

from hypothesis import given  # => same property-test decorator -- this file is DELIBERATELY buggy (co-19)  # fmt: skip
from hypothesis import strategies as st  # => generates lists of integers, of varying length (co-20)  # fmt: skip


def buggy_sum(
    xs: list[int],
) -> int:  # => the unit under test -- has a REAL, deliberate bug
    total = 0  # => accumulator, starts at zero
    for x in xs[:-1]:  # => BUG: xs[:-1] drops the LAST element -- should just be `for x in xs`  # fmt: skip
        total += x  # => never adds the dropped last element
    return total  # => wrong for any non-empty list


@given(st.lists(st.integers(), min_size=1))  # => co-20: min_size=1 forces at least one element every time  # fmt: skip
def test_buggy_sum_matches_builtin_sum(xs: list[int]) -> None:
    # => this assertion is EXPECTED to fail -- buggy_sum silently drops the last element,
    # => so Hypothesis WILL find a failing input and then SHRINK it to a minimal one (co-19)
    assert buggy_sum(xs) == sum(xs)  # => genuinely fails for any list where the last element matters  # fmt: skip
