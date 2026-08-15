from typing import Final  # => typed window fixture

RECENT: Final[tuple[str, str]] = ("turn-3", "turn-4")  # => bounded verbatim state
assert len(RECENT) == 2
print("PASS: rolling-window-plus-summary")  # => window bound
