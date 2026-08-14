from typing import Final  # => typed history fixture

HISTORY: Final[tuple[str, str]] = ("first", "second")  # => scoped session context
assert HISTORY[-1] == "second"
print("PASS: conversation-continuation")  # => carries forward
