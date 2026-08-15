from typing import Final  # => typed error fixture

RESULT: Final[str] = "tool_error"  # => error becomes observation
assert RESULT == "tool_error"
print("PASS: tool-error-feedback")  # => feedback
