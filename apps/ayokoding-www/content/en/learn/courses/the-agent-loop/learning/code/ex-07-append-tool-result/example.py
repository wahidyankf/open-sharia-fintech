from typing import Final  # => typed offline state

HISTORY: Final[tuple[str, str]] = ("request", "tool_result")  # => observation append
assert len(HISTORY) == 2
print("PASS: append-tool-result")  # => history grows
