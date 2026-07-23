"""Example 54: pytest verification for the Cooperative Blocking Hazard."""

import asyncio

from example import TICK_INTERVAL, max_gap, run_blocking_scenario, run_fixed_scenario


def test_blocking_call_starves_the_event_loop() -> None:
    timestamps = asyncio.run(run_blocking_scenario())
    assert max_gap(timestamps) > TICK_INTERVAL * 3  # => time.sleep froze the loop, delaying the ticker


def test_asyncio_sleep_keeps_the_loop_responsive() -> None:
    timestamps = asyncio.run(run_fixed_scenario())
    assert max_gap(timestamps) < TICK_INTERVAL * 3  # => asyncio.sleep cooperates, ticker stays on schedule


# => Run: pytest -- Output: 2 passed
