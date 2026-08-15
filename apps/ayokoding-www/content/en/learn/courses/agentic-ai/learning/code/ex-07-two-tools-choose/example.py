from typing import Final  # => typed survey fixture

TOOLS: Final[tuple[str, str]] = ("lookup", "weather")  # => constrained offered set
assert "lookup" in TOOLS  # => survey does not implement selection runtime
print("PASS: two-tools-choose")  # => credential-free result
