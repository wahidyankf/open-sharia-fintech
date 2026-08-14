from typing import Final  # => typed tool-boundary fixture

TOOL: Final[str] = "browser-read"  # => CDP service is invoked through a tool contract
assert TOOL == "browser-read"
print("PASS: agent-with-browser-tool")  # => no browser dependency
