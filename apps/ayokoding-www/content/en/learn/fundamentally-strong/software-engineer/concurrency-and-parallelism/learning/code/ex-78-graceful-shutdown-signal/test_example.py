"""Example 78: pytest verification for Sentinel-Driven Graceful Shutdown."""

from example import run_with_graceful_shutdown


def test_all_in_flight_work_completes_before_shutdown() -> None:
    work_items = list(range(20))
    results = run_with_graceful_shutdown(work_items)
    assert sorted(results) == work_items  # => every queued item was processed, none dropped
    assert len(results) == len(work_items)  # => nothing was processed twice either


# => Run: pytest -- Output: 1 passed
