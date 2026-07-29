"""Example 4: Scheduling Background Work as a Task."""

import asyncio  # => create_task and gather live here (co-04)


async def step(label: str, seconds: float) -> str:  # => a unit of background work
    await asyncio.sleep(seconds)  # => yields to the loop while "working" (co-01)
    return f"{label} done"  # => the value the Task resolves to


async def main() -> list[str]:  # => schedules work, does other things, then collects results
    # => create_task WRAPS a coroutine in a Task and schedules it on the loop IMMEDIATELY (co-04)
    # => the coroutine starts running as soon as the loop gets control -- it does not wait to be awaited
    task = asyncio.create_task(step("background", 0.05))  # => running concurrently, in the background
    # => this await runs CONCURRENTLY with the task above -- both make progress on one loop
    foreground = await step("foreground", 0.05)  # => awaited directly, in the foreground
    # => awaiting the Task COLLECTS its result; if it already finished, this returns immediately
    background = await task  # => no extra wait if the task completed during the foreground await
    return [foreground, background]  # => both completed, in the order we collect them


if __name__ == "__main__":  # => only runs when executed directly
    results = asyncio.run(main())  # => drive the async main
    print(results)  # => Output: ['foreground done', 'background done']
