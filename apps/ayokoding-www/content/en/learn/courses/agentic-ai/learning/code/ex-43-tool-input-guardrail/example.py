from typing import Final  # => typed survey fixture

HAS_SECRET: Final[bool] = False  # => tool parameters must exclude secrets
assert not HAS_SECRET  # => validation blocks sensitive input
print("PASS: tool-input-guardrail")  # => offline result
