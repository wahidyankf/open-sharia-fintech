# learning/code/ex-49-hypothesis-assume/test_example.py
"""Example 49: Discarding Invalid Inputs with assume()."""

import pytest  # => pytest.approx -- for comparing the float result below (co-07)
from hypothesis import assume, given  # => assume() DISCARDS a generated input rather than failing on it (co-20)  # fmt: skip
from hypothesis import strategies as st  # => generates a wide range of integers, including zero  # fmt: skip


def reciprocal(x: float) -> float:  # => the unit under test -- undefined (raises) at x == 0  # fmt: skip
    return 1 / x  # => genuinely raises ZeroDivisionError if x is 0 -- not this example's concern  # fmt: skip


@given(st.integers(min_value=-1000, max_value=1000))  # => co-20: includes zero among the generated values  # fmt: skip
def test_reciprocal_property_excludes_zero(x: int) -> None:
    assume(x != 0)  # => co-20: DISCARDS x==0 entirely -- Hypothesis just generates a different value instead  # fmt: skip
    # => assume() is NOT the same as an if-guard around the assertion -- a discarded input
    # => does not count as a passing case at all, it is simply excluded from consideration
    result = reciprocal(
        x
    )  # => act: only ever runs for x != 0, thanks to assume() above
    assert result * x == pytest.approx(1.0)  # => the property: x times its OWN reciprocal is always ~1.0  # fmt: skip
