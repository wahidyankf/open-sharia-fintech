from typing import Final  # => typed survey fixture

CHOICE: Final[str] = "workflow"  # => fixed task needs simpler control
assert CHOICE == "workflow"  # => agency is declined
print("PASS: when-not-agent")  # => offline result
