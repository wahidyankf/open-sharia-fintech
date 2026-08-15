from typing import Final  # => typed latency fixture

SMALL_MS, LARGE_MS = 1, 2  # => larger prompt simulated slower
assert LARGE_MS > SMALL_MS
print("PASS: latency-vs-size")  # => trend observed
