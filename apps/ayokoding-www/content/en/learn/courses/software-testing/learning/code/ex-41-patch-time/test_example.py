# learning/code/ex-41-patch-time/test_example.py
"""Example 41: Freezing Time."""

import datetime  # => the real, wall-clock-dependent module this example needs to CONTROL (co-26)  # fmt: skip

from freezegun import freeze_time  # => freezegun 1.5.5 -- freezes datetime.now() to a fixed point (co-14)  # fmt: skip


def get_year() -> int:  # => the unit under test -- normally non-deterministic (depends on WHEN it runs)  # fmt: skip
    return datetime.datetime.now().year  # => without freezing, this changes every year the suite runs  # fmt: skip


def test_freeze_time_makes_the_year_deterministic() -> None:
    with freeze_time("2030-01-01"):  # => co-14/co-26: pins datetime.now() to an EXACT, fixed moment  # fmt: skip
        assert get_year() == 2030  # => act+assert: deterministic, regardless of when this test ACTUALLY runs  # fmt: skip
    # => outside the "with" block, datetime.now() reverts to the REAL current time --
    # => freeze_time, like mock.patch (ex-35), is scoped to its own context manager block
    assert get_year() != 2030 or True  # => sanity: this line runs with the REAL clock restored (always true, documents scope)  # fmt: skip
