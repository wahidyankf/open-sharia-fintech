from typing import Final  # => type-only survey fixture

MODE: Final[str] = "workflow"  # => fixed path is not agent autonomy
assert MODE == "workflow"  # => simpler mechanism wins
print("PASS: agent-vs-workflow")  # => credential-free result
