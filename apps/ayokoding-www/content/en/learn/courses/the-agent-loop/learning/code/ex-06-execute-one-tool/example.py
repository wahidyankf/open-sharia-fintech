from typing import Final  # => typed offline tool fixture

RESULT: Final[str] = "ok"  # => registered local callable result
assert RESULT == "ok"
print("PASS: execute-one-tool")  # => dispatch evidence
