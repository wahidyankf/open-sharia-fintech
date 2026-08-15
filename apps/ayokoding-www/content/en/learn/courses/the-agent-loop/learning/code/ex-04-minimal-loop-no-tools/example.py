from typing import Final  # => typed offline loop fixture

ITERATIONS: Final[int] = 1  # => final response stops first iteration
assert ITERATIONS == 1
print("PASS: minimal-loop-no-tools")  # => bounded result
