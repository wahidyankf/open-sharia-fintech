"""Example 52: An `asyncio.Queue` Pipeline -- Cooperative Producer/Consumer."""

import asyncio  # => co-26, co-22: the async counterpart to ex-21's threaded producer/consumer

ITEM_COUNT = 10  # => how many items the producer generates for the consumer to process


async def producer(q: "asyncio.Queue[int | None]") -> None:
    for i in range(ITEM_COUNT):  # => generates ITEM_COUNT items, cooperatively yielding between each
        await q.put(i)  # => `await` because put() can suspend if the queue has a maxsize and is full
        await asyncio.sleep(0)  # => yields control to the event loop -- lets the consumer interleave
    await q.put(None)  # => None: the sentinel telling the consumer there are no more items coming


async def consumer(q: "asyncio.Queue[int | None]", collected: list[int]) -> None:
    while True:  # => keeps draining until the sentinel arrives
        item = await q.get()  # => `await` because get() can suspend if the queue is momentarily empty
        if item is None:  # => None is the shutdown sentinel produced above
            break  # => stops the consumer's loop
        collected.append(item)  # => records the item -- SAFE without a lock since this is single-threaded


async def run_pipeline() -> list[int]:
    q: "asyncio.Queue[int | None]" = asyncio.Queue(maxsize=3)  # => a BOUNDED queue -- backpressure, same idea as ex-38
    collected: list[int] = []  # => collected: filled in by the consumer coroutine as it drains the queue
    await asyncio.gather(producer(q), consumer(q, collected))  # => runs BOTH coroutines concurrently on one loop
    return collected  # => everything the consumer managed to pull off the queue


if __name__ == "__main__":  # => module entry point
    collected = asyncio.run(run_pipeline())  # => drives the whole pipeline to completion on one event loop
    print(f"collected={collected}")  # => Output: collected=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # => `asyncio.Queue` provides the SAME put/get/maxsize/sentinel shape as `queue.Queue` (ex-20-ex-22),
    # => but its `put`/`get` are coroutines (`await`-able) instead of blocking calls -- appropriate for a
    # => SINGLE-THREADED event loop, where a genuinely blocking call would freeze everything (co-27,
    # => see ex-54). Producer and consumer run as separate Tasks under `asyncio.gather`, cooperatively
    # => taking turns at every `await` point, and every item the producer makes IS consumed in order.
    assert collected == list(range(ITEM_COUNT))  # => confirms every item arrived, in order, none lost
    print("ex-52 OK")  # => Output: ex-52 OK
