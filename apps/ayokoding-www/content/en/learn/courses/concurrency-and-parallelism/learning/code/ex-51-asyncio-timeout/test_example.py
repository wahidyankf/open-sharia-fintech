"""Example 51: pytest verification for `asyncio.timeout` Cancellation."""

import asyncio

import pytest

from example import with_timeout


def test_fast_operation_completes_within_its_deadline() -> None:
    result = asyncio.run(with_timeout(delay=0.02, limit=0.5))
    assert result == "completed"


def test_slow_operation_raises_timeout_error() -> None:
    with pytest.raises(TimeoutError):
        asyncio.run(with_timeout(delay=0.5, limit=0.02))


# => Run: pytest -- Output: 2 passed
