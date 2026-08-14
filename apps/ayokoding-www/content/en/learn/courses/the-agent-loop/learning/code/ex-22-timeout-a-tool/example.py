from typing import Final  # => typed timeout fixture

RESULT: Final[str] = "timeout"  # => timeout becomes tool observation
assert RESULT == "timeout"
print("PASS: timeout-a-tool")  # => loop may continue
