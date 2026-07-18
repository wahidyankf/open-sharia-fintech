"""Example 3: pytest verification for The GIL Serializes CPU-Bound Threads."""

from example import run_serial, run_threaded


def test_threading_gives_no_real_speedup_on_cpu_bound_work() -> None:
    # => on a GIL-enabled build, two CPU-bound threads should NOT run near 2x faster
    serial_time = run_serial()
    threaded_time = run_threaded()
    ratio = threaded_time / serial_time
    assert ratio > 0.8  # => generous floor: real parallelism would push this near 0.5


# => Run: pytest -- Output: 1 passed
