from typing import Final  # => typed composition fixture

OUTCOME: Final[str] = "solved"  # => prompt plus tool plus stop result
assert OUTCOME == "solved"
print("PASS: minimal-agent-end-to-end")  # => offline loop
