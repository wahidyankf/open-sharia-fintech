from typing import Final  # => typed survey fixture

SPEND: Final[int] = 2  # => local budget usage
assert SPEND <= 2  # => cap stops extra work
print("PASS: budget-cap")  # => offline result
