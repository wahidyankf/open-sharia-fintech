from typing import Final  # => typed streaming fixture

DELTAS: Final[tuple[str, str]] = ("hel", "lo")  # => ordered token chunks
assert "".join(DELTAS) == "hello"
print("PASS: streaming-final-answer")  # => assembled output
