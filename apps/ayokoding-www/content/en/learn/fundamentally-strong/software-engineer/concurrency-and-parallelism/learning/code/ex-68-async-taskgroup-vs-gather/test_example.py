"""Example 68: pytest verification for `asyncio.TaskGroup` Failure Cancellation."""

import asyncio

from example import run_task_group


def test_one_failing_task_cancels_all_its_siblings() -> None:
    raised, ran_to_completion = asyncio.run(run_task_group())
    assert raised is True  # => the DownloadError propagated out of the TaskGroup
    assert ran_to_completion == []  # => the slower siblings were cancelled, never completing


# => Run: pytest -- Output: 1 passed
