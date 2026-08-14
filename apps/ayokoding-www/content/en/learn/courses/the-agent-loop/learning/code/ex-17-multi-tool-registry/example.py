from typing import Final  # => typed registry fixture

TOOLS: Final[set[str]] = {"calculator", "clock", "echo"}  # => allowed tools
assert len(TOOLS) == 3
print("PASS: multi-tool-registry")  # => names registered
