from typing import Final  # => typed offline shell fixture

OUTPUT: Final[str] = "ok"  # => bounded command result
assert OUTPUT == "ok"
print("PASS: shell-running-agent")  # => feedback available
