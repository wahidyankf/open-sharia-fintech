from typing import Final  # => typed offline call fixture

CALL: Final[dict[str, str]] = {"name": "echo", "arg": "ok"}  # => parsed request
assert CALL["name"] == "echo"
print("PASS: detect-tool-call")  # => parse result
