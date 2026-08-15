from typing import Final  # => typed approval fixture

APPROVED: Final[bool] = False  # => risky tool stays paused
assert not APPROVED
print("PASS: human-in-the-loop-gate")  # => waits safely
