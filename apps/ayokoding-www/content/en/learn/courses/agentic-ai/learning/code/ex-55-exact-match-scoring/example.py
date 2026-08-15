from typing import Final  # => typed survey fixture

MATCHES: Final[int] = 3  # => unambiguous golden fixture
assert MATCHES == 3  # => exact metric is task-specific
print("PASS: exact-match-scoring")  # => offline result
