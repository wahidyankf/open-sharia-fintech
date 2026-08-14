from typing import Final  # => typed survey fixture

LEGS: Final[set[str]] = {
    "private-data",
    "untrusted-content",
}  # => external action removed
assert len(LEGS) == 2  # => exfiltration path is cut
print("PASS: trifecta-mitigation")  # => credential-free result
