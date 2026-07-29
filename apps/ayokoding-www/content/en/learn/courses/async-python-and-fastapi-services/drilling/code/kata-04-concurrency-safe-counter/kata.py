"""Kata 4 -- A concurrency-safe counter under simulated concurrent tasks (co-23)."""

import asyncio  # => co-23: Lock guards the critical section


class Counter:  # => a lock-guarded shared counter (co-23)
    def __init__(self) -> None:
        self._value = 0  # => the shared mutable state
        self._lock = (
            asyncio.Lock()
        )  # => only one coroutine in the critical section at a time

    async def inc(self) -> int:  # => a guarded read-modify-write
        async with self._lock:  # => atomic across coroutines (co-23)
            self._value += 1  # => the critical section
            return self._value  # => the new value


async def main() -> None:  # => N concurrent increments
    counter = Counter()  # => the shared counter
    n = 100  # => number of concurrent increments
    await asyncio.gather(
        *(counter.inc() for _ in range(n))
    )  # => all run concurrently (co-04)
    print(counter._value)  # => Output: 100 -- no lost updates
    assert counter._value == n  # => the lock made every increment count


if __name__ == "__main__":
    asyncio.run(main())
