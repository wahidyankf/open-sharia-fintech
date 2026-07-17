"""Example 58: pytest verification for Free-Threaded CPU Scaling."""

from example import gil_is_enabled, measure_threaded_speedup


def test_speedup_matches_the_current_builds_gil_status() -> None:
    speedup = measure_threaded_speedup(iterations=3_000_000, thread_count=4)
    if gil_is_enabled():
        assert speedup < 2.0  # => this environment's standard build: threads don't parallelize CPU work
    else:
        assert speedup > 2.5  # => a free-threaded (python3.14t) build: threads DO parallelize CPU work


# => Run: pytest -- Output: 1 passed
