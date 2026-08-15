from typing import Final  # => typed diagram fixture

FLOW: Final[tuple[str, str]] = ("summary", "recent-window")  # => rolling strategy nodes
assert len(FLOW) == 2
print("PASS: compaction-diagram")  # => flow represented
