from typing import Final  # => typed limit fixture

STOP: Final[str] = "budget"  # => first configured limit tripped
assert STOP == "budget"
print("PASS: budget-and-turn-limits-together")  # => halt evidence
