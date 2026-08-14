from typing import Final  # => typed offline state

RESPONSE: Final[str] = "final"  # => scripted model turn
assert RESPONSE == "final"
print("PASS: model-response")  # => terminal turn
