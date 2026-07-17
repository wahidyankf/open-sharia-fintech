"""Example 51: `asyncio.timeout` Cancels a Coroutine That Runs Too Long."""

import asyncio  # => co-26: `asyncio.timeout` (3.11+) is the modern, structured way to bound a wait


async def slow_operation(delay: float) -> str:  # => a coroutine that simulates a slow network call
    await asyncio.sleep(delay)  # => suspends for `delay` seconds -- the timeout races against THIS wait
    return "completed"  # => only reached if the sleep finishes before any surrounding timeout fires


async def with_timeout(delay: float, limit: float) -> str:
    async with asyncio.timeout(limit):  # => `async with` scopes the deadline to exactly this block
        return await slow_operation(delay)  # => if `delay` exceeds `limit`, this await is CANCELLED, not finished


if __name__ == "__main__":  # => module entry point
    fast_result = asyncio.run(with_timeout(delay=0.05, limit=0.5))  # => delay < limit -- should complete normally
    print(f"fast_result={fast_result!r}")  # => Output: fast_result='completed'

    timed_out = False  # => timed_out: flips to True only if TimeoutError is actually raised below
    try:
        asyncio.run(with_timeout(delay=0.5, limit=0.05))  # => delay > limit -- the timeout MUST fire first
    except TimeoutError:  # => `asyncio.timeout` raises the STANDARD `TimeoutError`, not an asyncio-specific one
        timed_out = True  # => confirms the slow coroutine was cancelled before it could finish

    print(f"timed_out={timed_out}")  # => Output: timed_out=True

    # => `asyncio.timeout(limit)` (Python 3.11+) starts a deadline the moment the `async with` block is
    # => entered; if the code inside hasn't finished by then, EVERY task running inside that block is
    # => cancelled, and a `TimeoutError` propagates out of the `async with`. This is the modern
    # => replacement for `asyncio.wait_for(coro, timeout=...)` -- both achieve the same cancellation
    # => semantics (co-26), but `asyncio.timeout` scopes more naturally to a block of MULTIPLE awaits.
    assert fast_result == "completed"  # => confirms the fast path finished well within its deadline
    assert timed_out is True  # => confirms the slow path was cancelled, and TimeoutError propagated
    print("ex-51 OK")  # => Output: ex-51 OK
