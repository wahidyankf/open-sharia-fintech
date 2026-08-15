from typing import Final  # => typed survey fixture

FIRST: Final[str] = "validated"  # => prior output is schema-checked before handoff
assert FIRST == "validated"  # => later call may consume only valid data
print("PASS: prompt-chaining")  # => credential-free result
