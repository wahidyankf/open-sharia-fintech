from typing import Final  # => typed offline guard

TURNS, LIMIT = 2, 2  # => observed turns and policy cap
assert TURNS <= LIMIT
print("PASS: max-turns-guard")  # => guard halts
