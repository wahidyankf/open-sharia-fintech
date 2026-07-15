# learning/code/ex-56-fixture-parametrized/test_example.py
"""Example 56: A Parametrized Fixture."""

import pytest  # => brings in @pytest.fixture(params=...) -- combining co-05 with co-06 (co-05, co-06)  # fmt: skip


@pytest.fixture(params=[1, 2, 3])  # => co-06: THREE param values -- the fixture itself fans out, not just @parametrize  # fmt: skip
def sample_number(request) -> int:  # => request.param holds the CURRENT value from params= above (co-05)  # fmt: skip
    return (
        request.param
    )  # => whichever of 1, 2, 3 this particular run is currently using


def test_number_is_positive(sample_number: int) -> None:  # => uses the fixture -- runs 3 TIMES, once per param  # fmt: skip
    assert sample_number > 0  # => true for all three: 1, 2, 3


def test_number_squared_is_at_least_itself(sample_number: int) -> None:  # => a SECOND test, SAME fixture -- also runs 3 times  # fmt: skip
    assert sample_number**2 >= sample_number  # => true for all three: 1<=1, 4>=2, 9>=3
    # => TWO test functions, both depending on the SAME parametrized fixture, produce
    # => 3 + 3 = 6 total test runs -- the fan-out lives in the FIXTURE, not in either test body  # fmt: skip
