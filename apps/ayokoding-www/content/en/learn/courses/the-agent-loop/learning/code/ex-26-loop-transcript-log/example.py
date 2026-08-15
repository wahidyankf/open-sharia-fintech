from typing import Final  # => typed transcript fixture

EVENTS: Final[tuple[str, str]] = ("model", "tool")  # => replayable trace
assert len(EVENTS) == 2
print("PASS: loop-transcript-log")  # => inspectable record
