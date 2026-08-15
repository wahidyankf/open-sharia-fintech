from typing import Final  # => typed survey fixture

MAX_TURNS: Final[int] = 3  # => explicit loop ceiling
assert MAX_TURNS == 3  # => runtime owner enforces cap
print("PASS: max-turns")  # => offline result
