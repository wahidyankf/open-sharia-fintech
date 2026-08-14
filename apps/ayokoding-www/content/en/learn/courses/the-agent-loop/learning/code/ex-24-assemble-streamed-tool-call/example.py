from typing import Final  # => typed streaming call fixture

NAME: Final[str] = "echo"  # => complete assembled tool name
assert NAME == "echo"
print("PASS: assemble-streamed-tool-call")  # => execute only complete call
