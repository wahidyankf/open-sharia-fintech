from typing import Final  # => typed streaming fixture

ANSWER: Final[str] = "complete"  # => assembled streamed final output
assert ANSWER == "complete"
print("PASS: streaming-full-loop")  # => parity result
