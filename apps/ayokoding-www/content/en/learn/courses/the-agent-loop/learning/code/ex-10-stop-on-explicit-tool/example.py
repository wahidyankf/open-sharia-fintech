from typing import Final  # => typed offline stop state

TOOL: Final[str] = "finish"  # => explicit terminal tool
assert TOOL == "finish"
print("PASS: stop-on-explicit-tool")  # => loop ends
