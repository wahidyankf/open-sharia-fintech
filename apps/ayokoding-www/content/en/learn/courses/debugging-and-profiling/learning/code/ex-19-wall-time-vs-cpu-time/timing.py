"""Example 19: Wall Time vs. CPU Time."""

from __future__ import annotations

import time


def io_bound_sleep(seconds: float) -> None:
    time.sleep(
        seconds
    )  # the OS suspends this thread -- no CPU is consumed while waiting


def cpu_bound_busy_loop(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def timed(label: str, fn, *args: object) -> None:
    wall_start = (
        time.perf_counter()
    )  # co-15: elapsed real-world time, keeps running during I/O wait
    cpu_start = (
        time.process_time()
    )  # co-15: on-CPU time only -- does NOT advance during a sleep
    fn(*args)
    wall_elapsed = time.perf_counter() - wall_start
    cpu_elapsed = time.process_time() - cpu_start
    print(f"{label}: wall={wall_elapsed:.3f}s cpu={cpu_elapsed:.3f}s")


if __name__ == "__main__":
    timed("io_bound_sleep(0.3)", io_bound_sleep, 0.3)
    timed("cpu_bound_busy_loop(20_000_000)", cpu_bound_busy_loop, 20_000_000)
