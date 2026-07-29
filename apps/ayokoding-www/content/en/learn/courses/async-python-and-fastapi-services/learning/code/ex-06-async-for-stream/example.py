"""Example 6: Consuming an Async Stream with async for."""

import asyncio  # => the event-loop module (co-02)
from collections.abc import AsyncIterator  # => the typed return shape of an async generator (co-05)


async def emit(count: int) -> AsyncIterator[int]:  # => an ASYNC GENERATOR -- "async def" + "yield"
    for i in range(count):  # => produces one item per iteration
        await asyncio.sleep(0.01)  # => yields to the loop between items (co-01)
        yield i  # => hands one value to the consumer, then resumes here on the next pull (co-05)


async def main() -> list[int]:  # => consumes the whole stream into a list
    collected: list[int] = []  # => accumulator for the values pulled from the stream
    # => "async for" PULLS the next item, awaiting the generator between each one (co-05)
    async for value in emit(3):  # => each iteration awaits the generator's next "yield"
        collected.append(value)  # => values arrive one at a time, 0 then 1 then 2
    return collected  # => the full stream, materialised in order


if __name__ == "__main__":  # => only runs when executed directly
    result = asyncio.run(main())  # => drive the async main
    print(result)  # => Output: [0, 1, 2]
