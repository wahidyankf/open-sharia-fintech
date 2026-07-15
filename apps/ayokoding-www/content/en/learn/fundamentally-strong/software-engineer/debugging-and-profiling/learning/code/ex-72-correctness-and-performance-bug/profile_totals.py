import time  # => co-13: time.perf_counter() measures the SECOND half of this example -- the perf regression
import sys  # => needed only for sys.path.insert below

sys.path.insert(
    0, "."
)  # => co-13: makes the repo's own generated totals.py importable regardless of caller's cwd
from totals import (
    line_total,
)  # => co-13/co-23: the SAME function correctness-fixed just above, now profiled for speed

start = time.perf_counter()  # => co-13: starts the wall-clock timer BEFORE any calls -- a real, not simulated, measurement
for _ in range(
    200
):  # => co-13: 200 repetitions -- enough that the O(n) loop's own cost becomes clearly visible
    line_total(
        1.5, 200_000
    )  # => co-13: a large qty -- makes an O(n) implementation's cost dominate over an O(1) one
elapsed = (
    time.perf_counter() - start
)  # => co-13: the REAL wall time for all 200 calls together
print(
    f"200 calls of line_total(1.5, 200_000): {elapsed * 1e6:.1f}us"
)  # => co-13/co-23: the BEFORE/AFTER comparison point
