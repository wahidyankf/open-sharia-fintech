from typing import Final  # => typed survey fixture

LEGS: Final[set[str]] = {
    "private-data",
    "untrusted-content",
    "external-action",
}  # => risk combination
assert len(LEGS) == 3  # => all three legs are required
print("PASS: lethal-trifecta")  # => credential-free result
