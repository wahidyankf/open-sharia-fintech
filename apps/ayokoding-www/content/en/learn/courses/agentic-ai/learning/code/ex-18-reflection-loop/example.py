from typing import Final  # => typed survey fixture

RETRY_LIMIT: Final[int] = 1  # => reflection is bounded remediation
assert RETRY_LIMIT == 1  # => no unlimited self-critique loop
print("PASS: reflection-loop")  # => credential-free result
