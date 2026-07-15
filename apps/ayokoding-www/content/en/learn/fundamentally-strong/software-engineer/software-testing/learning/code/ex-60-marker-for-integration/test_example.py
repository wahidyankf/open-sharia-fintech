# learning/code/ex-60-marker-for-integration/test_example.py
"""Example 60: A Marker for Integration Tests."""

import pytest  # => brings in @pytest.mark.integration -- a CUSTOM marker, registered in pytest.ini (co-08)  # fmt: skip


def add(a: int, b: int) -> int:  # => a pure function -- stands in for genuinely FAST unit-level logic  # fmt: skip
    return a + b


def test_pure_unit_logic_always_runs() -> None:  # => NO marker -- always included, in every run (co-10)  # fmt: skip
    assert add(2, 3) == 5  # => fast, isolated, no external dependency at all


@pytest.mark.integration  # => co-08/co-10: labels a test that would touch a REAL external dependency  # fmt: skip
def test_something_that_would_need_a_real_database() -> None:
    # => in a real suite, this test would open an ACTUAL database connection -- here it is
    # => a stand-in, kept trivial on purpose, since only the MARKER matters for this example
    assert add(1, 1) == 2  # => a placeholder for what would be a slower, real-dependency-backed check  # fmt: skip
    # => `pytest -m "not integration"` excludes EXACTLY this test, keeping a fast unit-only
    # => run separate from a slower run that would touch real infrastructure (co-10)
