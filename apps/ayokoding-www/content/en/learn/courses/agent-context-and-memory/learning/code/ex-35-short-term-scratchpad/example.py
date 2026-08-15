from typing import Final  # => typed local session fixture

SCRATCHPAD: Final[dict[str, str]] = {"plan": "compare options"}  # => session state
assert SCRATCHPAD["plan"] == "compare options"
print("PASS: short-term-scratchpad")  # => persists in session
