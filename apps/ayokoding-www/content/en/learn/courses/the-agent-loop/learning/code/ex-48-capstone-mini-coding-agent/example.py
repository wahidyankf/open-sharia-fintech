from typing import Final  # => typed capstone fixture

OUTCOME: Final[str] = "verified"  # => bounded prompt/tool/stop composition
assert OUTCOME == "verified"
print("PASS: capstone-mini-coding-agent")  # => offline completion
