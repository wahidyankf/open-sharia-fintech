"""Example 72: Async Generator Backpressure.

A bounded asyncio.Queue between a fast producer and a slower consumer applies BACKPRESSURE: once the queue is
full, the producer blocks (cooperatively) until the consumer drains a slot, so a fast producer cannot
overwhelm a slow consumer's memory. Run: python3 example.py. (co-22, co-23)
"""

import asyncio  # => asyncio.Queue is the bounded buffer (co-23)
from collections.abc import AsyncIterator


async def producer(queue: asyncio.Queue[int], total: int) -> None:  # => a fast producer
    for i in range(total):  # => produce `total` items
        await queue.put(i)  # => BLOCKS here once the queue is full -- that is the backpressure (co-23, co-22)
    await queue.put(None)  # => a sentinel signalling "no more items" (co-22)


async def consumer(queue: asyncio.Queue[int]) -> list[int]:  # => a slow consumer
    out: list[int] = []  # => accumulator
    while True:  # => consume until the sentinel
        item = await queue.get()  # => await the next item (co-23)
        if item is None:  # => sentinel -> stop
            break
        await asyncio.sleep(0.01)  # => simulate SLOW processing -- the producer waits when full (co-22)
        out.append(item)  # => record the consumed item
    return out  # => all consumed items, in order


async def stream_with_backpressure(total: int, bound: int) -> AsyncIterator[int]:  # => a streaming shape (co-22)
    queue: asyncio.Queue[int] = asyncio.Queue(maxsize=bound)  # => a BOUNDED queue -- the backpressure mechanism (co-23)
    producer_task = asyncio.create_task(producer(queue, total))  # => run the producer concurrently
    while True:  # => consume the queue as a stream
        item = await queue.get()  # => next item
        if item is None:  # => sentinel
            break
        yield item  # => one streamed item -- the producer is throttled while the queue is full (co-22)
    await producer_task  # => ensure the producer finished cleanly


async def main() -> None:  # => demonstrates the bounded stream
    consumed = [item async for item in stream_with_backpressure(5, 2)]  # => bound=2 -> backpressure on the producer (co-22)
    print(consumed)  # => Output: [0, 1, 2, 3, 4] -- all items, producer throttled by the bound


if __name__ == "__main__":  # => run directly
    asyncio.run(main())
