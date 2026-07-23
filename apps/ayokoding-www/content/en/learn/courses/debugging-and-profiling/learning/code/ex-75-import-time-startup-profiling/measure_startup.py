"""Example 75: measure real process startup wall time, BEFORE (eager import of
slow_module) vs AFTER (deferred import) -- confirms deferring the named module
reduces startup wall time.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the measurement itself

import subprocess  # => co-13: launches EACH run as a genuinely SEPARATE process -- real startup cost, not an in-process call
import sys  # => co-13: sys.executable -- runs the SAME interpreter this script itself is running under
import time  # => co-13: time.perf_counter() -- measures REAL wall time, including full process startup


def median_startup_time(
    script: str, runs: int = 9
) -> float:  # => co-13: median, not mean -- resistant to one slow outlier run
    times: list[
        float
    ] = []  # => co-13: accumulates one wall-time measurement per fresh process launch
    for _ in range(
        runs
    ):  # => co-13: 9 independent launches -- enough to get a stable median despite OS scheduling noise
        start = (
            time.perf_counter()
        )  # => co-13: starts timing BEFORE the subprocess is even spawned
        subprocess.run(
            [sys.executable, script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )  # => co-13
        times.append(
            time.perf_counter() - start
        )  # => co-13: the REAL wall time for this ONE fresh process, start to exit
    times.sort()  # => co-13: sorts ascending so the middle element below IS the median
    return times[
        len(times) // 2
    ]  # => co-13: the median of 9 runs -- odd count, so this is a genuine middle value


def main() -> (
    None
):  # => co-13/co-23: times BOTH variants and confirms the deferred import genuinely helps
    before = median_startup_time(
        "app_before.py"
    )  # => co-13: the EAGER-import baseline -- pays slow_module's cost always
    after = median_startup_time(
        "app_after.py"
    )  # => co-23: the DEFERRED-import fix -- never pays that cost at startup
    print(
        f"median startup BEFORE (eager import of slow_module): {before:.4f}s"
    )  # => co-13: the BEFORE number, real and median
    print(
        f"median startup AFTER  (deferred import):              {after:.4f}s"
    )  # => co-23: the AFTER number, same measurement

    assert after < before, (
        "expected deferring the import to reduce startup wall time"
    )  # => co-13/co-23: the real, quantified check
    speedup = (
        before / after
    )  # => co-13/co-23: how many TIMES faster startup became, not just the raw seconds saved
    print(
        f"confirmed: deferring slow_module's import made startup {speedup:.1f}x faster"
    )  # => co-13/co-23: the headline result


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that measures both variants and reports the comparison
