from typing import Final  # => typed embedding fixture

VECTOR: Final[tuple[float, float]] = (0.1, 0.2)  # => local vector representation
assert len(VECTOR) == 2
print("PASS: embed-text")  # => dimensionality known
