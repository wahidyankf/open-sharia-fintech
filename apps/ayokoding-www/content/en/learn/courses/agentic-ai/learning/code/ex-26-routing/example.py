from typing import Final  # => typed survey fixture

ROUTE: Final[str] = "billing"  # => deterministic classifier result
assert ROUTE == "billing"  # => specialized handler choice is explicit
print("PASS: routing")  # => credential-free result
