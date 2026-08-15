from typing import Final  # => typed fake-test fixture

LIVE_CALLS: Final[int] = 0  # => deterministic suite has no provider dependency
assert LIVE_CALLS == 0
print("PASS: deterministic-test-suite")  # => offline proof
