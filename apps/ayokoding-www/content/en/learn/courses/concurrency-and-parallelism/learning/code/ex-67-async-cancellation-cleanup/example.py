"""Example 67: Cancelling a Task -- Catching `CancelledError` to Run Cleanup."""

import asyncio  # => co-26, co-27: cancellation is delivered AS an exception, not a silent flag


class FakeResource:  # => stands in for something that MUST be released -- a connection, a file handle
    def __init__(self) -> None:
        # => starts unreleased -- the whole point of this example is proving release() DOES get called
        self.released = False  # => released: starts False -- flips to True ONLY via release()

    def release(self) -> None:
        # => a REAL resource's release() might close a socket, flush a buffer, or free a lock
        self.released = True  # => marks this resource as properly cleaned up


async def work_with_cleanup(resource: FakeResource) -> None:
    # => the caller is responsible for making sure THIS coroutine reaches an await before cancelling
    try:
        await asyncio.sleep(10)  # => a long-running await -- this is where cancellation will actually land
    except asyncio.CancelledError:  # => `task.cancel()` raises THIS exception at the current `await` point
        resource.release()  # => the cleanup -- runs BECAUSE the exception was caught here, not silently dropped
        raise  # => re-raises: swallowing CancelledError entirely is almost always wrong (co-27)


async def run_and_cancel() -> tuple[bool, bool]:
    # => orchestrates the whole demo: create the task, let it start, cancel it, observe the fallout
    resource = FakeResource()  # => resource: the thing this task is responsible for cleaning up
    task = asyncio.create_task(work_with_cleanup(resource))  # => schedules the coroutine to start running
    await asyncio.sleep(0.02)  # => lets the task actually REACH its `await asyncio.sleep(10)` before cancelling
    task.cancel()  # => requests cancellation -- delivers CancelledError at the task's current await point
    was_cancelled = False  # => was_cancelled: True only if awaiting the task itself raises CancelledError
    try:
        # => `await task` is where the CALLER (not the task itself) observes the cancellation
        await task  # => awaiting a cancelled task re-raises the SAME CancelledError to the caller
    except asyncio.CancelledError:  # => confirms cancellation propagated all the way out, as expected
        was_cancelled = True  # => records that the caller correctly observed the cancellation
    return resource.released, was_cancelled  # => everything needed to verify BOTH cleanup and propagation


if __name__ == "__main__":  # => module entry point
    released, was_cancelled = asyncio.run(run_and_cancel())  # => drives the cancellation scenario to completion
    print(f"released={released} was_cancelled={was_cancelled}")  # => Output: released=True was_cancelled=True

    # => `task.cancel()` does NOT immediately stop a task -- it schedules `CancelledError` to be raised
    # => at the NEXT `await` point inside that task (co-26). Catching it, like any exception, is the
    # => correct place to release resources (co-27) -- but the handler must `raise` (or otherwise NOT
    # => suppress it) afterward, since callers awaiting a cancelled task expect to see CancelledError
    # => propagate; swallowing it silently would make the task appear to have completed normally.
    assert released is True  # => confirms the `except CancelledError:` block genuinely ran cleanup
    assert was_cancelled is True  # => confirms CancelledError still propagated out to the awaiting caller
    print("ex-67 OK")  # => Output: ex-67 OK
