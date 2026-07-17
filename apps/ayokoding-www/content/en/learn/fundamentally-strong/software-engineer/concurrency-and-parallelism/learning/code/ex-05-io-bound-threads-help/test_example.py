"""Example 5: pytest verification for I/O-Bound Threads Actually Help."""

from example import run_serial, run_threaded


def test_threaded_io_beats_serial_io() -> None:
    calls = 4
    serial_time = run_serial(calls)
    threaded_time = run_threaded(calls)
    assert threaded_time < serial_time * 0.5  # => threads overlap I/O; the GIL doesn't block sleep


# => Run: pytest -- Output: 1 passed
