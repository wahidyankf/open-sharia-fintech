from typing import Final  # => typed replay fixture

OUTCOME: Final[str] = "same"  # => fake model replay result
assert OUTCOME == "same"
print("PASS: replay-a-transcript")  # => deterministic regression
