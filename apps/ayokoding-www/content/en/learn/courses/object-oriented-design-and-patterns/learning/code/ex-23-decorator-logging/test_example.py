"""Example 23: pytest verification for Decorator: Log a Service Call Without Editing It."""

import inspect

from example import LOG, charge


def test_charge_source_contains_no_logging_statements() -> None:
    source: str = inspect.getsource(charge)  # => reads the DECORATED function's own source text (the wrapper, via @wraps)
    assert "LOG" not in source  # => proves the wrapper's logging lives outside this body


def test_calling_charge_still_records_a_log_entry() -> None:
    LOG.clear()  # => resets the shared log before this test's own assertions
    result: str = charge(50.0)
    assert result == "charged 50.0"  # => the original business result is unchanged
    assert len(LOG) == 2  # => one entry logged before the call, one logged after


# => Run: pytest -- Output: 2 passed
