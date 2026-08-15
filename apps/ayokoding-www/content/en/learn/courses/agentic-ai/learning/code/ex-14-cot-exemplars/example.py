from typing import Final  # => typed survey fixture

FORMAT: Final[str] = "claim: evidence"  # => exemplar constrains output format
assert ":" in FORMAT  # => format is machine-checkable
print("PASS: cot-exemplars")  # => credential-free result
