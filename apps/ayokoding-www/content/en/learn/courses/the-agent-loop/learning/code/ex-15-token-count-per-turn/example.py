from typing import Final  # => typed usage fixture

TOKENS: Final[int] = 12  # => per-turn accounting record
assert TOKENS == 12
print("PASS: token-count-per-turn")  # => running total input
