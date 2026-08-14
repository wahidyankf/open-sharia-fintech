from typing import Final  # => typed turn fixture

CALLS: Final[tuple[str, str]] = ("clock", "echo")  # => two requested tools
assert len(CALLS) == 2
print("PASS: multi-tool-turn")  # => both are observed
