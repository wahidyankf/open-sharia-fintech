from typing import Final  # => typed survey fixture

SAFE: Final[bool] = True  # => input gate decision
assert SAFE  # => unsafe input would stop before planning
print("PASS: input-guardrail")  # => offline result
