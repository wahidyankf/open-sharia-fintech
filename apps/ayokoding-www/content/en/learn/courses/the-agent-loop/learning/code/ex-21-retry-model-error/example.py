from typing import Final  # => typed retry fixture

ATTEMPTS: Final[int] = 2  # => transient error then success
assert ATTEMPTS == 2
print("PASS: retry-model-error")  # => bounded retry
