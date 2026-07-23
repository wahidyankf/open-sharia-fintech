"""Example 68: `asyncio.TaskGroup` -- One Failure Cancels ALL Its Siblings."""

import asyncio  # => co-26: `TaskGroup` (3.11+) is STRUCTURED concurrency -- gather's more disciplined cousin


class DownloadError(Exception):  # => a domain-specific failure, to show it propagates with its own type intact
    """Raised by `flaky_download` when a simulated download fails."""


async def flaky_download(n: int, fail_at: int, ran_to_completion: list[int]) -> int:
    if n == fail_at:  # => exactly ONE task in the group is designed to fail
        await asyncio.sleep(0.02)  # => fails a LITTLE after the others start, so they're genuinely mid-flight
        raise DownloadError(f"download {n} failed")  # => the failure that should cancel every sibling
    await asyncio.sleep(0.2)  # => the OTHER tasks are deliberately slower -- still running when the failure hits
    ran_to_completion.append(n)  # => only reached if this task was NEVER cancelled by a sibling's failure
    return n  # => a trivial "result" for the tasks that DO succeed


async def run_task_group() -> tuple[bool, list[int]]:
    ran_to_completion: list[int] = []  # => ran_to_completion: filled in ONLY by tasks that finish uncancelled
    raised = False  # => raised: True once the group's own ExceptionGroup is caught below
    try:
        async with asyncio.TaskGroup() as tg:  # => `async with` scopes the group -- exits ONLY when ALL are done
            for i in range(4):  # => launches 4 sibling tasks, one of which (i == 1) is designed to fail
                tg.create_task(flaky_download(i, fail_at=1, ran_to_completion=ran_to_completion))
    except* DownloadError:  # => `except*` (3.11+): TaskGroup wraps failures in an ExceptionGroup, unpacked here
        raised = True  # => confirms the failure propagated out of the `async with` block, as designed
    return raised, ran_to_completion  # => everything the caller needs to verify cancellation propagated


if __name__ == "__main__":  # => module entry point
    raised, ran_to_completion = asyncio.run(run_task_group())  # => drives the whole scenario to completion
    print(f"raised={raised} ran_to_completion={ran_to_completion}")  # => Output: raised=True ran_to_completion=[]

    # => `asyncio.TaskGroup` implements STRUCTURED concurrency (co-26): the moment ANY task inside the
    # => `async with` block raises, EVERY OTHER task in the group is automatically cancelled, and the
    # => group's own exit re-raises the failure (wrapped in an `ExceptionGroup`, unpacked here via
    # => `except*`). This is a stricter, safer default than `asyncio.gather` (ex-28, ex-50), where a
    # => failing task by itself does NOT automatically cancel its siblings unless explicitly configured --
    # => `TaskGroup` makes "one fails, all stop" the guaranteed behavior, not something to remember to add.
    assert raised is True  # => confirms the DownloadError genuinely propagated out of the TaskGroup
    assert ran_to_completion == []  # => confirms the slower siblings were CANCELLED, never reaching their append
    print("ex-68 OK")  # => Output: ex-68 OK
