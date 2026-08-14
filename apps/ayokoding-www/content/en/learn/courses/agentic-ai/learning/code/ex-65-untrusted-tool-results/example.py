from typing import Final  # => typed survey fixture

RESULT: Final[str] = "untrusted data"  # => tool output classification
assert RESULT.endswith("data")  # => not promoted to policy
print("PASS: untrusted-tool-results")  # => credential-free result
