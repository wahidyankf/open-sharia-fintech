"""Example 66: `asyncio.wait(..., timeout=...)` -- Returns BOTH the Done AND the Pending Sets."""

import asyncio  # => co-26: `asyncio.wait` (unlike `gather`) never raises on a timeout -- it just reports

DELAYS = [0.05, 0.05, 0.3, 0.3]  # => two FAST tasks (finish within the timeout) and two SLOW tasks (don't)
WAIT_TIMEOUT = 0.15  # => the deadline: enough time for the fast tasks, not enough for the slow ones


async def labeled_sleep(label: str, delay: float) -> str:  # => label: identifies which task this is
    await asyncio.sleep(delay)  # => the only thing this coroutine does -- simulates work of varying length
    return label  # => returns its own label so the caller can tell WHICH tasks finished


async def wait_with_timeout() -> tuple[set[str], int]:
    tasks = [asyncio.create_task(labeled_sleep(f"task-{i}", d)) for i, d in enumerate(DELAYS)]
    # => tasks: every coroutine wrapped in a Task -- `asyncio.wait` requires Tasks/Futures, not raw coroutines
    done, pending = await asyncio.wait(tasks, timeout=WAIT_TIMEOUT)  # => returns AT the deadline, not before
    done_labels = {t.result() for t in done}  # => done_labels: the labels of whichever tasks ALREADY finished
    pending_count = len(pending)  # => pending_count: how many tasks were STILL RUNNING when the timeout hit
    for task in pending:  # => cleans up the still-running tasks so they don't outlive this coroutine
        task.cancel()  # => cancels each one -- otherwise they'd keep running in the background, orphaned
    return done_labels, pending_count  # => everything the caller needs to verify the timeout behavior


if __name__ == "__main__":  # => module entry point
    done_labels, pending_count = asyncio.run(wait_with_timeout())  # => drives the whole scenario to completion
    print(f"done_labels={done_labels} pending_count={pending_count}")  # => Output: done_labels={'task-0','task-1'} pending_count=2

    # => `asyncio.wait(tasks, timeout=...)` NEVER raises `TimeoutError` -- it simply returns as soon as
    # => the timeout elapses (or every task finishes, whichever comes first), splitting the tasks into
    # => `done` (already completed) and `pending` (still running) sets (co-26). This is fundamentally
    # => different from `asyncio.wait_for`/`asyncio.timeout` (ex-51), which CANCEL and raise on timeout --
    # => `asyncio.wait` instead hands BOTH sets back, letting the caller decide what to do with stragglers.
    assert done_labels == {"task-0", "task-1"}  # => confirms exactly the two FAST tasks finished in time
    assert pending_count == 2  # => confirms exactly the two SLOW tasks were still running at the deadline
    print("ex-66 OK")  # => Output: ex-66 OK
