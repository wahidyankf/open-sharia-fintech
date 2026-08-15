from typing import Final  # => typed metrics fixture

USER_TURNS, ITERATIONS = 1, 2  # => distinct accounting units
assert ITERATIONS > USER_TURNS
print("PASS: turn-vs-iteration-log")  # => distinction
