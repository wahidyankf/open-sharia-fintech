# learning/code/ex-10-approx-float/test_example.py
"""Example 10: Approx for Floats."""

import pytest  # => brings in pytest.approx, the tolerance-based float comparator (co-07)


def test_float_addition_is_not_exact() -> None:  # => documents WHY approx exists at all
    assert (
        0.1 + 0.2 != 0.3
    )  # => binary floating point cannot represent 0.1 exactly (IEEE 754)
    # => this assert PASSES specifically because 0.1 + 0.2 is 0.30000000000000004, not 0.3


def test_approx_treats_them_as_equal_anyway() -> None:
    assert 0.1 + 0.2 == pytest.approx(0.3)  # => approx wraps 0.3 in a tolerance-aware comparator  # fmt: skip
    # => approx's default relative tolerance is 1e-6 -- the 4e-17 error above is far inside it,
    # => so this comparison succeeds even though the plain == in the test above it fails
