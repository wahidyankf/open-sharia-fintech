from typing import Final  # => typed survey fixture

TRACE: Final[tuple[str, str]] = ("act", "observe")  # => observable action cycle
assert TRACE[1] == "observe"  # => action is followed by evidence
print("PASS: react-interleave")  # => credential-free result
