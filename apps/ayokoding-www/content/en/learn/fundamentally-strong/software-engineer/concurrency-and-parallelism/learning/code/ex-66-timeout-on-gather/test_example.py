"""Example 66: pytest verification for `asyncio.wait` with a Timeout."""

import asyncio

from example import wait_with_timeout


def test_asyncio_wait_returns_both_done_and_pending_sets() -> None:
    done_labels, pending_count = asyncio.run(wait_with_timeout())
    assert done_labels == {"task-0", "task-1"}  # => exactly the two fast tasks finished in time
    assert pending_count == 2  # => exactly the two slow tasks were still running at the deadline


# => Run: pytest -- Output: 1 passed
