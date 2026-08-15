from typing import Final  # => typed survey fixture

ROLES: Final[tuple[str, str]] = ("lead", "subagent")  # => delegation roles
assert ROLES[0] == "lead"  # => lead retains integration responsibility
print("PASS: multi-agent-lead-subagents")  # => offline result
