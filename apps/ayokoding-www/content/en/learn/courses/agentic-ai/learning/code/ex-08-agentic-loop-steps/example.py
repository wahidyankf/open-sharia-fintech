from typing import Final  # => typed survey fixture

STEPS: Final[tuple[str, ...]] = (
    "request",
    "tool_use",
    "tool_result",
    "stop",
)  # => bounded cycle
assert STEPS[-1] == "stop"  # => stop is part of the model
print("PASS: agentic-loop-steps")  # => credential-free result
