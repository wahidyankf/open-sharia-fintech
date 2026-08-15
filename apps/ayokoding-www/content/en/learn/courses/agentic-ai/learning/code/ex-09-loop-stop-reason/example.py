from typing import Final  # => typed survey fixture

STOP_REASON: Final[str] = "end_turn"  # => terminal protocol state
assert STOP_REASON != "tool_use"  # => no additional action is allowed
print("PASS: loop-stop-reason")  # => credential-free result
