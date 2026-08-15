from typing import Final  # => typed survey fixture

STEPS: Final[tuple[str, ...]] = ("validate", "call", "return")  # => fixed path
assert STEPS[0] == "validate"  # => workflow begins deterministically
print("PASS: workflow-predefined-path")  # => credential-free result
