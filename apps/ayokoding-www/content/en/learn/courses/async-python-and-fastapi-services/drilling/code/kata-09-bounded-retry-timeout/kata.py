"""Kata 9 -- A bounded retry with a timeout around a flaky call (co-06, co-17)."""

import asyncio  # => co-06: asyncio.timeout enforces a deadline


async def call_with_retry(
    func, attempts: int, timeout: float
):  # => bounded retry + per-call deadline
    last_error: Exception = RuntimeError(
        "no attempts made"
    )  # => remembers the last failure
    for _ in range(attempts):  # => a BOUNDED number of attempts (co-06)
        try:
            async with asyncio.timeout(
                timeout
            ):  # => cut off a slow call after `timeout` (co-06)
                return await func()  # => success -> return immediately
        except (
            RuntimeError,
            TimeoutError,
        ) as exc:  # => transient failure or timeout -> retry
            last_error = exc  # => record and retry
    raise last_error  # => exhausted -> re-raise (a handler maps this to 503, co-17)


attempts_made = 0  # => a mutable counter for the mock


async def flaky():  # => fails twice, then succeeds
    global attempts_made
    attempts_made += 1
    await asyncio.sleep(0.01)  # => simulate latency (co-02)
    if attempts_made < 3:  # => fail the first two
        raise RuntimeError("transient")
    return "ok"  # => succeed on the third


async def main() -> None:
    result = await call_with_retry(
        flaky, attempts=5, timeout=1.0
    )  # => succeeds on attempt 3
    print(result)  # => Output: ok
    assert result == "ok"


if __name__ == "__main__":
    asyncio.run(main())
