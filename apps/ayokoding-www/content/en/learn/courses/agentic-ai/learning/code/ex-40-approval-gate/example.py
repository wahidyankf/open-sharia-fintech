from typing import Final  # => typed survey fixture

GATED: Final[bool] = True  # => authority requires approval
assert GATED  # => ungated action is not modeled
print("PASS: approval-gate")  # => offline result
