"""Example 73: pytest verification for `asyncio.to_thread`."""

import asyncio

from example import TICK_INTERVAL, max_gap, run_with_to_thread


def test_event_loop_stays_responsive_while_to_thread_call_runs() -> None:
    timestamps, result = asyncio.run(run_with_to_thread())
    assert max_gap(timestamps) < TICK_INTERVAL * 3  # => the ticker never stalled -- the loop stayed responsive
    assert result == "legacy result"  # => the offloaded call still produced the correct result


# => Run: pytest -- Output: 1 passed
