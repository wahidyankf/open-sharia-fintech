"""Example 27: Before/After Timing a One-Line Fix -- median of 5 perf_counter() runs, each way."""

from __future__ import annotations

import statistics
import time
from importlib import import_module


def median_of_5(module_name: str, values: list[int]) -> float:
    module = import_module(module_name)
    timings: list[float] = []
    for _ in range(5):
        start = time.perf_counter()
        module.dedupe(values)
        timings.append(time.perf_counter() - start)
    return statistics.median(timings)


if __name__ == "__main__":
    data = list(range(4000)) * 2  # 8000 items, half of them duplicates
    before = median_of_5("dedupe_before", data)
    after = median_of_5("dedupe_after", data)
    print(f"before (list membership): median={before:.4f}s")
    print(f"after  (set membership):  median={after:.4f}s")
    print(f"after is faster: {after < before}")
