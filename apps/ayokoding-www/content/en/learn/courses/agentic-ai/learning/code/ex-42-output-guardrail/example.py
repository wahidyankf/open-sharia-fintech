from typing import Final  # => typed survey fixture

OUTPUT_SAFE: Final[bool] = True  # => final output gate decision
assert OUTPUT_SAFE  # => unsafe output is not released
print("PASS: output-guardrail")  # => offline result
