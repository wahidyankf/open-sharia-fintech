"""Example 84: pytest verification for Backpressure Strategies -- Buffer-All vs Keep-Latest."""

from example import CONSUMER_PERIOD, ITEM_COUNT, simulate_buffer_all, simulate_latest_only


def test_buffer_all_loses_nothing_but_its_backlog_grows() -> None:
    consumed, peak = simulate_buffer_all(ITEM_COUNT, CONSUMER_PERIOD)
    assert consumed == list(range(ITEM_COUNT))  # => every produced item is eventually consumed, in order
    assert peak > 1  # => the backlog grew well beyond a single item -- the memory-cost tradeoff


def test_latest_only_keeps_bounded_memory_but_drops_items() -> None:
    consumed, dropped = simulate_latest_only(ITEM_COUNT, CONSUMER_PERIOD)
    assert len(consumed) < ITEM_COUNT  # => far fewer items reach the consumer than were produced
    assert dropped > 0  # => at least one value was overwritten before being read -- a real, permanent loss


# => Run: pytest -- Output: 2 passed
