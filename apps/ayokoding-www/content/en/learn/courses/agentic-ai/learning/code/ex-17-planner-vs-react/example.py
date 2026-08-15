from typing import Final  # => typed survey fixture

MODES: Final[set[str]] = {"plan", "observe_each_step"}  # => two control tradeoffs
assert len(MODES) == 2  # => comparison remains survey-level
print("PASS: planner-vs-react")  # => credential-free result
