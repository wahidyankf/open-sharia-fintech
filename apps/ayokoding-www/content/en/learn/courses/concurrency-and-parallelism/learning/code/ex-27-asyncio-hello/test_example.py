"""Example 27: pytest verification for Your First Coroutine -- `async def` and `asyncio.run`."""

import asyncio

from example import greet


def test_coroutine_runs_to_completion_via_asyncio_run() -> None:
    result = asyncio.run(greet("pytest"))
    assert result == "hello, pytest"  # => asyncio.run() drove the coroutine to a final return value


# => Run: pytest -- Output: 1 passed
