"""Example 67: pytest verification for Async Task Cancellation Cleanup."""

import asyncio

from example import run_and_cancel


def test_cancellation_runs_cleanup_and_still_propagates() -> None:
    released, was_cancelled = asyncio.run(run_and_cancel())
    assert released is True  # => the except CancelledError block ran the resource release
    assert was_cancelled is True  # => CancelledError still propagated out to the awaiting caller


# => Run: pytest -- Output: 1 passed
