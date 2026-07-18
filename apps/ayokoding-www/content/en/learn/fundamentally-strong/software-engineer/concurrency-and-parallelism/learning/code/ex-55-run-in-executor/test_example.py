"""Example 55: pytest verification for `loop.run_in_executor`."""

import asyncio

from example import TICK_INTERVAL, max_gap, run_offloaded


def test_event_loop_stays_responsive_while_offloaded_call_runs() -> None:
    timestamps, legacy_result = asyncio.run(run_offloaded())
    assert max_gap(timestamps) < TICK_INTERVAL * 3  # => the ticker never stalled -- the loop stayed responsive
    assert legacy_result == "legacy result"  # => the offloaded call still produced the correct result


# => Run: pytest -- Output: 1 passed
