"""Example 77: pytest verification for CPU Benchmarked Three Ways."""

from example import run_processes, run_serial, run_threads


def test_only_processes_beat_serial_on_cpu_bound_work() -> None:
    serial_time = run_serial()
    threads_time = run_threads()
    processes_time = run_processes()

    assert threads_time > serial_time * 0.7  # => the GIL keeps threads from meaningfully speeding up CPU work
    assert processes_time < serial_time * 0.7  # => separate processes DO deliver a meaningful CPU speedup


# => Run: pytest -- Output: 1 passed
