from typing import Final  # => typed survey fixture

LIMIT: Final[int] = 5  # => recursive step boundary
assert LIMIT > 0  # => exhaustion can halt safely
print("PASS: recursion-limit")  # => offline result
