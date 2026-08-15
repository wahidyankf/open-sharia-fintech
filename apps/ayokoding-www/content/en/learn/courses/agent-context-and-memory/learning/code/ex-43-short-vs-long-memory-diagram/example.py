from typing import Final  # => typed diagram fixture

DIAGRAM: Final[str] = (
    "scratchpad[session state] --> agent; memory[durable store] --> agent"  # => both lifetimes
)
assert "session" in DIAGRAM and "durable" in DIAGRAM
print("PASS: short-vs-long-memory-diagram")  # => both shown
