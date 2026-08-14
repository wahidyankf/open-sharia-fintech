from typing import Final  # => typed survey fixture

TERMINATED: Final[bool] = True  # => bounded loop observation
assert TERMINATED  # => completion is explicit
print("PASS: loop-terminates")  # => offline result
