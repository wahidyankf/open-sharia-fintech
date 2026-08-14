from typing import Final  # => typed session fixture

HISTORY: Final[tuple[str, str]] = (
    "saved",
    "resumed",
)  # => persisted conversation state
assert HISTORY[-1] == "resumed"
print("PASS: resumable-session")  # => continuation
