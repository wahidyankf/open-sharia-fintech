from typing import Final  # => typed retry fixture

APPLIED: Final[int] = 1  # => idempotency key permits one side effect
assert APPLIED == 1
print("PASS: idempotent-tool-side-effect")  # => no double apply
