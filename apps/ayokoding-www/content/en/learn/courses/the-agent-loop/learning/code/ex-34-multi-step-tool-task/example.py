from typing import Final  # => typed task fixture

STEPS: Final[tuple[str, str, str]] = (
    "read",
    "compute",
    "write",
)  # => ordered tool goal
assert STEPS[-1] == "write"
print("PASS: multi-step-tool-task")  # => terminal evidence
