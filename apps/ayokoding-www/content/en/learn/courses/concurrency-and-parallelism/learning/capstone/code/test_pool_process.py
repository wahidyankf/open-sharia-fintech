"""Capstone: pytest verification for pool_process.py's thread- vs
process-pooled aggregation."""

from pool_process import run_processes_aggregate, run_threads_aggregate
from workload import run_serial_aggregate


def test_threads_do_not_meaningfully_speed_up_cpu_work() -> None:
    one_worker_time, baseline_total = run_serial_aggregate()
    threads_time, threads_total = run_threads_aggregate()
    assert threads_total == baseline_total
    assert threads_time > one_worker_time * 0.7  # => the GIL keeps threads from speeding up CPU work


def test_processes_do_meaningfully_speed_up_cpu_work() -> None:
    one_worker_time, baseline_total = run_serial_aggregate()
    processes_time, processes_total = run_processes_aggregate()
    assert processes_total == baseline_total
    assert processes_time < one_worker_time * 0.7  # => separate processes DO speed up CPU work


# => Run: pytest -- Output: 2 passed
