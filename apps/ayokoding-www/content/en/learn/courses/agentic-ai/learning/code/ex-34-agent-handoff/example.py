from typing import Final  # => typed survey fixture

HANDOFF: Final[tuple[str, str]] = ("lead", "specialist")  # => control transfer record
assert HANDOFF[1] == "specialist"  # => receiver is named explicitly
print("PASS: agent-handoff")  # => offline result
