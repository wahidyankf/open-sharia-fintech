from typing import Final  # => typed output fixture

FINAL: Final[dict[str, str]] = {"answer": "ok"}  # => schema-shaped final answer
assert set(FINAL) == {"answer"}
print("PASS: structured-final-output")  # => validates
