from typing import Final  # => typed offline state

HISTORY: Final[tuple[str, str]] = ("system", "user")  # => ordered messages
assert HISTORY[0] == "system"
print("PASS: message-history-list")  # => structure
