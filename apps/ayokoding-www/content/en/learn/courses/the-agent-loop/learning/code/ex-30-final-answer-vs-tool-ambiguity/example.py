from typing import Final  # => typed resolution fixture

DECISION: Final[str] = "tool"  # => policy resolves text-plus-call ambiguity
assert DECISION == "tool"
print("PASS: final-answer-vs-tool-ambiguity")  # => deterministic
