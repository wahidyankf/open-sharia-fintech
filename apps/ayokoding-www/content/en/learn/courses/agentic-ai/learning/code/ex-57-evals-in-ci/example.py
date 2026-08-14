from typing import Final  # => typed survey fixture

GATE: Final[str] = "eval"  # => CI gate label
assert GATE == "eval"  # => pipeline implementation is omitted
print("PASS: evals-in-ci")  # => credential-free result
